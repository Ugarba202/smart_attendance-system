from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
import shutil
import os

from app.database import SessionLocal
from app.models.user import User

router = APIRouter()


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users")
async def create_user(
    full_name: str = Form(...),
    registration_number: str = Form(...),
    department: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Create folder for user images
    user_folder = f"AI/datasets/{registration_number}"
    os.makedirs(user_folder, exist_ok=True)

    file_path = os.path.join(
        user_folder,
        image.filename
    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            image.file,
            buffer
        )

    # Save to database
    new_user = User(
        full_name=full_name,
        registration_number=registration_number,
        department=department,
        image_path=file_path,
        status="Active"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user": {
            "id": new_user.id,
            "full_name": new_user.full_name,
            "registration_number": new_user.registration_number,
            "department": new_user.department,
            "status": new_user.status
        }
    }


@router.get("/users")
def get_users(
    db: Session = Depends(get_db)
):
    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "full_name": user.full_name,
            "registration_number":
                user.registration_number,
            "department": user.department,
            "status": user.status
        }
        for user in users
    ]

import shutil
import os


@router.delete(
    "/users/{user_id}"
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        return {
            "status": "error",
            "message":
            "User not found"
        }

    dataset_path = os.path.join(
        "AI",
        "datasets",
        user.full_name.lower()
    )

    if os.path.exists(
        dataset_path
    ):
        shutil.rmtree(
            dataset_path
        )

    db.delete(user)
    db.commit()

    return {
        "status": "success",
        "message":
        "User deleted successfully"
    }

from fastapi import HTTPException


@router.put(
    "/users/{user_id}"
)
def update_user(
    user_id: int,
    payload: dict,
    db: Session = Depends(get_db)
):

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user.full_name = payload.get(
        "full_name",
        user.full_name
    )

    user.registration_number = (
        payload.get(
            "registration_number",
            user.registration_number
        )
    )

    user.department = payload.get(
        "department",
        user.department
    )

    user.status = payload.get(
        "status",
        user.status
    )

    db.commit()
    db.refresh(user)

    return {
        "message":
        "User updated successfully"
    }