import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import json, os, datetime, subprocess
from openpyxl import Workbook

import sys

# Change to the root directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE_DIR)

# ========================
# File Paths
# ========================
USERS_FILE = "users.json"
ATTENDANCE_FILE = "attendance.json"
BG_IMAGE_PATH = r"C:\gunja\RMS\images\images FD\gunja.jfif"
EXPORT_DIR = os.path.join(os.getcwd(), "exports")
os.makedirs(EXPORT_DIR, exist_ok=True)

# ========================
# Utility Functions
# ========================
def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

# ========================
# Attendance Marking
# ========================
def mark_attendance(email, subject="General"):
    users = load_json(USERS_FILE)
    if email not in users:
        messagebox.showerror("Error", "User not found in users.json")
        return False

    records = load_json(ATTENDANCE_FILE)
    today = datetime.date.today().strftime("%Y-%m-%d")
    now = datetime.datetime.now().strftime("%H:%M:%S")

    if email not in records:
        records[email] = []

    records[email].append({
        "date": today,
        "time": now,
        "subject": subject,
        "status": "Present"
    })

    save_json(ATTENDANCE_FILE, records)
    messagebox.showinfo("Success", f"Attendance marked for {email}")
    return True

# ========================
# Features
# ========================
def open_users_record():
    users = load_json(USERS_FILE)

    win = tk.Toplevel(root)
    win.title("Users Record")
    win.geometry("750x450")
    win.configure(bg="#f4f6f7")

    tree = ttk.Treeview(win, columns=("ID","Name","Email","Contact","Role","Registered At"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Email", text="Email")
    tree.heading("Contact", text="Contact")
    tree.heading("Role", text="Role")
    tree.heading("Registered At", text="Registered At")
    tree.column("ID", width=50, anchor="center")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    for idx, (email, details) in enumerate(users.items(), start=1):
        tree.insert("", "end", values=(
            idx, 
            details.get("name",""),
            email,
            details.get("contact",""),
            details.get("role","user"),
            details.get("registered_at","")
        ))

def open_attendance_summary():
    records = load_json(ATTENDANCE_FILE)
    users = load_json(USERS_FILE)

    win = tk.Toplevel(root)
    win.title("Attendance Summary")
    win.geometry("650x450")
    win.configure(bg="#f4f6f7")

    tree = ttk.Treeview(win, columns=("ID","Name","Email","Total Present","Attendance %"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Email", text="Email")
    tree.heading("Total Present", text="Total Present")
    tree.heading("Attendance %", text="Attendance %")
    tree.column("ID", width=50, anchor="center")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    total_classes = max([len(v) for v in records.values()], default=1)

    for idx, (email, details) in enumerate(users.items(), start=1):
        attended = len(records.get(email, []))
        percentage = (attended / total_classes) * 100 if total_classes > 0 else 0
        tree.insert("", "end", values=(idx, details.get("name",""), email, attended, f"{percentage:.1f}%"))

def open_search_attendance():
    records = load_json(ATTENDANCE_FILE)
    users = load_json(USERS_FILE)

    win = tk.Toplevel(root)
    win.title("Search Attendance")
    win.geometry("850x500")
    win.configure(bg="#f4f6f7")

    tk.Label(win, text="Enter Email:", font=("Segoe UI", 12)).pack(pady=5)
    email_entry = tk.Entry(win, font=("Segoe UI", 12))
    email_entry.pack(pady=5)

    tree = ttk.Treeview(win, columns=("ID","Date","Time","Subject","Status"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Date", text="Date")
    tree.heading("Time", text="Time")
    tree.heading("Subject", text="Subject")
    tree.heading("Status", text="Status")
    tree.column("ID", width=50, anchor="center")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    def search():
        for row in tree.get_children():
            tree.delete(row)
        email = email_entry.get().strip()
        if email in records:
            for idx, entry in enumerate(records[email], start=1):
                tree.insert("", "end", values=(idx, entry.get("date",""), entry.get("time",""),
                                               entry.get("subject",""), entry.get("status","")))
        else:
            messagebox.showwarning("Not Found", "No attendance found for this user")

    tk.Button(win, text="Search", bg="#2980b9", fg="white", font=("Segoe UI",12,"bold"),
              command=search).pack(pady=10)

def open_mark_attendance():
    users = load_json(USERS_FILE)

    win = tk.Toplevel(root)
    win.title("Mark Attendance")
    win.geometry("500x300")
    win.configure(bg="#f4f6f7")

    tk.Label(win, text="Select User:", font=("Segoe UI", 12)).pack(pady=5)
    emails = list(users.keys())
    email_cb = ttk.Combobox(win, values=emails, font=("Segoe UI", 12))
    email_cb.pack(pady=5)

    tk.Label(win, text="Subject:", font=("Segoe UI", 12)).pack(pady=5)
    subject_entry = tk.Entry(win, font=("Segoe UI", 12))
    subject_entry.pack(pady=5)

    def submit():
        email = email_cb.get().strip()
        subject = subject_entry.get().strip() or "General"
        if email:
            mark_attendance(email, subject)
        else:
            messagebox.showwarning("Input Error", "Please select a user")

    tk.Button(win, text="Mark Attendance", bg="#27ae60", fg="white", font=("Segoe UI",12,"bold"),
              command=submit).pack(pady=15)

# ========================
# Open Next Dashboard
# ========================
def open_next_dashboard():
    root.destroy()  # close current window
    subprocess.Popen([sys.executable, "admin/admin_dashboard.py"])  # open next page

# ========================
# Main Window
# ========================
root = tk.Tk()
root.title("Admin Dashboard - Attendance System")
root.geometry("950x650")
root.resizable(False, False)

# ========================
# Background Image
# ========================
if os.path.exists(BG_IMAGE_PATH):
    bg_image = Image.open(BG_IMAGE_PATH)
    bg_image = bg_image.resize((950, 650), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
else:
    root.configure(bg="#ecf0f1")

# ========================
# Toolbar
# ========================
toolbar = tk.Frame(root, bg="#34495e", height=60)
toolbar.place(relx=0, rely=0, relwidth=1)
title = tk.Label(toolbar, text="Admin Panel - Attendance System", fg="white", bg="#34495e", font=("Segoe UI", 18, "bold"))
title.pack(pady=10)

# ========================
# Buttons Section
# ========================
def add_hover_effect(button, color_on_hover, color_normal):
    button.bind("<Enter>", lambda e: button.config(bg=color_on_hover))
    button.bind("<Leave>", lambda e: button.config(bg=color_normal))

btn_users = tk.Button(root, text="Users Record", font=("Segoe UI",16,"bold"),
                      width=20, height=2, bg="#bdc3c7", command=open_users_record)
btn_users.place(x=100, y=180)
add_hover_effect(btn_users, "#95a5a6", "#bdc3c7")

btn_att_summary = tk.Button(root, text="Attendance Summary", font=("Segoe UI",16,"bold"),
                            width=20, height=2, bg="#bdc3c7", command=open_attendance_summary)
btn_att_summary.place(x=100, y=260)
add_hover_effect(btn_att_summary, "#95a5a6", "#bdc3c7")

btn_mark_att = tk.Button(root, text="Mark Attendance", font=("Segoe UI",16,"bold"),
                         width=20, height=2, bg="#27ae60", fg="white", command=open_mark_attendance)
btn_mark_att.place(x=100, y=340)
add_hover_effect(btn_mark_att, "#219150", "#27ae60")

btn_search_att = tk.Button(root, text="Search Attendance", font=("Segoe UI",16,"bold"),
                           width=20, height=2, bg="#2980b9", fg="white", command=open_search_attendance)
btn_search_att.place(x=100, y=420)
add_hover_effect(btn_search_att, "#2471a3", "#2980b9")

# 🔹 New button for next dashboard
btn_next = tk.Button(root, text="Go to Next Dashboard", font=("Segoe UI",14,"bold"),
                     bg="#e67e22", fg="white", width=20, command=open_next_dashboard)
btn_next.place(x=680, y=500)
add_hover_effect(btn_next, "#d35400", "#e67e22")

btn_exit = tk.Button(root, text="Exit", font=("Segoe UI",14,"bold"),
                     bg="#e74c3c", fg="white", width=14, command=root.destroy)
btn_exit.place(x=730, y=550)
add_hover_effect(btn_exit, "#c0392b", "#e74c3c")

root.mainloop()
