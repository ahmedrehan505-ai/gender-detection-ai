import os
import cv2
import pickle

# Load trained model
with open("data/gender_model.pkl", "rb") as f:
    model = pickle.load(f)

# Folder containing test images
test_folder = "test_images"

# Loop through each image in the test folder
for filename in os.listdir(test_folder):
    path = os.path.join(test_folder, filename)
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f" Skipping invalid image: {filename}")
        continue

    img = cv2.resize(img, (100, 100))
    img_flatten = img.flatten().reshape(1, -1)

    prediction = model.predict(img_flatten)[0]

    label = "Male" if prediction == 0 else "Female"
    print(f" {filename} -> Predicted: {label}")
