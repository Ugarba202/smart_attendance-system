import cv2
import os

# Base AI directory
BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "AI"
    )
)

# Model paths
model_path = os.path.join(
    BASE_DIR,
    "models",
    "trained_model.yml"
)

label_path = os.path.join(
    BASE_DIR,
    "models",
    "labels.txt"
)

# Load recognizer
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(model_path)

# Load labels
labels = {}

with open(label_path, "r") as file:

    for line in file:

        label_id, name = line.strip().split(",")

        labels[int(label_id)] = name


def recognize_face(image_path):

    # Read image
    image = cv2.imread(image_path)

    if image is None:

        return {
            "status": "error",
            "message": "Image not found"
        }

    # Convert image
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # Since saved image is face crop
    face_region = gray

    # Predict
    label, confidence = recognizer.predict(
        face_region
    )

    # Threshold
    if confidence < 100:

        user_name = labels.get(
            label,
            "Unknown"
        )

        return {
            "status": "recognized",
            "full_name": user_name,
            "confidence": confidence,
        }

    return {
        "status": "unknown",
        "full_name": "Unknown",
        "confidence": float(confidence)
    }