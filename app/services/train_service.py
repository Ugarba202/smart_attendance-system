import os
import cv2
import numpy as np
BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "AI"
    )
)


def train_model():

    dataset_path = os.path.join(
        BASE_DIR,
        "datasets"
    )

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

    recognizer = (
        cv2.face
        .LBPHFaceRecognizer_create()
    )

    faces = []
    labels = []

    label_map = {}
    current_label = 0

    for user_name in os.listdir(
        dataset_path
    ):

        user_folder = os.path.join(
            dataset_path,
            user_name
        )

        if not os.path.isdir(
            user_folder
        ):
            continue

        if user_name not in label_map:

            label_map[user_name] = (
                current_label
            )

            current_label += 1

        label_id = label_map[
            user_name
        ]

        for image_name in os.listdir(
            user_folder
        ):

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
            labels.append(label_id)

    recognizer.train(
    faces,
    np.array(labels)
)

    recognizer.save(model_path)

    with open(
        label_path,
        "w"
    ) as file:

        for name, label in (
            label_map.items()
        ):

            file.write(
                f"{label},{name}\n"
            )

    return {
        "message":
        "Model trained successfully"
    }