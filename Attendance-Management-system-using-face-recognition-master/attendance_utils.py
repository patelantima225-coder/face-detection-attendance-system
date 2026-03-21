import json
import os
import datetime

USER_DB_FILE = "users.json"

# Load users
def load_users():
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, "r") as f:
            return json.load(f)
    return {}

# Save users
def save_users(users_db):
    with open(USER_DB_FILE, "w") as f:
        json.dump(users_db, f, indent=4)

# Mark attendance
def mark_attendance(email, subject="General"):
    users_db = load_users()
    today = datetime.date.today().strftime("%Y-%m-%d")
    now = datetime.datetime.now().strftime("%H:%M:%S")

    if email in users_db:
        if "attendance" not in users_db[email]:
            users_db[email]["attendance"] = []

        users_db[email]["attendance"].append({
            "date": today,
            "time": now,
            "subject": subject,
            "status": "Present"
        })

        save_users(users_db)
        print(f"Attendance marked for {email} on {today}")
        return True
    else:
        print("User not found!")
        return False
