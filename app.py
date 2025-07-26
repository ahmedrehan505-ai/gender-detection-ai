from flask import Flask, render_template, request, jsonify
import joblib
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Upload folder setup
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load trained model (saved with joblib)
model_path = os.path.join("data", "gender_model.pkl")
model = joblib.load(model_path)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'})

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Read and preprocess image
    img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return jsonify({'error': 'Image not readable'})
    
    # Resize and normalize (if model trained on normalized data)
    img = cv2.resize(img, (100, 100)).astype('float32') / 255.0
    img = img.flatten().reshape(1, -1)

    # Predict
    prediction = model.predict(img)[0]
    gender = 'Male' if prediction == 0 else 'Female'

    # Key features (dummy values)
    features = []
    if gender == 'Male':
        features = ['Square jawline', 'Prominent brow ridge', 'Thicker eyebrows']
    else:
        features = ['Round jawline', 'Softer facial features', 'Thinner eyebrows']

    return jsonify({
        'gender': gender,
        'filename': filename,
        'features': features
    })

if __name__ == '__main__':
    # For production, remove debug=True and set host for network access
    app.run(host="0.0.0.0", port=5000, debug=True)
