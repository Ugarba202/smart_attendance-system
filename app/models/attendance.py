from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time
)

from app.database import Base


class Attendance(Base):

    __tablename__ = "attendance"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_name = Column(
        String,
        nullable=False
    )

    date = Column(
        Date
    )

    time = Column(
        Time
    )

    status = Column(
        String,
        default="Present"
    )