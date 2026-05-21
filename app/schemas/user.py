from pydantic import BaseModel


class UserCreate(BaseModel):

    full_name: str
    department: str | None = None