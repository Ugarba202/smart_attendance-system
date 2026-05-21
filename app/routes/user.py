import shutil
import os

import shutil
import os

from app.services.train_service import (
    train_model
)

from sqlalchemy.orm import Session
from fastapi import Depends

from app.database import get_db
from app.models.user import User

from fastapi import (
    
    
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form
)

from sqlalchemy.orm import Session

from app.database import (
    get_db
)

from app.models.user import User

from app.services.train_service import (
    train_model
)

import os
import shutil

router = APIRouter()

BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "AI"
    )
)


@router.post("/register-user")
def register_user(
    full_name: str = Form(...),
    department: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # Save image folder
    dataset_folder = os.path.join(
        BASE_DIR,
        "datasets",
        full_name.lower()
    )

    os.makedirs(
        dataset_folder,
        exist_ok=True
    )

    image_path = os.path.join(
        dataset_folder,
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

    # Save DB user
    new_user = User(
        full_name=full_name,
        department=department,
        image_path=image_path
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Auto train model
    train_model()

    return {
        "message":
        "User registered successfully",

        "user": {
            "id": new_user.id,
            "full_name":
            new_user.full_name
        }
    }
@router.get("/users")
def get_users(db: Session = Depends(get_db)):

    users = db.query(User).all()

    return users

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    # Find user
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        return {
            "status": "error",
            "message": "User not found"
        }

    # Dataset folder path
    base_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "AI"
        )
    )

    dataset_path = os.path.join(
        base_dir,
        "datasets",
        user.full_name
    )

    # Delete dataset folder
    if os.path.exists(dataset_path):

        shutil.rmtree(dataset_path)

    # Delete DB record
    db.delete(user)
    db.commit()

    # Retrain model
    train_model()

    return {
        "status": "success",
        "message": (
            "User deleted "
            "successfully"
        )
    }

@router.delete("/users/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):

    # Find user
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:

        return {
            "status": "error",
            "message": "User not found"
        }

    # Dataset folder path
    base_dir = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "AI"
        )
    )

    dataset_path = os.path.join(
        base_dir,
        "datasets",
        user.full_name.lower()
    )

    # Delete dataset folder
    if os.path.exists(dataset_path):

        shutil.rmtree(dataset_path)

    # Delete user from database
    db.delete(user)
    db.commit()

    # Retrain model
    from app.services.train_service import (
        train_model
    )

    train_model()

    return {
        "status": "success",
        "message":
        "User deleted successfully"
    }