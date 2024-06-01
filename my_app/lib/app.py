import base64
import flask
import os
import tensorflow as tf
import numpy as np
import cv2

app = flask.Flask(__name__) 

@app.route('/predict', methods=['POST'])
def predict():
    """
    The main function to predict the image. This function is called when the front end sends a POST request.
    This function implements input validation, image processing, and model prediction.
    """

    # Get the image data from the front end
    img_data = flask.request.json['base64_bytes']

    # Return error code 452 if the image data is invalidated by the front end
    if img_data == "":
        return flask.jsonify({'error': 'Not an image file format! Please use .jpg, .jpeg or .png only.'}), 452

    img_bytes = base64.b64decode(img_data)

    try:
        # Convert the image data to a numpy array
        np_array = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    except Exception as _:
        # Return error code 453 if the image can't be converted
        return flask.jsonify({'error': 'Invalid image, please try using another image.'}), 453
        
    # Convert the image to grayscale for face detection
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face = face_classifier.detectMultiScale(gray_image, minNeighbors=3)

    # Crop the image to the face
    if len(face) != 0:
        (x, y, w, h) = face[0]
        img = img[y:y+h, x:x+w]
    
    # Sharpen the image
    img = sharpen(img)
    
    # Resize the image to 224x224
    input = cv2.resize(img, (224, 224))
    input = input.astype(np.uint8)

    # Predict the image using the model
    idx = np.argmax(model.predict(np.array([input]))[0])
    sharpened_image_bytes = cv2.imencode('.png', img)[1].tostring()

    # Show the name of the predicted person
    print(names[idx])

    # Return the prediction and the sharpened image
    return flask.jsonify({'prediction': names[idx],'sharpened_image': base64.b64encode(sharpened_image_bytes).decode()}), 200

@app.route('/names', methods=['GET'])
def get_names():
    """
    Function to get the names of the people in the dataset. This is used for the front end
    to check whether a user has entered a valid name.
    """
    names = [name.strip() for name in open("lfw_names.txt", "r").readlines()]
    return flask.jsonify({'names': names})

def sharpen(image):
    """
    This function implements a simple sharpening kernel to sharpen the image.
    """
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    kernel = 1/3 * kernel
    return cv2.filter2D(image, -1, kernel)

if __name__ == '__main__': 
    os.chdir(os.getcwd()+"/lib")

    # Load the face classifier
    face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Load the model 
    checkpoint_path = "lfw_skipconn_model/"
    checkpoint_dir = os.path.dirname(checkpoint_path)
    model = tf.keras.models.load_model(checkpoint_dir)

    # Load the names of the people in the dataset
    names = open("lfw_names.txt", "r").read().split("\n")

    app.run()