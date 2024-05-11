import base64
import io
import flask
import os
import tensorflow as tf
import numpy as np

from PIL import Image
import cv2


app = flask.Flask(__name__) 

@app.route('/predict', methods=['POST'])
def predict():
    if 'base64_bytes' not in flask.request.json or 'name' not in flask.request.json:
        return flask.jsonify({'error': 'No image provided'}), 401

    img_data = flask.request.json['base64_bytes']
    img_bytes = base64.b64decode(img_data)

    try:
        np_array = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    except Exception as e:
        return flask.jsonify({'error': 'Invalid image'}), 400
        
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    face = face_classifier.detectMultiScale(gray_image, minNeighbors=3)

    (x, y, w, h) = face[0]
    img = img[y:y+h, x:x+w]

    img = sharpen(img)
    
    input = cv2.resize(img, (224, 224))
    # input = cv2.cvtColor(input, cv2.COLOR_BGR2RGB)
    input = input.astype(np.uint8)
    
    checkpoint_path = "skipconn_model/"
    checkpoint_dir = os.path.dirname(checkpoint_path)
    model = tf.keras.models.load_model(checkpoint_dir)

    names = open("names.txt", "r").read().split("\n")

    idx = np.argmax(model.predict(np.array([input]))[0])

    return flask.jsonify({'prediction': names[idx]}), 200

def test(img):

    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    face = face_classifier.detectMultiScale(gray_image, minNeighbors=3)

    # for (x, y, w, h) in face:
    #     cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    (x, y, w, h) = face[0]
    img = img[y:y+h, x:x+w]

    img = cv2.resize(img, (224, 224))
    img = sharpen(img)
    input = np.array(img, "uint8")
    
    checkpoint_path = "skipconn_model/"
    checkpoint_dir = os.path.dirname(checkpoint_path)
    model = tf.keras.models.load_model(checkpoint_dir)

    names = open("names.txt", "r").read().split("\n")

    idx = np.argmax(model.predict(np.array([input]))[0])

    print(names[idx])

    cv2.imshow("image", img)
    cv2.waitKey(0)

def sharpen(image):
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    kernel = 1/3 * kernel
    return cv2.filter2D(image, -1, kernel)

if __name__ == '__main__': 
    os.chdir(os.getcwd()+"/lib")
    app.run()
    # test()