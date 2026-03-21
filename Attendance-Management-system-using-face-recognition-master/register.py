
# Fix working directory issue
import sys
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import messagebox, ttk
import json, re, os
from PIL import Image, ImageTk
from datetime import datetime

# ========================
# Load or initialize users DB
# ========================
USER_DB_FILE = "users.json"
if os.path.exists(USER_DB_FILE):
    with open(USER_DB_FILE, "r") as f:
        data = json.load(f)
        if isinstance(data, list):
            users_db = {user["email"]: user for user in data if "email" in user}
        elif isinstance(data, dict):
            users_db = data
        else:
            users_db = {}
else:
    users_db = {}

def save_users_db():
    with open(USER_DB_FILE, "w") as f:
        json.dump(users_db, f, indent=4)

def open_login():
    root.destroy()
    import sys
    import subprocess
    subprocess.Popen([sys.executable, "Login.py"])

# ========================
# UI Setup
# ========================
root = tk.Tk()
root.title("User Registration - CLASS VISION")
root.geometry("1000x650")
root.resizable(False, False)

# ========================
# Background Image
# ========================
bg_path = r"C:\gunja\RMS\images\images FD\gunja.jfif"
if os.path.exists(bg_path):
    bg_img = Image.open(bg_path).resize((1000, 650))
    bg_photo = ImageTk.PhotoImage(bg_img)
    canvas = tk.Canvas(root, width=1000, height=650, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
else:
    root.configure(bg="#2c5364")
    canvas = tk.Canvas(root, width=1000, height=650, highlightthickness=0, bg="#2c5364")
    canvas.pack(fill="both", expand=True)

# ========================
# Main frame (center)
# ========================
frame = tk.Frame(root, bg="white", bd=2, relief="ridge")
canvas.create_window(500, 325, window=frame, width=650, height=580)

tk.Label(frame, text="REGISTER", font=("Segoe UI", 28, "bold"), bg="white", fg="#2c5364").pack(pady=15)

# ========================
# Variables
# ========================
name_var = tk.StringVar()
email_var = tk.StringVar()
contact_var = tk.StringVar()
password_var = tk.StringVar()
confirm_password_var = tk.StringVar()
country_code_var = tk.StringVar(value="+91")

# ========================
# Reusable styled Entry
# ========================
def form_field(label_text, variable, parent=frame, show=None):
    tk.Label(parent, text=label_text, font=("Segoe UI", 12, "bold"), bg="white", anchor="w").pack(padx=50, fill="x")
    entry = tk.Entry(parent, textvariable=variable, font=("Segoe UI", 12), fg="#000", bg="#f9f9f9",
                     relief="flat", highlightthickness=1, highlightbackground="#ccc")
    entry.pack(padx=50, fill="x", ipady=7, pady=(0, 10))
    if show:
        entry.config(show=show)
    return entry

# ========================
# Input Fields
# ========================
form_field("Full Name", name_var)
form_field("Email", email_var)

tk.Label(frame, text="Contact", font=("Segoe UI", 12, "bold"), bg="white", anchor="w").pack(padx=50, fill="x")
contact_row = tk.Frame(frame, bg="white")
contact_row.pack(padx=50, pady=(0, 10), anchor="w", fill="x")

ttk.Combobox(contact_row, textvariable=country_code_var, values=["+91", "+1", "+44"],
             width=5, font=("Segoe UI", 11), state="readonly").pack(side="left")

tk.Entry(contact_row, textvariable=contact_var, font=("Segoe UI", 12), fg="#000", bg="#f9f9f9",
         relief="flat", highlightthickness=1, highlightbackground="#ccc", width=30).pack(side="left", padx=10, ipady=5)

form_field("Password", password_var, show="*")
form_field("Confirm Password", confirm_password_var, show="*")

# ========================
# Register Logic
# ========================
def register_user():
    name = name_var.get().strip()
    email = email_var.get().strip()
    contact = contact_var.get().strip()
    password = password_var.get()
    confirm = confirm_password_var.get()
    full_contact = f"{country_code_var.get()}{contact}"

    if not name or not email or not contact or not password or not confirm:
        messagebox.showerror("Error", "All fields required.")
        return

    # Email Validation
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, email):
        messagebox.showerror("Error", "Invalid email format. Please enter a valid email.")
        return

    if email in users_db:
        messagebox.showerror("Error", "Email already exists.")
        return

    if not re.match(r"^\d{10}$", contact):
        messagebox.showerror("Error", "Contact must be 10 digits.")
        return

    if password != confirm:
        messagebox.showerror("Error", "Passwords don't match.")
        return

    # Save user with timestamp and empty attendance
    users_db[email] = {
        "name": name,
        "email": email,
        "contact": full_contact,
        "password": password,
        "role": "user",   # force user only
        "registered_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "attendance": []
    }

    save_users_db()
    messagebox.showinfo("Success", "User registered successfully!")

    root.destroy()
    import sys
    import subprocess
    subprocess.Popen([sys.executable, "Login.py"])

# ========================
# Buttons
# ========================
tk.Button(frame, text="Register", command=register_user,
          bg="#2c5364", fg="white", font=("Segoe UI", 13, "bold"),
          width=20, height=2, cursor="hand2").pack(pady=(10,5))

tk.Button(frame, text="Go to Login Page →", command=open_login,
          bg="#f9a825", fg="white", font=("Segoe UI", 12, "bold"),
          width=25, height=2, cursor="hand2").pack(pady=(5,15))

root.mainloop()
