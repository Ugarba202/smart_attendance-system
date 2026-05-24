from app.services.attendance_service import (
    mark_attendance
)

from app.services.train_service import (
    train_model
)

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User

from app.services.recognize_service import (
    recognize_face
)

import shutil
import os

router = APIRouter()


@router.post("/recognize")
def recognize(
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # Temp upload folder
    temp_folder = "temp_uploads"

    os.makedirs(
        temp_folder,
        exist_ok=True
    )

    # Save uploaded image
    image_path = os.path.join(
        temp_folder,
        image.filename
    )

    with open(
        image_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            image.file,
            buffer
        )

    # Run AI recognition
    result = recognize_face(
        image_path
    )

    # If not recognized
    if result["status"] != "recognized":
        return result

    # Get recognized name
    recognized_name = (
        result["full_name"]
        .strip()
        .lower()
    )

    # Search user loosely
    users = db.query(User).all()

    user = None

    for db_user in users:

        db_name = (
            db_user.full_name
            .strip()
            .lower()
        )

        if (
            recognized_name in db_name
            or
            db_name in recognized_name
        ):
            user = db_user
            break

    # If user not found
    if not user:

        return {
            "status": "error",
            "message":
            f"User not found: {recognized_name}"
        }

    # Mark attendance
    attendance_result = (
        mark_attendance(
            db,
            user.full_name
        )
    )

    return {
        "status": "recognized",

        "attendance_marked":
        attendance_result[
            "attendance_marked"
        ],

        "message":
        attendance_result[
            "message"
        ],

        "user": {
            "id": user.id,
            "full_name":
            user.full_name,
            "department":
            user.department,
            "registration_number":
            user.registration_number
        },

        "confidence":
        result["confidence"]
    }


@router.post("/train-model")
def retrain_model():

    train_model()

    return {
        "status": "success",
        "message":
        "Model trained successfully"
    }