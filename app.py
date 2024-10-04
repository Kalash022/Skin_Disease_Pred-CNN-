from flask import Flask, request, jsonify, render_template
from keras.models import load_model
import numpy as np
import cv2
import os

app = Flask(__name__)

model = load_model('skin_disease_model.h5')

@app.route('/')
def home():
    return render_template('index.html')  # This serves the index.html file

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    
    img = cv2.resize(img, (224, 224))
    img = img / 255.0 
    img = np.expand_dims(img, axis=0) 

    predictions = model.predict(img)
    class_index = np.argmax(predictions, axis=1)[0]

    labels = ['Disease 1', 'Disease 2', 'Disease 3']  
    predicted_label = labels[class_index]

    return jsonify({'predicted_disease': predicted_label})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
