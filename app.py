from flask import Flask, render_template, request, jsonify
import pickle
import os
import cv2
import numpy as np

app = Flask(__name__, template_folder='templates', static_folder='static')

# Load the gender prediction model
with open("data/gender_model.pkl", "rb") as f:
    model = pickle.load(f)

# Route for main page
@app.route('/')
def index():
    return render_template("index.html")

# Route for image upload and prediction
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'})

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Save uploaded image
    upload_folder = os.path.join(app.static_folder, 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    file_path = os.path.join(upload_folder, file.filename)
    file.save(file_path)

    # Read image using OpenCV
    image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        return jsonify({'error': 'Invalid image format'})

     # Resize and flatten the image for prediction
    image = cv2.resize(image, (100, 100))  # Match your model training size
    image = image.flatten().reshape(1, -1)

    # Predict gender
    prediction = model.predict(image)[0]
    gender = 'Male' if prediction == 1 else 'Female'

    return jsonify({'gender': gender, 'image_path': f'static/uploads/{file.filename}'})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
