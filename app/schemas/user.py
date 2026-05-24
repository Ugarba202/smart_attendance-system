from pydantic import BaseModel


class UserResponse(BaseModel):
    id: int
    full_name: str
    registration_number: str
    department: str
    image_path: str
    status: str

    class Config:
        from_attributes = True