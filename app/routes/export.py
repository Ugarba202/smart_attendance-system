from fastapi import (
    APIRouter,
    Depends
)

from fastapi.responses import (
    FileResponse
)

from sqlalchemy.orm import (
    Session
)

from datetime import (
    date,
    timedelta
)

from openpyxl import Workbook

from app.database import (
    get_db
)

from app.models.attendance import (
    Attendance
)

import os


router = APIRouter()


@router.get(
    "/attendance/export/{period}"
)
def export_attendance(
    period: str,
    db: Session = Depends(get_db)
):

    today = date.today()

    query = db.query(
        Attendance
    )

    if period == "daily":

        query = query.filter(
            Attendance.date ==
            today
        )

    elif period == "weekly":

        week_ago = (
            today -
            timedelta(days=7)
        )

        query = query.filter(
            Attendance.date >=
            week_ago
        )

    elif period == "monthly":

        month_ago = (
            today -
            timedelta(days=30)
        )

        query = query.filter(
            Attendance.date >=
            month_ago
        )

    attendance = query.all()

    workbook = Workbook()

    sheet = workbook.active
    sheet.title = (
        "Attendance Report"
    )

    headers = [
        "Student Name",
        "Date",
        "Time",
        "Status"
    ]

    sheet.append(headers)

    for record in attendance:

        sheet.append([
            record.user_name,
            str(record.date),
            str(record.time),
            record.status
        ])

    os.makedirs(
        "exports",
        exist_ok=True
    )

    file_path = (
        f"exports/"
        f"attendance_"
        f"{period}.xlsx"
    )

    workbook.save(
        file_path
    )

    return FileResponse(
        path=file_path,
        filename=
        f"attendance_{period}.xlsx",
        media_type=
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )