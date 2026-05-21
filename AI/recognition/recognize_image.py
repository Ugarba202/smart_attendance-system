import cv2
import os

# Base directory
BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
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

    print("Image loaded:", image_path)

    # Preview image
    cv2.imshow(
        "Test Image",
        image
    )

    cv2.waitKey(1000)
    cv2.destroyAllWindows()

    # Convert to grayscale
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    # Since image is already cropped face
    face_region = gray

    # Predict face
    label, confidence = recognizer.predict(
        face_region
    )

    print(
        "Confidence:",
        confidence
    )

    # Recognition threshold
    if confidence < 100:

        user_name = labels.get(
            label,
            "Unknown"
        )

        return {
            "status": "recognized",
            "user": user_name,
            "confidence": confidence
        }

    return {
        "status": "unknown",
        "user": "Unknown",
        "confidence": confidence
    }


# Test run
if __name__ == "__main__":

    image_path = input(
        "Enter image path: "
    )

    result = recognize_face(
        image_path
    )

    print(result)