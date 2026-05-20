import sys
import os

# Add AI root directory to Python path
BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

sys.path.append(BASE_DIR)

from attendance.mark_attendance import (
    mark_attendance
)
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

# Load face detector
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# Open webcam
camera = cv2.VideoCapture(0)

print("\nRecognition started...")
print("Press Q to quit\n")

while True:

    success, frame = camera.read()

    if not success:
        print("Failed to access camera")
        break

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    # Detect faces
    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5
    )

    for (x, y, w, h) in faces:

        # Draw rectangle
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        # Face region
        face_region = gray[y:y+h, x:x+w]

        # Predict face
        label, confidence = recognizer.predict(
            face_region
            
        )
        print("Confidence:", confidence)

        # Recognition threshold
        if confidence < 100:

            user_name = labels.get(
                label,
                "Unknown"
            )

            text = f"{user_name}"
            mark_attendance(user_name)

        else:
            text = "Unknown"

        # Display name
        cv2.putText(
            frame,
            text,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 0),
            2
        )

    # Show webcam
    cv2.imshow(
        "Face Recognition",
        frame
    )

    # Quit
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

# Cleanup
camera.release()
cv2.destroyAllWindows()