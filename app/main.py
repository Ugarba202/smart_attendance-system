from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import (
    engine,
    Base,
    SessionLocal
)

# Import models BEFORE create_all
from app.models.user import User
from app.models.attendance import Attendance
from app.models.admin import Admin

from app.routes import (
    attendance,
    dashboard,
    user,
    recognition,
    export,
    auth
)
Base.metadata.create_all(
    bind=engine
)
db = SessionLocal()

existing_admin = (
    db.query(Admin)
    .filter(
        Admin.username ==
        "admin"
    )
    .first()
)

if not existing_admin:

    admin = Admin(
        username="admin",
        password="admin123",
        role="super_admin",
        full_name="System Admin"
    )

    db.add(admin)
    db.commit()

db.close()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(
    user.router
)

app.include_router(
    attendance.router
)

app.include_router(
    recognition.router
)

app.include_router(
    dashboard.router
)

app.include_router(
    export.router
)

app.include_router(
    auth.router
)