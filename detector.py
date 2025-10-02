# detector.py
import firebase_admin
from firebase_admin import credentials, firestore

# 🔹 Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")  # Path to your Firebase key
    firebase_admin.initialize_app(cred)

db = firestore.client()

# 🔹 Define expected working days (for testing you can hardcode)
expected_days = {"2025-09-25", "2025-09-26", "2025-09-27"}

def detect_anomalies():
    attendance_map = {}

    # 🔹 Load attendance into a Python dictionary
    students_ref = db.collection("attendance")
    students = students_ref.stream()

    for student in students:
        student_id = student.id
        records_ref = students_ref.document(student_id).collection("records").stream()
        days = [rec.id for rec in records_ref]
        attendance_map[student_id] = days

    print("📊 Attendance Map:", attendance_map)

    # 🔹 Step 1: Detect missing attendance
    for student, days in attendance_map.items():
        day_set = set(days)
        missing = expected_days - day_set
        if missing:
            print(f"⚠️ {student} missing attendance on: {missing}")

    # 🔹 Step 2: Detect duplicate records
        if len(days) != len(day_set):
            print(f"⚠️ {student} has duplicate records")

    # 🔹 Step 3: Detect late entries
        records_ref = db.collection("attendance").document(student).collection("records").stream()
        for rec in records_ref:
            rec_data = rec.to_dict()
            if "time" in rec_data and rec_data["time"] > "10:00:00":  # assuming 24-hour format
                print(f"⏰ {student} was late on {rec.id} at {rec_data['time']}")

if __name__ == "__main__":
    detect_anomalies()
