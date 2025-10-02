from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase once
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def log_attendance(name, status):
    today = datetime.now().strftime("%Y-%m-%d")
    time_now = datetime.now().strftime("%H:%M:%S")

    student_ref = db.collection("attendance").document(name)
    record_ref = student_ref.collection("records").document(today)

    record_ref.set({
        "status": status,
        "time": time_now
    }, merge=True)

    print(f"✅ Attendance logged for {name} on {today} at {time_now}")
