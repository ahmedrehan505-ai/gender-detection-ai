import cv2
import numpy as np
import joblib

# Load the trained model
model = joblib.load("gender_model.pkl")

# Define test image path
image_path = "test_images/test1.jpg"

# Load and preprocess image
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
if img is None:
    print("❌ Failed to load image. Check path.")
    exit()

img = cv2.resize(img, (100, 100))
img = img.flatten().reshape(1, -1)

# Predict gender
prediction = model.predict(img)[0]
gender = "Male" if prediction == 0 else "Female"

print(f"Predicted Gender: {gender}")
