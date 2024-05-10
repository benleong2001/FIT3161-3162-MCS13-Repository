import flask
import os
import tensorflow as tf
import numpy as np

from PIL import Image

app = flask.Flask(__name__) 

@app.route('/') 
def hello_world(): 
    os.chdir('C:/Users/User/OneDrive/Desktop/Monash/FIT3162/git/FIT3161-3162-MCS13-Repository/my_app/lib') 
    checkpoint_path = "skipconn_model/" 
    checkpoint_dir = os.path.dirname(checkpoint_path) 
    model = tf.keras.models.load_model(checkpoint_dir) 

    img = Image.open('000023.jpg').resize((224,224)) 
    input = np.array(img, "uint8") 

    names = open("names.txt", "r") 
    names = names.read().split("\n") 

    idx = np.argmax(model.predict(np.array([input]))[0]) 

    print(names[idx])

    return names[idx]
    
if __name__ == '__main__': 
    app.run()

