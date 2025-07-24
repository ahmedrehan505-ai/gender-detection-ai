import os
import cv2
import numpy as np
from sklearn.svm import SVC
import pickle

def load_images(folder, label):
    images = []
    labels = []
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        img = cv2.resize(img, (100, 100))
        images.append(img.flatten())
        labels.append(label)
    return images, labels

# Load male and female images
male_images, male_labels = load_images("data/male", 0)     # 0 = Male
female_images, female_labels = load_images("data/female", 1)  # 1 = Female

# Combine data
X = np.array(male_images + female_images)
y = np.array(male_labels + female_labels)

print("Training data shape:", X.shape)

# Train the model
model = SVC(kernel='linear')
model.fit(X, y)

# Save the model
with open("gender_model.pkl", "wb") as f:
    pickle.dump(model, f)

print(" Model trained and saved as gender_model.pkl")
