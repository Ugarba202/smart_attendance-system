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

    # temp folder
    temp_folder = (
        "temp_uploads"
    )

    os.makedirs(
        temp_folder,
        exist_ok=True
    )

    image_path = (
        os.path.join(
            temp_folder,
            image.filename
        )
    )

    with open(
        image_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            image.file,
            buffer
        )

    # AI recognition
    result = recognize_face(
        image_path
    )

    if (
        result["status"]
        != "recognized"
    ):

        return result

    # recognized label
    recognized_label = (
        result["full_name"]
        .strip()
        .lower()
    )

    # IMPORTANT FIX:
    # search registration number
    user = (
        db.query(User)
        .filter(
            User.registration_number
            .ilike(
                recognized_label
            )
        )
        .first()
    )

    if not user:

        return {
            "status":
            "error",

            "message":
            f"User not found: {recognized_label}"
        }

    # mark attendance
    attendance_result = (
        mark_attendance(
            db,
            user.full_name
        )
    )

    return {

        "status":
        "recognized",

        "attendance_marked":
        attendance_result[
            "attendance_marked"
        ],

        "message":
        attendance_result[
            "message"
        ],

        "user": {

            "id":
            user.id,

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


@router.post(
    "/train-model"
)
def retrain_model():

    train_model()

    return {
        "status":
        "success",

        "message":
        "Model trained successfully"
    }