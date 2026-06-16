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
    auth,
    esp_recognition
)
Base.metadata.create_all(
    bind=engine
)
db = SessionLocal()

import os
from dotenv import load_dotenv

load_dotenv()

existing_admin = (
    db.query(Admin)
    .filter(
        Admin.username ==
        os.getenv("ADMIN_USERNAME", "admin")
    )
    .first()
)

if not existing_admin:

    admin = Admin(
        username=os.getenv("ADMIN_USERNAME", "admin"),
        password=os.getenv("ADMIN_PASSWORD", "admin123"),
        role=os.getenv("ADMIN_ROLE", "super_admin"),
        full_name=os.getenv("ADMIN_FULL_NAME", "System Admin")
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

@app.get("/esp-test")
def esp_test():
    return {
        "status": "success",
        "message": "ESP Connected"
    }


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

app.include_router(
    esp_recognition.router
)