from fastapi import FastAPI

from app.database import (
    Base,
    engine
)

from app.routes.user import (
    router as user_router
)

from app.routes.recognition import (
    router as recognition_router
)

from app.routes.attendance import (
    router as attendance_router
)

Base.metadata.create_all(
    bind=engine
)

app = FastAPI()


@app.get("/")
def home():

    return {
        "message":
        "Smart Attendance API"
    }


app.include_router(user_router)
app.include_router(recognition_router)
app.include_router(attendance_router)