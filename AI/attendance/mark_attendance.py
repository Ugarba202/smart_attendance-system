import csv
import os
from datetime import datetime

# Base directory
BASE_DIR = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        ".."
    )
)

# Attendance file path
attendance_file = os.path.join(
    BASE_DIR,
    "attendance",
    "attendance_log.csv"
)

def mark_attendance(user_name):

    today_date = datetime.now().strftime("%Y-%m-%d")

    current_time = datetime.now().strftime("%I:%M:%S %p")

    # Read existing attendance
    existing_records = []

    with open(attendance_file, "r") as file:

        reader = csv.reader(file)

        for row in reader:
            existing_records.append(row)

    # Check duplicates
    for row in existing_records:

        if len(row) < 2:
            continue

        recorded_name = row[0]
        recorded_date = row[1]

        if (
            recorded_name == user_name and
            recorded_date == today_date
        ):

            print(
                f"{user_name} already marked today."
            )

            return False

    # Save new attendance
    with open(attendance_file, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            user_name,
            today_date,
            current_time,
            "Present"
        ])

    print(
        f"Attendance marked for {user_name}"
    )

    return True