import cv2
import os

# Load face detector
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)

# Ask user name
user_name = input("Enter user name: ").strip()

# Absolute AI base directory
BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

# Dataset path
dataset_path = os.path.join(
    BASE_DIR,
    "datasets",
    user_name
)

print("Dataset path:", dataset_path)

# Create folder
os.makedirs(dataset_path, exist_ok=True)

# Open webcam
camera = cv2.VideoCapture(0)

image_count = 0
max_images = 20

print("\nCamera started...")
print("Face images will auto-save")
print("Press Q to quit\n")

while True:

    success, frame = camera.read()

    if not success:
        print("Failed to access camera")
        break

    # Convert to grayscale
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

    # Draw rectangles and crop face
    for (x, y, w, h) in faces:

        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

        # Crop face
        face_crop = frame[y:y+h, x:x+w]

        # Auto-save images
        if image_count < max_images:

            image_count += 1

            image_path = os.path.join(
                dataset_path,
                f"face_{image_count}.jpg"
            )

            cv2.imwrite(
                image_path,
                face_crop
            )

            print(
                f"Saved image {image_count}/{max_images}"
            )

            # Delay for better image variety
            cv2.waitKey(500)

    # Show webcam
    cv2.imshow(
        "User Registration",
        frame
    )

    # Stop after enough images
    if image_count >= max_images:
        print("\nRegistration completed!")
        break

    # Quit manually
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

# Cleanup
camera.release()
cv2.destroyAllWindows()