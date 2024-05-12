
# @app.route('/predict', methods=['POST'])
# def predict():
#     if 'base64_bytes' not in flask.request.json or 'name' not in flask.request.json:
#         return flask.jsonify({'error': 'No image provided'}), 452

#     img_data = flask.request.json['base64_bytes']
#     img_bytes = base64.b64decode(img_data)

#     try:
#         np_array = np.frombuffer(img_bytes, np.uint8)
#         img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
#     except Exception as e:
#         return flask.jsonify({'error': 'Invalid image'}), 453
        
#     gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#     face = face_classifier.detectMultiScale(gray_image, minNeighbors=3)
#     if len(face) != 0:
            
#         (x, y, w, h) = face[0]
#         img = img[y:y+h, x:x+w]
    

#     img = sharpen(img)
    
#     input = cv2.resize(img, (224, 224))
#     # input = cv2.cvtColor(input, cv2.COLOR_BGR2RGB)
#     input = input.astype(np.uint8)
    
#     checkpoint_path = "skipconn_model/"
#     checkpoint_dir = os.path.dirname(checkpoint_path)
#     model = tf.keras.models.load_model(checkpoint_dir)

#     names = open("names.txt", "r").read().split("\n")

#     idx = np.argmax(model.predict(np.array([input]))[0])
#     sharpened_image_bytes = cv2.imencode('.png', img)[1].tostring()
#     return flask.jsonify({'prediction': names[idx],'sharpened_image': base64.b64encode(sharpened_image_bytes).decode()}), 200
