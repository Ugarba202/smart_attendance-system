from datetime import (
    datetime,
    date
)

from sqlalchemy.orm import Session

from app.models.attendance import (
    Attendance
)


def mark_attendance(
    db: Session,
    user_name: str
):

    today = date.today()

    # Check duplicate attendance
    existing_attendance = (
        db.query(Attendance)
        .filter(
            Attendance.user_name
            == user_name,

            Attendance.date
            == today
        )
        .first()
    )

    # Already marked
    if existing_attendance:

        return {
            "attendance_marked":
            False,

            "message":
            "Attendance already marked"
        }

    # Create attendance record
    attendance = Attendance(
        user_name=user_name,
        date=today,
        time=datetime.now().time(),
        status="Present"
    )

    db.add(attendance)
    db.commit()

    return {
        "attendance_marked":
        True,

        "message":
        "Attendance marked"
    }