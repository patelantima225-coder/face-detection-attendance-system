# admin_dashboard.py
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import json, os, platform
from datetime import datetime, timedelta
import math

# matplotlib for charts
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# optional excel export
try:
    from openpyxl import Workbook
    HAVE_OPENPYXL = True
except Exception:
    HAVE_OPENPYXL = False

# ------------------------
# Paths & setup
# ------------------------
import sys
# Always anchor the root explicitly
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE_DIR)
USERS_FILE = os.path.join(BASE_DIR, "users.json")
ATTENDANCE_FILE = os.path.join(BASE_DIR, "attendance.json")
EXPORT_DIR = os.path.join(BASE_DIR, "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

BG_IMAGE_PATH = r"C:\gunja\RMS\images\images FD\gunja.jfif"  # optional, kept from your original code

# ------------------------
# JSON helpers
# ------------------------
def load_json(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ------------------------
# Ensure sample files (if empty) so UI shows immediately
# ------------------------
def ensure_sample_files():
    users = load_json(USERS_FILE)
    attendance = load_json(ATTENDANCE_FILE)

    if not users:
        users = {"sampurna321@gmail.com": {
    "name": "sampurna mam",
    "email": "sampurna321@gmail.com",
    "contact": "+911234567890",
    "password": "123",
    "attendance": [
      {
        "date": "2025-09-17",
        "time": "08:10:00",
        "subject": "General",
        "status": "Present"
      },
      {
        "date": "2025-09-16",
        "time": "08:12:00",
        "subject": "General",
        "status": "Present"
      },
      {
        "date": "2025-09-14",
        "time": "23:47:54",
        "subject": "General",
        "status": "Present"
      },
      {
        "date": "2025-09-14",
        "time": "23:48:02",
        "subject": "General",
        "status": "Present"
      }
    ]
  },
  "aj06@gmail.com": {
    "name": "aj",
    "email": "aj06@gmail.com",
    "contact": "+911234567890",
    "password": "234",
    "role": "user",
    "registered_at": "2025-09-14 00:09:17",
    "attendance": [
      {
        "date": "2025-09-17",
        "time": "08:15:00",
        "subject": "General",
        "status": "Late"
      },
      {
        "date": "2025-09-14",
        "time": "23:45:39",
        "subject": "General",
        "status": "Present"
      },
      {
        "date": "2025-09-14",
        "time": "23:45:49",
        "subject": "General",
        "status": "Present"
      }
    ]
  },
  "ritu23@gmail.com": {
    "name": "ritu patel",
    "email": "ritu23@gmail.com",
    "contact": "+911111111111",
    "password": "123",
    "attendance": [
      {
        "date": "2025-09-15",
        "time": "09:45:00",
        "subject": "Python",
        "status": "Present"
      },
      {
        "date": "2025-09-16",
        "time": "10:20:00",
        "subject": "AI",
        "status": "Present"
      },
      {
        "date": "2025-09-17",
        "time": "09:00:33",
        "subject": "os",
        "status": "Present"
      }
    ]
  },
  "antima225@gmail.com": {
    "name": "Admin",
    "email": "antima225@gmail.com",
    "contact": "+911234567890",
    "password": "admin123",
    "role": "admin",
    "registered_at": "2025-09-15 00:00:00",
    "attendance": []
  },
  "bittu23@gmail.com": {
    "name": "bittu",
    "email": "bittu23@gmail.com",
    "contact": "+911234567890",
    "password": "09876",
    "role": "admin",
    "attendance": []
  },
  "sona@321gmail.com": {
    "name": "sonaaaa patel",
    "email": "sona@321gmail.com",
    "contact": "+911234567890",
    "password": "1212",
    "attendance": []
  },
  "ajdon@gmail.com": {
    "name": "ajajan",
    "email": "ajdon@gmail.com",
    "contact": "+916936258514",
    "password": "123",
    "attendance": [
      {
        "date": "2025-09-15",
        "time": "11:00:00",
        "subject": "Maths",
        "status": "Present"
      }
    ]
  },
  "anita@11gmail.com": {
    "name": "anita_patel",
    "email": "anita@11gmail.com",
    "contact": "+911234567890",
    "password": "321",
    "attendance": []
  },
  "basanti34@gmail.com": {
    "name": "basanti",
    "email": "basanti34@gmail.com",
    "contact": "+911234567890",
    "password": "6767",
    "role": "user",
    "registered_at": "2025-09-13 23:44:59",
    "attendance": []
  },
  "patel.antima@225gmail.com": {
    "name": "antima patel",
    "email": "patel.antima@225gmail.com",
    "contact": "+912323232323",
    "password": "123",
    "role": "user",
    "registered_at": "2025-09-15 11:05:48",
    "attendance": []
  },
  "riya@45gmail.com": {
    "name": "riya",
    "email": "riya@45gmail.com",
    "contact": "+911234567890",
    "password": "123",
    "role": "user",
    "registered_at": "2025-09-15 11:47:49",
    "attendance": []
  },
  "riyu24@gmil.com": {
    "name": "riyu",
    "email": "riyu24@gmil.com",
    "contact": "+911234567890",
    "password": "123",
    "role": "user",
    "registered_at": "2025-09-15 11:55:34",
    "attendance": []
  },
  "siya67@gmil.com": {
    "name": "siya",
    "email": "siya67@gmil.com",
    "contact": "+911234567890",
    "password": "098",
    "role": "user",
    "registered_at": "2025-09-15 11:56:15",
    "attendance": []
  },
  "ripo@45gmil.com": {
    "name": "ripo",
    "email": "ripo@45gmil.com",
    "contact": "+911234567890",
    "password": "123",
    "role": "user",
    "registered_at": "2025-09-15 11:58:53",
    "attendance": []
  },
  "jiya23@gmail.com": {
    "name": "jiya",
    "email": "jiya23@gmail.com",
    "contact": "+911234567890",
    "password": "890",
    "role": "user",
    "registered_at": "2025-09-16 19:35:10",
    "attendance": []
  },
  "anuuu34@gmil.com": {
    "name": "sdfgv",
    "email": "anuuu34@gmil.com",
    "contact": "+911234567890",
    "password": "0987",
    "role": "user",
    "registered_at": "2025-09-15 22:54:03",
    "attendance": []
  },
  "piya12@gmail.com": {
    "name": "piya",
    "email": "piya12@gmail.com",
    "contact": "+911234567890",
    "password": "12345",
    "role": "user",
    "registered_at": "2025-09-16 20:45:04",
    "attendance": []
  }
}

        save_json(USERS_FILE, users)

    if not attendance:
        # create some records aligned with users
        attendance = {
            "ritu23@gmail.com": [
                {"date": (datetime.now().date()-timedelta(days=2)).strftime("%Y-%m-%d"), "time":"09:45:00","subject":"Python","status":"Present"},
                {"date": (datetime.now().date()-timedelta(days=1)).strftime("%Y-%m-%d"), "time":"10:20:00","subject":"AI","status":"Present"}
            ],
            "ajdon@gmail.com": [
                {"date": (datetime.now().date()-timedelta(days=2)).strftime("%Y-%m-%d"), "time":"11:00:00","subject":"Maths","status":"Present"}
            ],
            "sampurna321@gmail.com": [
                {"date": (datetime.now().date()-timedelta(days=1)).strftime("%Y-%m-%d"), "time":"08:12:00","subject":"General","status":"Present"},
                {"date": (datetime.now().date()-timedelta(days=0)).strftime("%Y-%m-%d"), "time":"08:10:00","subject":"General","status":"Present"}
            ],
            "aj06@gmail.com": [
                {"date": (datetime.now().date()-timedelta(days=0)).strftime("%Y-%m-%d"), "time":"08:15:00","subject":"General","status":"Late"}
            ]
        }
        save_json(ATTENDANCE_FILE, attendance)

    return load_json(USERS_FILE), load_json(ATTENDANCE_FILE)

# ------------------------
# Utilities to merge attendance placed inside users.json (optional) with central attendance.json
# ------------------------
def merge_attendance(users_map, central_records):
    # If users have "attendance" inside their record, merge into central (without duplicating)
    merged = {k: list(v) for k,v in central_records.items()}
    for email, info in users_map.items():
        if isinstance(info, dict) and info.get("attendance"):
            for rec in info.get("attendance", []):
                merged.setdefault(email, [])
                # naive duplicate check: if same date+time exists skip
                exists = any(r.get("date")==rec.get("date") and r.get("time")==rec.get("time") for r in merged[email])
                if not exists:
                    merged[email].append(rec.copy())
    # Optionally sort each email logs by date/time descending
    for email, logs in merged.items():
        try:
            logs.sort(key=lambda r: (r.get("date",""), r.get("time","")), reverse=False)
        except Exception:
            pass
    return merged

# ------------------------
# Compute stats
# ------------------------
def compute_stats(users_map, central_records, trend_days=14):
    # Merge any attendance fields
    records = merge_attendance(users_map, central_records)

    # treat total students as number of users where role != admin (or all if role missing)
    total_students = sum(1 for e, u in users_map.items() if str(u.get("role","user")).lower() != "admin")
    if total_students == 0:
        total_students = len(users_map)  # fallback

    today_str = datetime.now().date().strftime("%Y-%m-%d")
    present_today = 0
    late_today = 0
    # present/late determination
    for email, user in users_map.items():
        if str(user.get("role","user")).lower() == "admin":
            continue
        user_logs = records.get(email, [])
        # find any record for today - consider latest
        found_today = False
        for r in reversed(user_logs):
            if r.get("date") == today_str:
                found_today = True
                status = r.get("status","Present").lower()
                if status == "present":
                    present_today += 1
                elif status == "late":
                    late_today += 1
                break
    absent_today = max(0, total_students - (present_today + late_today))

    # Trend counts (last trend_days)
    trend_counts = []
    trend_labels = []
    for d in range(trend_days-1, -1, -1):
        day = (datetime.now().date() - timedelta(days=d)).strftime("%Y-%m-%d")
        cnt = 0
        for email, user in users_map.items():
            if str(user.get("role","user")).lower() == "admin":
                continue
            logs = records.get(email, [])
            for r in logs:
                if r.get("date") == day and r.get("status", "Present").lower() in ("present", "late"):
                    cnt += 1
                    break
        trend_counts.append(cnt)
        trend_labels.append(day[5:])  # MM-DD for label

    # Students by class (if missing, create dummy buckets)
    class_counts = {}
    for email, user in users_map.items():
        if str(user.get("role","user")).lower() == "admin":
            continue
        cls = user.get("class")
        if not cls:
            # make a dummy class assignment based on hash to create meaningful buckets
            cls = f"Class-{(abs(hash(email)) % 8) + 1}"
        class_counts[cls] = class_counts.get(cls, 0) + 1

    # Students by gender (if missing, create dummy)
    gender_counts = {}
    for email, user in users_map.items():
        if str(user.get("role","user")).lower() == "admin":
            continue
        g = user.get("gender")
        if not g:
            g = "Female" if (abs(hash(email)) % 2 == 0) else "Male"
        gender_counts[g] = gender_counts.get(g, 0) + 1

    # Top attendants: count present days in last trend_days window
    start_date = (datetime.now().date() - timedelta(days=trend_days-1))
    attendance_list = []
    for email, user in users_map.items():
        if str(user.get("role","user")).lower() == "admin":
            continue
        logs = records.get(email, [])
        present_days = 0
        for r in logs:
            try:
                d = datetime.strptime(r.get("date",""), "%Y-%m-%d").date()
            except Exception:
                continue
            if start_date <= d <= datetime.now().date():
                if r.get("status","present").lower() in ("present", "late"):
                    present_days += 1
        pct = (present_days / trend_days) * 100 if trend_days > 0 else 0
        attendance_list.append((user.get("name", email), f"{pct:.1f}%", present_days))
    attendance_list.sort(key=lambda x: (-float(x[1].rstrip("%")), -x[2]))

    # Weekly absent counts (Mon..Sun) -> count how many students were absent that day (no present/late record -> absent)
    weekly_absent = {'Mon':0,'Tue':0,'Wed':0,'Thu':0,'Fri':0,'Sat':0,'Sun':0}
    for d in range(6, -1, -1):
        day = datetime.now().date() - timedelta(days=d)
        day_str = day.strftime("%Y-%m-%d")
        weekday = day.strftime("%a")
        absent_count_for_day = 0
        for email, user in users_map.items():
            if str(user.get("role","user")).lower() == "admin":
                continue
            logs = records.get(email, [])
            had_present = False
            for r in logs:
                if r.get("date") == day_str and r.get("status","Present").lower() in ("present","late"):
                    had_present = True
                    break
            if not had_present:
                absent_count_for_day += 1
        # Map weekday to our key (Mon/Tue/..)
        key = weekday
        weekly_absent[key] = absent_count_for_day

    # Total logs count (for avg attendance calc)
    total_logs = sum(len(v) for v in records.values())

    stats = {
        "total_students": total_students,
        "present_today": present_today,
        "late_today": late_today,
        "absent_today": absent_today,
        "trend_counts": trend_counts,
        "trend_labels": trend_labels,
        "class_counts": class_counts,
        "gender_counts": gender_counts,
        "top_attendants": attendance_list[:6],
        "weekly_absent": weekly_absent,
        "total_logs": total_logs,
        "records": records
    }
    return stats

# ------------------------
# GUI Setup
# ------------------------
root = tk.Tk()
root.title("Admin Panel - Attendance System")
root.geometry("1200x700")
root.resizable(False, False)

# background image if exists
if os.path.exists(BG_IMAGE_PATH):
    try:
        bg_image = Image.open(BG_IMAGE_PATH)
        bg_image = bg_image.resize((1200,700), Image.Resampling.LANCZOS)
        bg_photo = ImageTk.PhotoImage(bg_image)
        bg_label = tk.Label(root, image=bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    except Exception:
        root.configure(bg="#ecf0f1")
else:
    root.configure(bg="#ecf0f1")

menu_frame = tk.Frame(root, bg="#2c3e50", width=230)
menu_frame.pack(side="left", fill="y")

content_frame = tk.Frame(root, bg="#f9f9f9")
content_frame.pack(side="right", fill="both", expand=True)

def clear_content():
    for w in content_frame.winfo_children():
        w.destroy()

# ------------------------
# Home page with charts & cards
# ------------------------
def show_home():
    clear_content()
    users_map, central_records = ensure_sample_files()
    users_map = load_json(USERS_FILE)
    central_records = load_json(ATTENDANCE_FILE)
    stats = compute_stats(users_map, central_records, trend_days=14)

    # Title
    title = tk.Label(content_frame, text="📊 Admin Dashboard Overview",
                     font=("Segoe UI", 22, "bold"), bg="#f9f9f9", fg="#2c3e50")
    title.pack(pady=20)

    # Cards row
    card_frame = tk.Frame(content_frame, bg="#f9f9f9")
    card_frame.pack(pady=10)

    def create_card(parent, label_text, value_text, color):
        card = tk.Frame(parent, bg=color, width=220, height=110, relief="raised", bd=2)
        card.pack(side="left", padx=18)
        tk.Label(card, text=label_text, font=("Segoe UI", 12, "bold"), bg=color, fg="white").pack(pady=6)
        tk.Label(card, text=value_text, font=("Segoe UI", 20, "bold"), bg=color, fg="white").pack()

    create_card(card_frame, "Total Students", str(stats["total_students"]), "#3498db")
    create_card(card_frame, "Present Today", str(stats["present_today"]), "#2ecc71")
    create_card(card_frame, "Absent Today", str(stats["absent_today"]), "#e74c3c")
    create_card(card_frame, "Late Students", str(stats["late_today"]), "#f39c12")

    # Middle charts frame
    charts_frame = tk.Frame(content_frame, bg="#f9f9f9")
    charts_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Left: Attendance trend (line)
    fig1, ax1 = plt.subplots(figsize=(4,3))
    ax1.plot(range(1, len(stats["trend_counts"])+1), stats["trend_counts"], marker="o")
    ax1.set_title("Total Attendance Report")
    ax1.set_xlabel("Days")
    ax1.set_ylabel("Students Present")
    ax1.set_xticks(range(1, len(stats["trend_labels"])+1))
    ax1.set_xticklabels(stats["trend_labels"], rotation=30, fontsize=8)
    canvas1 = FigureCanvasTkAgg(fig1, master=charts_frame)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side="left", padx=10)

    # Right: Students by class (bar)
    fig2, ax2 = plt.subplots(figsize=(4,3))
    classes = list(stats["class_counts"].keys())
    class_vals = list(stats["class_counts"].values())
    ax2.bar(classes, class_vals)
    ax2.set_title("Students by Class")
    ax2.set_xticklabels(classes, rotation=30, fontsize=8)
    canvas2 = FigureCanvasTkAgg(fig2, master=charts_frame)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side="left", padx=10)

    # Bottom frame: gender pie, top attendants, weekly radar
    bottom_frame = tk.Frame(content_frame, bg="#f9f9f9")
    bottom_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Pie: gender
    fig3, ax3 = plt.subplots(figsize=(3,3))
    genders = list(stats["gender_counts"].keys())
    gender_vals = list(stats["gender_counts"].values())
    ax3.pie(gender_vals, labels=genders, autopct="%1.1f%%", startangle=90)
    ax3.set_title("Students by Gender")
    canvas3 = FigureCanvasTkAgg(fig3, master=bottom_frame)
    canvas3.draw()
    canvas3.get_tk_widget().pack(side="left", padx=12)

    # Top attendants table
    right_frame = tk.Frame(bottom_frame, bg="#f9f9f9")
    right_frame.pack(side="left", padx=20, fill="y")

    tk.Label(right_frame, text="🏅 Top Attendants", font=("Segoe UI", 16, "bold"),
             bg="#f9f9f9", fg="#2c3e50").pack(anchor="w")

    tree = ttk.Treeview(right_frame, columns=("Name","%","Days"), show="headings", height=6)
    tree.heading("Name", text="Name")
    tree.heading("%", text="Attendance %")
    tree.heading("Days", text="Days")
    tree.column("Name", width=160)
    tree.column("%", width=80, anchor="center")
    tree.column("Days", width=60, anchor="center")
    tree.pack(pady=8)

    for row in stats["top_attendants"]:
        tree.insert("", "end", values=row)

    # Radar chart: weekly absent
    fig4 = plt.figure(figsize=(3,3))
    ax4 = fig4.add_subplot(111, polar=True)
    labels = list(stats["weekly_absent"].keys())
    stats_vals = list(stats["weekly_absent"].values())
    angles = [n / float(len(labels)) * 2 * math.pi for n in range(len(labels))]
    stats_vals_extended = stats_vals + stats_vals[:1]
    angles_extended = angles + angles[:1]
    ax4.plot(angles_extended, stats_vals_extended, "o-", linewidth=2)
    ax4.fill(angles_extended, stats_vals_extended, alpha=0.25)
    ax4.set_xticks(angles)
    ax4.set_xticklabels(labels)
    ax4.set_title("Weekly Absent")
    canvas4 = FigureCanvasTkAgg(fig4, master=bottom_frame)
    canvas4.draw()
    canvas4.get_tk_widget().pack(side="left", padx=10)

# ------------------------
# Users page (table + export)
# ------------------------
def show_users():
    clear_content()
    users_map = load_json(USERS_FILE)

    lbl = tk.Label(content_frame, text="👥 Registered Users", font=("Segoe UI", 18, "bold"), bg="#f9f9f9")
    lbl.pack(pady=10)

    tree = ttk.Treeview(content_frame,
                        columns=("ID", "Name", "Email", "Contact", "Role", "Registered At"),
                        show="headings")
    for col in ("ID", "Name", "Email", "Contact", "Role", "Registered At"):
        tree.heading(col, text=col)
        tree.column(col, width=160, anchor="center")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    for idx, (email, details) in enumerate(users_map.items(), start=1):
        tree.insert("", "end", values=(
            idx, details.get("name", ""), email,
            details.get("contact", ""), details.get("role", "user"),
            details.get("registered_at", "")
        ))

    def export_users_excel():
        if not HAVE_OPENPYXL:
            messagebox.showerror("Missing Library", "openpyxl not installed. Install with `pip install openpyxl`")
            return
        wb = Workbook()
        ws = wb.active
        ws.title = "Users"
        ws.append(["ID", "Name", "Email", "Contact", "Role", "Registered At"])
        for idx, (email, details) in enumerate(users_map.items(), start=1):
            ws.append([
                idx, details.get("name", ""), email,
                details.get("contact", ""), details.get("role", "user"),
                details.get("registered_at", "")
            ])
        file_path = os.path.join(EXPORT_DIR, "users.xlsx")
        wb.save(file_path)
        try:
            if platform.system() == "Windows":
                os.startfile(file_path)
            else:
                messagebox.showinfo("Saved", f"Saved to {file_path}")
        except Exception:
            messagebox.showinfo("Saved", f"Saved to {file_path}")

    tk.Button(content_frame, text="⬇ Export to Excel", bg="#27ae60", fg="white",
              font=("Segoe UI", 12, "bold"), command=export_users_excel).pack(pady=10)

# ------------------------
# Attendance records page
# ------------------------
def show_attendance():
    clear_content()
    central_records = load_json(ATTENDANCE_FILE)
    users_map = load_json(USERS_FILE)
    merged_records = merge_attendance(users_map, central_records)

    lbl = tk.Label(content_frame, text="📑 Attendance Records", font=("Segoe UI", 18, "bold"), bg="#f9f9f9")
    lbl.pack(pady=10)

    search_frame = tk.Frame(content_frame, bg="#f9f9f9")
    search_frame.pack(pady=5)

    tk.Label(search_frame, text="Email:", font=("Segoe UI", 12), bg="#f9f9f9").pack(side="left")
    search_entry = tk.Entry(search_frame, font=("Segoe UI", 12))
    search_entry.pack(side="left", padx=5)

    tk.Label(search_frame, text="Last N days:", font=("Segoe UI", 12), bg="#f9f9f9").pack(side="left")
    days_entry = tk.Entry(search_frame, width=10, font=("Segoe UI", 12))
    days_entry.pack(side="left", padx=5)

    tree = ttk.Treeview(content_frame,
                        columns=("ID", "Name", "Email", "Date", "Time", "Subject", "Status"),
                        show="headings")
    for col in ("ID", "Name", "Email", "Date", "Time", "Subject", "Status"):
        tree.heading(col, text=col)
        tree.column(col, width=140, anchor="center")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    def load_data(filter_email="", last_days=""):
        for row in tree.get_children():
            tree.delete(row)

        row_id = 1
        for email, details in users_map.items():
            if filter_email and filter_email.lower() not in email.lower():
                continue
            user_name = details.get("name", "Unknown")
            logs = merged_records.get(email, [])

            # Filter by last N days
            if last_days.isdigit():
                cutoff = datetime.now() - timedelta(days=int(last_days))
                filtered_logs = []
                for r in logs:
                    dt_str = r.get("date", "") + " " + r.get("time", "")
                    try:
                        # robust parse attempts
                        dt = datetime.strptime(r.get("date","") + " " + r.get("time",""), "%Y-%m-%d %H:%M:%S")
                    except Exception:
                        try:
                            dt = datetime.strptime(r.get("date","") + " " + r.get("time",""), "%Y-%m-%d %H:%M")
                        except Exception:
                            continue
                    if dt >= cutoff:
                        filtered_logs.append(r)
                logs = filtered_logs

            if logs:
                for entry in logs:
                    tree.insert("", "end", values=(
                        row_id, user_name, email,
                        entry.get("date", ""), entry.get("time", ""),
                        entry.get("subject", ""), entry.get("status", "Present")))
                    row_id += 1
            else:
                tree.insert("", "end", values=(row_id, user_name, email, "-", "-", "-", "-"))
                row_id += 1

    def do_search():
        load_data(search_entry.get().strip(), days_entry.get().strip())

    def reset_search():
        search_entry.delete(0, tk.END)
        days_entry.delete(0, tk.END)
        load_data()

    def mark_attendance():
        email = search_entry.get().strip()
        if email not in users_map:
            messagebox.showerror("Error", "Enter a valid user email to mark attendance")
            return
        timestamp = datetime.now()
        record = {
            "date": timestamp.strftime("%Y-%m-%d"),
            "time": timestamp.strftime("%H:%M:%S"),
            "subject": "General",
            "status": "Present"
        }
        central_records.setdefault(email, []).append(record)
        save_json(ATTENDANCE_FILE, central_records)
        messagebox.showinfo("Success", f"Attendance marked for {email}")
        load_data(email)

    tk.Button(search_frame, text="🔍 Search", bg="#2980b9", fg="white",
              font=("Segoe UI", 10, "bold"), command=do_search).pack(side="left", padx=5)
    tk.Button(search_frame, text="⟳ Reset", bg="#95a5a6", fg="white",
              font=("Segoe UI", 10, "bold"), command=reset_search).pack(side="left", padx=5)
    tk.Button(search_frame, text="✅ Mark Attendance", bg="#27ae60", fg="white",
              font=("Segoe UI", 10, "bold"), command=mark_attendance).pack(side="left", padx=5)

    def export_attendance_excel():
        if not HAVE_OPENPYXL:
            messagebox.showerror("Missing Library", "openpyxl not installed. Install with `pip install openpyxl`")
            return
        wb = Workbook()
        ws = wb.active
        ws.title = "Attendance"
        ws.append(["ID", "Name", "Email", "Date", "Time", "Subject", "Status"])

        row_id = 1
        for email, details in users_map.items():
            user_name = details.get("name", "Unknown")
            logs = merged_records.get(email, [])
            if logs:
                for entry in logs:
                    ws.append([row_id, user_name, email,
                               entry.get("date", ""), entry.get("time", ""),
                               entry.get("subject", ""), entry.get("status", "Present")])
                    row_id += 1
        file_path = os.path.join(EXPORT_DIR, "attendance.xlsx")
        wb.save(file_path)
        try:
            if platform.system() == "Windows":
                os.startfile(file_path)
            else:
                messagebox.showinfo("Saved", f"Saved to {file_path}")
        except Exception:
            messagebox.showinfo("Saved", f"Saved to {file_path}")

    load_data()

# ------------------------
# Attendance % page
# ------------------------
def show_percentage():
    clear_content()
    central_records = load_json(ATTENDANCE_FILE)
    users_map = load_json(USERS_FILE)
    merged_records = merge_attendance(users_map, central_records)

    lbl = tk.Label(content_frame, text="📈 Attendance Percentage", font=("Segoe UI", 18, "bold"), bg="#f9f9f9")
    lbl.pack(pady=10)

    tree = ttk.Treeview(content_frame, columns=("ID", "Name", "Email", "Attendance %"), show="headings")
    for col in ("ID", "Name", "Email", "Attendance %"):
        tree.heading(col, text=col)
        tree.column(col, width=220, anchor="center")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    TOTAL_CLASSES = 14  # using the same window as trend_days
    for idx, (email, details) in enumerate(users_map.items(), start=1):
        if str(details.get("role","user")).lower() == "admin":
            continue
        attended = 0
        logs = merged_records.get(email, [])
        for r in logs:
            try:
                d = datetime.strptime(r.get("date",""), "%Y-%m-%d").date()
            except Exception:
                continue
            # consider last TOTAL_CLASSES days window
            if d >= (datetime.now().date() - timedelta(days=TOTAL_CLASSES-1)):
                if r.get("status","present").lower() in ("present","late"):
                    attended += 1
        percentage = (attended / TOTAL_CLASSES) * 100 if TOTAL_CLASSES > 0 else 0
        tree.insert("", "end", values=(idx, details.get("name", ""), email, f"{percentage:.1f}%"))

# ------------------------
# Menu
# ------------------------
menu_buttons = [
    ("🏠 Home", show_home),
    ("👥 Users", show_users),
    ("📑 Attendance", show_attendance),
    ("📈 Attendance %", show_percentage),
    ("❌ Logout", root.destroy),
]

for text, cmd in menu_buttons:
    btn = tk.Button(menu_frame, text=text, font=("Segoe UI", 14, "bold"),
                    bg="#34495e", fg="white", relief="flat", command=cmd)
    btn.pack(fill="x", pady=6, ipady=10)

# Start
show_home()
root.mainloop()
