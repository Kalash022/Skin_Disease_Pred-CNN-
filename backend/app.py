from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np

app = Flask(__name__)

# Load your CNN model here
model = load_model('Skin_Disease_Pred-CNN-/backend/saved_model/skin_disease_model.h5')

def preprocess_image(image):
    image = image.resize((224, 224))  # Example size, change to match your model input
    image = np.array(image) / 255.0   # Normalize
    image = np.expand_dims(image, axis=0)  # Add batch dimension
    return image

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    image = Image.open(file)
    processed_image = preprocess_image(image)
    
    prediction = model.predict(processed_image)
    # Map prediction to disease labels (customize as per your model)
    diagnosis = np.argmax(prediction, axis=1)
    
    return jsonify({"diagnosis": str(diagnosis)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
