import tkinter as tk
from tkinter import messagebox
import subprocess, json, os

import sys

# Change to the root project directory so files like users.json load correctly from any IDE
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE_DIR)

# =========================
# Load Users Database
# =========================
USER_DB_FILE = "users.json"
if os.path.exists(USER_DB_FILE):
    with open(USER_DB_FILE, "r") as f:
        users_db = json.load(f)
else:
    users_db = {}

# =========================
# Admin Login Window
# =========================
def open_admin_login():
    admin_win = tk.Toplevel(root)
    admin_win.title("🔒 Admin Secure Login")
    admin_win.geometry("450x300")
    admin_win.config(bg="#1e272e")

    # Heading
    tk.Label(admin_win, text="Admin Login", font=("Segoe UI", 20, "bold"),
             bg="#1e272e", fg="#f5f6fa").pack(pady=15)

    # Username / Email
    tk.Label(admin_win, text="Username / Email", font=("Segoe UI", 12),
             bg="#1e272e", fg="#dcdde1", anchor="w").pack(fill="x", padx=50, pady=(10, 2))
    email_entry = tk.Entry(admin_win, font=("Segoe UI", 12), width=30,
                           relief="flat", bg="#353b48", fg="white", insertbackground="white")
    email_entry.pack(pady=5)

    # Password
    tk.Label(admin_win, text="Password", font=("Segoe UI", 12),
             bg="#1e272e", fg="#dcdde1", anchor="w").pack(fill="x", padx=50, pady=(10, 2))
    pass_entry = tk.Entry(admin_win, font=("Segoe UI", 12), width=30, show="*",
                          relief="flat", bg="#353b48", fg="white", insertbackground="white")
    pass_entry.pack(pady=5)

    # Function to check admin login
    def check_admin():
        email = email_entry.get().strip()
        password = pass_entry.get().strip()

        if email in users_db and users_db[email].get("role") == "admin" and users_db[email]["password"] == password:
            messagebox.showinfo("✅ Success", "Welcome Admin!")
            admin_win.destroy()
            root.destroy()
            subprocess.Popen([sys.executable, "admin/admin_home.py"])  # Go to Admin Home
        else:
            messagebox.showerror("❌ Error", "Invalid Admin Credentials")

    # Login Button
    login_btn = tk.Button(admin_win, text="Login", font=("Segoe UI", 12, "bold"),
                          bg="#00a8ff", fg="white", activebackground="#0097e6",
                          relief="flat", width=15, command=check_admin)
    login_btn.pack(pady=20)

    # Cancel Button
    cancel_btn = tk.Button(admin_win, text="Cancel", font=("Segoe UI", 11),
                           bg="#e84118", fg="white", relief="flat", width=10,
                           command=admin_win.destroy)
    cancel_btn.pack()

# =========================
# Main Window
# =========================
root = tk.Tk()
root.title("Main Page")
root.geometry("500x400")
root.configure(bg="#2f3640")

tk.Label(root, text="Welcome", font=("Segoe UI", 24, "bold"),
         bg="#2f3640", fg="white").pack(pady=30)

# Buttons
def open_user_register():
    root.destroy()
    subprocess.Popen([sys.executable, "register.py"])

tk.Button(root, text="User Register", font=("Segoe UI", 14, "bold"),
          bg="#2980b9", fg="white", relief="flat", width=20,
          command=open_user_register).pack(pady=15)

tk.Button(root, text="Admin Login", font=("Segoe UI", 14, "bold"),
          bg="#e1b12c", fg="black", relief="flat", width=20,
          command=open_admin_login).pack(pady=15)

tk.Button(root, text="Exit", font=("Segoe UI", 14, "bold"),
          bg="#c23616", fg="white", relief="flat", width=20,
          command=root.destroy).pack(pady=15)

root.mainloop()
