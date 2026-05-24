from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import (
    Session
)

from app.database import (
    get_db
)

from app.models.admin import (
    Admin
)

router = APIRouter()


# -------------------
# LOGIN
# -------------------
@router.post("/login")
def login(
    payload: dict,
    db: Session = Depends(get_db)
):

    username = payload.get(
        "username"
    )

    password = payload.get(
        "password"
    )

    admin = db.query(Admin).filter(
        Admin.username ==
        username
    ).first()

    if not admin:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if admin.password != password:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    return {
        "message":
        "Login successful",

        "admin": {
            "id":
            admin.id,

            "username":
            admin.username,

            "role":
            admin.role,

            "full_name":
            admin.full_name
        }
    }


# -------------------
# GET ADMINS
# -------------------
@router.get("/admins")
def get_admins(
    db: Session = Depends(get_db)
):

    return db.query(
        Admin
    ).all()


# -------------------
# CREATE ADMIN
# -------------------
@router.post("/admins")
def create_admin(
    payload: dict,
    db: Session = Depends(get_db)
):

    existing_admin = (
        db.query(Admin)
        .filter(
            Admin.username ==
            payload["username"]
        )
        .first()
    )

    if existing_admin:

        raise HTTPException(
            status_code=400,
            detail=
            "Username already exists"
        )

    admin = Admin(
        full_name=
        payload["full_name"],

        username=
        payload["username"],

        password=
        payload["password"],

        role=
        payload.get(
            "role",
            "admin"
        )
    )

    db.add(admin)
    db.commit()

    return {
        "message":
        "Admin created"
    }


# -------------------
# UPDATE ADMIN
# -------------------
@router.put(
    "/admins/{admin_id}"
)
def update_admin(
    admin_id: int,
    payload: dict,
    db: Session = Depends(get_db)
):

    admin = db.query(Admin).filter(
        Admin.id ==
        admin_id
    ).first()

    if not admin:

        raise HTTPException(
            status_code=404,
            detail=
            "Admin not found"
        )

    admin.full_name = (
        payload.get(
            "full_name",
            admin.full_name
        )
    )

    admin.username = (
        payload.get(
            "username",
            admin.username
        )
    )

    admin.role = (
        payload.get(
            "role",
            admin.role
        )
    )

    db.commit()

    return {
        "message":
        "Admin updated"
    }


# -------------------
# DELETE ADMIN
# -------------------
@router.delete(
    "/admins/{admin_id}"
)
def delete_admin(
    admin_id: int,
    db: Session = Depends(get_db)
):

    admin = db.query(Admin).filter(
        Admin.id ==
        admin_id
    ).first()

    if not admin:

        raise HTTPException(
            status_code=404,
            detail=
            "Admin not found"
        )

    db.delete(admin)
    db.commit()

    return {
        "message":
        "Admin deleted"
    }


# -------------------
# CHANGE PASSWORD
# -------------------
@router.put(
    "/admins/change-password"
)
def change_password(
    payload: dict,
    db: Session = Depends(get_db)
):

    username = payload.get(
        "username"
    )

    password = payload.get(
        "password"
    )

    admin = db.query(Admin).filter(
        Admin.username ==
        username
    ).first()

    if not admin:

        raise HTTPException(
            status_code=404,
            detail=
            "Admin not found"
        )

    admin.password = password

    db.commit()

    return {
        "message":
        "Password updated"
    }