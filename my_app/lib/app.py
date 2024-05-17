import base64
import flask
import os
import tensorflow as tf
import numpy as np
import cv2

app = flask.Flask(__name__) 

@app.route('/predict', methods=['POST'])
def predict():

    img_data = flask.request.json['base64_bytes']

    if img_data == "":
        return flask.jsonify({'error': 'Not an image file format! Please use .jpg, .jpeg or .png only.'}), 452

    img_bytes = base64.b64decode(img_data)

    try:
        np_array = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    except Exception as _:
        return flask.jsonify({'error': 'Invalid image, please try using another image.'}), 453
        
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face = face_classifier.detectMultiScale(gray_image, minNeighbors=3)

    if len(face) != 0:
        (x, y, w, h) = face[0]
        img = img[y:y+h, x:x+w]
    
    img = sharpen(img)
    
    input = cv2.resize(img, (224, 224))
    input = input.astype(np.uint8)

    idx = np.argmax(model.predict(np.array([input]))[0])
    sharpened_image_bytes = cv2.imencode('.png', img)[1].tostring()
    return flask.jsonify({'prediction': names[idx],'sharpened_image': base64.b64encode(sharpened_image_bytes).decode()}), 200


@app.route('/names', methods=['GET'])
def get_names():
    names = [name.strip() for name in open("names.txt", "r").readlines()]
    return flask.jsonify({'names': names})

def sharpen(image):
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    kernel = 1/3 * kernel
    return cv2.filter2D(image, -1, kernel)

if __name__ == '__main__': 
    os.chdir(os.getcwd()+"/lib")

    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    checkpoint_path = "lfw_skipconn_model/"
    checkpoint_dir = os.path.dirname(checkpoint_path)
    model = tf.keras.models.load_model(checkpoint_dir)

    names = open("lfw_names.txt", "r").read().split("\n")

    app.run()