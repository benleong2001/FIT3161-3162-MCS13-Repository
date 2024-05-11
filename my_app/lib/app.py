import base64
import io
import flask
import os
import tensorflow as tf
import numpy as np

from PIL import Image

app = flask.Flask(__name__) 

@app.route('/predict', methods=['POST'])
def predict():
    if 'base64_bytes' not in flask.request.json or 'name' not in flask.request.json:
        return flask.jsonify({'error': 'No image provided'}), 400

    img_data = flask.request.json['base64_bytes']
    img_bytes = base64.b64decode(img_data)

    try:
        img = Image.open(io.BytesIO(img_bytes))
    except Exception as e:
        return flask.jsonify({'error': 'Invalid image'}), 400

    input = np.array(img.resize((224, 224)), "uint8")
    
    checkpoint_path = "skipconn_model/"
    checkpoint_dir = os.path.dirname(checkpoint_path)
    model = tf.keras.models.load_model(checkpoint_dir)

    names = open("names.txt", "r").read().split("\n")

    idx = np.argmax(model.predict(np.array([input]))[0])

    return flask.jsonify({'prediction': names[idx]}), 200

if __name__ == '__main__': 
    os.chdir(os.getcwd()+"/lib")
    app.run()