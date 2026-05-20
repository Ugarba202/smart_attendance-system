# Smart Attendance System

AI-powered smart attendance system using:

- Python
- OpenCV
- ESP32-CAM
- Face Recognition
- Attendance Logging

## Features

- Real-time face detection
- Face registration system
- Multi-user recognition
- Attendance logging
- Duplicate attendance prevention
- Local AI recognition engine

---

# Project Structure

AI/
│
├── datasets/
├── attendance/
├── recognition/
├── registration/
├── models/
└── utils/

---

# Technologies Used

- Python 3.11
- OpenCV
- LBPH Face Recognizer
- NumPy
- ESP32-CAM (upcoming)
- FastAPI (upcoming)

---

# Current Progress

✅ Face Detection  
✅ User Registration  
✅ Dataset Collection  
✅ AI Model Training  
✅ Real-Time Face Recognition  
✅ Attendance Logging  

---

# Upcoming Features

- FastAPI Backend
- PostgreSQL Database
- Dashboard
- ESP32-CAM Integration
- Real-time Attendance Analytics

---

# Setup

## Create Virtual Environment

```bash
python3.11 -m venv venv
```

## Activate Virtual Environment

```bash
source venv/bin/activate
```

## Install Dependencies

```bash
pip install opencv-python opencv-contrib-python numpy
```

---

# Run Face Registration

```bash
cd AI/registration
python register_user.py
```

---

# Train Recognition Model

```bash
cd AI/recognition
python train_model.py
```

---

# Run Recognition System

```bash
cd AI/recognition
python recognize_face.py
```

---

# Author

Usman Umar Garba