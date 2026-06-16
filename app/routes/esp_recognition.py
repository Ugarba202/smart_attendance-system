from fastapi import APIRouter, Request, Depends
import os
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.services.recognize_service import recognize_face
from app.services.attendance_service import mark_attendance

router = APIRouter()

@router.post("/esp-recognize")
async def esp_recognize(
    request: Request,
    db: Session = Depends(get_db)
):
    image_bytes = await request.body()
    
    temp_folder = "temp_uploads"
    os.makedirs(temp_folder, exist_ok=True)
    image_path = os.path.join(temp_folder, "esp_capture.jpg")
    
    with open(image_path, "wb") as f:
        f.write(image_bytes)
        
    # Verify image has content
    if len(image_bytes) == 0:
        return {
            "status": "error",
            "message": "Empty image received",
            "attendance_marked": False
        }
        
    try:
        # AI recognition
        result = recognize_face(image_path)
        
        if result["status"] != "recognized":
            return {
                "status": "error",
                "message": result.get("message", "Face not recognized"),
                "attendance_marked": False
            }
            
        recognized_label = result["full_name"].strip().lower()
        
        # search registration number
        user = (
            db.query(User)
            .filter(User.registration_number.ilike(recognized_label))
            .first()
        )
        
        if not user:
            return {
                "status": "error",
                "message": f"User not found: {recognized_label}",
                "attendance_marked": False
            }
            
        # mark attendance
        attendance_result = mark_attendance(db, user.full_name)
        
        return {
            "status": "recognized",
            "message": attendance_result["message"],
            "attendance_marked": attendance_result["attendance_marked"],
            "user_name": user.full_name
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "attendance_marked": False
        }
