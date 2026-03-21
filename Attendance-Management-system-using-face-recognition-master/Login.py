
# Fix working directory issue
import sys
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
import json, os

# ========================
# Database File
# ========================
USER_DB_FILE = "users.json"
if os.path.exists(USER_DB_FILE):
    with open(USER_DB_FILE, "r") as f:
        users_db = json.load(f)
else:
    users_db = {}

# ========================
# Functional Logic
# ========================
def open_register():
    root.destroy()
    import sys
    import subprocess
    subprocess.Popen([sys.executable, "register.py"])

def toggle_password():
    if password_entry.cget('show') == '*':
        password_entry.config(show='')
        toggle_btn.config(text='Hide')
    else:
        password_entry.config(show='*')
        toggle_btn.config(text='Show')

def forgot_password():
    email = email_entry.get().strip()
    if not email:
        messagebox.showwarning("Missing Email", "Enter your registered email first.")
        return

    if email not in users_db:
        messagebox.showerror("Not Found", "Email not registered.")
        return

    new_password = simpledialog.askstring("Reset Password", "Enter your new password:", show="*")
    if not new_password:
        return
    confirm_password = simpledialog.askstring("Confirm Password", "Re-enter your new password:", show="*")

    if new_password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match.")
        return

    users_db[email]["password"] = new_password
    with open(USER_DB_FILE, "w") as f:
        json.dump(users_db, f, indent=4)
    messagebox.showinfo("Success", "Password updated successfully.")

def login():
    email = email_entry.get().strip()
    password = password_entry.get().strip()

    if not email or not password:
        messagebox.showwarning("Missing", "Fill all fields.")
        return

    if email not in users_db:
        messagebox.showerror("Login Failed", "Email not registered.")
        return

    if users_db[email]["password"] != password:
        messagebox.showerror("Login Failed", "Wrong password.")
        return

    # ✅ Determine role automatically
    role = "Admin" if email == "admin@gmail.com" else "User"
    role_title = "Admin Panel" if role == "Admin" else "User Dashboard"

    # ✅ Login ke baad Face Unlock open hoga
    root.destroy()
    import phone_unlock
    phone_unlock.start_unlock(role_title, email)

# ========================
# UI Layout
# ========================
root = tk.Tk()
root.title("Login - CLASS VISION")
root.geometry("1000x600")
root.resizable(False, False)

# ========================
# Background Image
# ========================
bg_path = r"C:\gunja\RMS\images\images FD\edited.jfif"
if os.path.exists(bg_path):
    bg_image = Image.open(bg_path).resize((1000, 600))
    bg_photo = ImageTk.PhotoImage(bg_image)

    canvas = tk.Canvas(root, width=1000, height=600)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
else:
    root.configure(bg="#e3f2fd")

# ========================
# Center Frame (Card Look)
# ========================
frame = tk.Frame(root, bg="white", bd=0, relief="flat")
frame.place(relx=0.5, rely=0.5, anchor="center", width=450, height=420)

# Title
tk.Label(frame, text="LOGIN", font=("Segoe UI", 28, "bold"), bg="white", fg="#212DAE").pack(pady=(20, 5))
tk.Frame(frame, bg="#212DAE", height=2, width=100).pack(pady=(0, 20))

# Email
tk.Label(frame, text="Email", font=("Segoe UI", 12, "bold"), bg="white", anchor="w").pack(padx=30, fill="x")
email_entry = tk.Entry(frame, font=("Segoe UI", 13), fg="#000", bg="#f1f3f6", relief="flat")
email_entry.pack(padx=30, fill="x", ipady=7, pady=(5, 15))

# Password
tk.Label(frame, text="Password", font=("Segoe UI", 12, "bold"), bg="white", anchor="w").pack(padx=30, fill="x")
pw_frame = tk.Frame(frame, bg="white")
pw_frame.pack(padx=30, fill="x", pady=(5, 15))

password_entry = tk.Entry(pw_frame, font=("Segoe UI", 13), fg="#000", bg="#f1f3f6", relief="flat", show="*")
password_entry.pack(side="left", fill="x", expand=True, ipady=7)

toggle_btn = tk.Button(pw_frame, text="Show", font=("Segoe UI", 9), command=toggle_password,
                       bd=0, bg="white", fg="#007BFF", cursor="hand2")
toggle_btn.pack(side="right", padx=(8, 0))

# Info: Admin option removed
tk.Label(frame, text="* Admin login only for admin@gmail.com", font=("Segoe UI", 9), bg="white", fg="red").pack(pady=(0,5))

# Login Button
tk.Button(frame, text="Login", command=login, bg="#212DAE", fg="white",
          font=("Segoe UI", 13, "bold"), width=20, height=2,
          relief="flat", cursor="hand2").pack(pady=15)

# Forgot Password
tk.Button(frame, text="Forgot Password?", command=forgot_password,
          bg="white", fg="red", bd=0, font=("Segoe UI", 11, "underline"), cursor="hand2").pack()

# Register
tk.Button(frame, text="New User? Register Here", command=open_register,
          bg="white", fg="skyblue", bd=0, font=("Segoe UI", 11, "underline"), cursor="hand2").pack(pady=(5, 0))

root.mainloop()
