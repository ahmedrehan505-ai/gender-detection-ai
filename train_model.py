import os
import cv2
import numpy as np
from sklearn.svm import SVC
import joblib
import matplotlib.pyplot as plt

def load_images(folder, label):
    images = []
    labels = []
    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            continue
        img = cv2.resize(img, (100, 100)).astype('float32') / 255.0  # normalize
        images.append(img.flatten())
        labels.append(label)
    return images, labels

def show_sample_images(folder, title, num_samples=5):
    plt.figure(figsize=(10, 2))
    files = os.listdir(folder)[:num_samples]
    for i, filename in enumerate(files):
        path = os.path.join(folder, filename)
        img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            img = cv2.resize(img, (100, 100))
            plt.subplot(1, num_samples, i + 1)
            plt.imshow(img, cmap='gray')
            plt.axis('off')
            plt.title(f"{title} {i+1}")
    plt.suptitle(f"Sample Images: {title}")
    plt.tight_layout()
    plt.show()

# Show sample images to verify correct folders
show_sample_images("data/male", "Male")
show_sample_images("data/female", "Female")

# Load male and female images
male_images, male_labels = load_images("data/male", 0)       # 0 = Male
female_images, female_labels = load_images("data/female", 1) # 1 = Female

# Combine data
X = np.array(male_images + female_images)
y = np.array(male_labels + female_labels)

print("Training data shape:", X.shape)

# Train the model
model = SVC(kernel='linear', probability=True, random_state=42)
model.fit(X, y)

# Save the model using joblib
model_path = "data/gender_model.pkl"
joblib.dump(model, model_path)

print(f"Model trained and saved as {model_path}")
