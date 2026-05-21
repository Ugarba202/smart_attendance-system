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

    # Get user from database
    user = db.query(User).filter(
        User.full_name ==
        result["full_name"]
    ).first()

    if not user:

        return {
            "status": "error",
            "message":
            "User not found"
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
            user.department
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