# Smart Attendance System (AI + ESP32)

An AI-powered smart attendance system using facial recognition, FastAPI, SQLite, and ESP32-CAM.

## Features

- Face registration
- Face recognition
- Automatic attendance marking
- Duplicate attendance prevention
- User management
- AI model training
- Attendance history tracking
- REST API backend
- ESP32-CAM integration (coming soon)

---

## Tech Stack

### Backend
- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn

### AI / Computer Vision
- OpenCV
- LBPH Face Recognition
- NumPy

### Hardware
- ESP32-CAM (planned)

---

## Project Structure

```txt
backend-api/
│
├── AI/
│   ├── datasets/
│   ├── models/
│   ├── recognition/
│   └── attendance/
│
├── app/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── database.py
│   └── main.py
│
├── requirements.txt
├── .gitignore
└── README.md
Installation
Clone Repository
git clone <your-repo-url>
cd backend-api
Create Virtual Environment
python3.11 -m venv venv

Activate:

Linux/macOS:

source venv/bin/activate

Windows:

venv\Scripts\activate
Install Dependencies
pip install -r requirements.txt
Run Server
uvicorn app.main:app --reload

Server:

http://127.0.0.1:8000

Swagger Docs:

http://127.0.0.1:8000/docs
API Endpoints
User APIs
Method	Endpoint	Description
POST	/register-user	Register user
GET	/users	Get users
DELETE	/users/{id}	Delete user
Recognition APIs
Method	Endpoint	Description
POST	/recognize	Recognize face
POST	/train-model	Retrain AI model
Attendance APIs
Method	Endpoint	Description
GET	/attendance	Attendance history
System Workflow
Register User
      ↓
Upload Face Image
      ↓
Train AI Model
      ↓
Recognition
      ↓
Attendance Marking
      ↓
Dashboard View
Future Improvements
Admin dashboard UI
Analytics dashboard
ESP32-CAM integration
Real-time notifications
Cloud deployment
Author

Usman Umar Garba
Software Engineering | Mobile Engineer | Bitcoin & Lightning Enthusiast