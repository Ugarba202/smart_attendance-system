from fastapi import (
    APIRouter,
    Depends,
    Query
)

from sqlalchemy.orm import Session
from datetime import date

from app.database import (
    get_db
)

from app.models.attendance import (
    Attendance
)

router = APIRouter()


@router.get("/attendance")
def get_attendance(
    db: Session = Depends(get_db),

    search: str = Query(
        default=""
    ),

    selected_date: str = Query(
        default=""
    )
):

    query = db.query(
        Attendance
    )

    # Search filter
    if search:

        query = query.filter(
            Attendance.user_name
            .ilike(
                f"%{search}%"
            )
        )

    # Date filter
    if selected_date:

        query = query.filter(
            Attendance.date ==
            selected_date
        )

    attendance = (
        query
        .order_by(
            Attendance.id.desc()
        )
        .all()
    )

    return attendance