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

@router.get(
    "/dashboard/analytics"
)
def get_analytics(
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
            Attendance.date ==
            today
        )
        .count()
    )

    absent_today = (
        total_users -
        present_today
    )

    attendance = (
        db.query(Attendance)
        .all()
    )

    weekly_data = {}

    for item in attendance:

        day = str(
            item.date
        )

        weekly_data[day] = (
            weekly_data.get(
                day,
                0
            ) + 1
        )

    weekly_chart = []

    for key, value in (
        weekly_data.items()
    ):

        weekly_chart.append({
            "date": key,
            "attendance":
            value
        })

    return {

        "pie_chart": [
            {
                "name":
                "Present",

                "value":
                present_today
            },

            {
                "name":
                "Absent",

                "value":
                absent_today
            }
        ],

        "weekly_chart":
        weekly_chart
    }