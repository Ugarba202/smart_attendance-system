from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.attendance import Attendance

router = APIRouter()


@router.get("/attendance")
def get_attendance(
    db: Session = Depends(get_db)
):

    attendance_records = (
        db.query(Attendance)
        .order_by(Attendance.id.desc())
        .all()
    )

    return attendance_records