from flask import Flask, render_template, request, jsonify
import pickle
import cv2
import numpy as np
import os
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder='templates', static_folder='static')
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load trained model
model_path = os.path.join("data", "gender_model.pkl")
with open(model_path, "rb") as f:
    model = pickle.load(f)

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

    # Process image
    img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return jsonify({'error': 'Image not readable'})
    img = cv2.resize(img, (100, 100)).flatten().reshape(1, -1)

    # Predict
    prediction = model.predict(img)[0]
    gender = 'Male' if prediction == 0 else 'Female'

    # Key features (optional, dummy values)
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
    app.run(debug=True)
