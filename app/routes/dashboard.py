from fastapi import (
    APIRouter,
    Depends
)

from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db

from app.models.user import User
from app.models.attendance import Attendance

router = APIRouter()


@router.get("/dashboard/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db)
):

    total_users = (
        db.query(User)
        .count()
    )

    today = date.today()

    present_today = (
        db.query(Attendance)
        .filter(
            Attendance.date == today
        )
        .count()
    )

    absent_today = max(
        total_users -
        present_today,
        0
    )

    return {
        "total_users":
        total_users,

        "present_today":
        present_today,

        "absent_today":
        absent_today,

        "model_status":
        "Ready"
    }


@router.get(
    "/dashboard/recent-attendance"
)
def get_recent_attendance(
    db: Session = Depends(get_db)
):

    attendance_records = (
        db.query(Attendance)
        .order_by(
            Attendance.id.desc()
        )
        .limit(10)
        .all()
    )

    result = []

    for item in attendance_records:

        user = db.query(User).filter(
            User.full_name ==
            item.user_name
        ).first()

        result.append({

            "full_name":
            item.user_name,

            "department":
            user.department
            if user else "Unknown",

            "time":
            str(item.time),

            "status":
            item.status
        })

    return result