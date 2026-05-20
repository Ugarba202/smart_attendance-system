import cv2
import os
import numpy as np

# Paths
BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

dataset_path = os.path.join(
    BASE_DIR,
    "datasets"
)

model_path = os.path.join(
    BASE_DIR,
    "models",
    "trained_model.yml"
)

# Create recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()

faces = []
labels = []

label_map = {}

current_label = 0

# Read dataset folders
for user_name in os.listdir(dataset_path):

    user_folder = os.path.join(
        dataset_path,
        user_name
    )

    # Skip non-folders
    if not os.path.isdir(user_folder):
        continue

    label_map[current_label] = user_name

    # Read images
    for image_name in os.listdir(user_folder):

        image_path = os.path.join(
            user_folder,
            image_name
        )

        image = cv2.imread(
            image_path,
            cv2.IMREAD_GRAYSCALE
        )

        if image is None:
            continue

        faces.append(image)
        labels.append(current_label)

    current_label += 1

# Convert labels
labels = np.array(labels)

# Train recognizer
print("Training model...")

recognizer.train(faces, labels)

# Save model
recognizer.save(model_path)

print("\nModel trained successfully!")
print(f"Model saved at:\n{model_path}")

# Save label mapping
label_file = os.path.join(
    BASE_DIR,
    "models",
    "labels.txt"
)

with open(label_file, "w") as file:

    for label, name in label_map.items():
        file.write(f"{label},{name}\n")

print("\nLabels saved successfully!")