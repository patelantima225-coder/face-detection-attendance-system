import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import *

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get().strip()
        if Subject == "":
            t = "Please enter the subject name."
            text_to_speech(t)
            return

        subject_dir = os.path.join("Attendance", Subject)
        if not os.path.exists(subject_dir):
            os.makedirs(subject_dir, exist_ok=True)

        # Find all CSVs created by automatic attendance for this subject
        filenames = glob(os.path.join(subject_dir, f"{Subject}_*.csv"))

        if len(filenames) == 0:
            text_to_speech("No attendance files found for this subject yet.")
            tk.messagebox.showinfo("Info", f"No attendance files found for subject: {Subject}")
            return

        # Read all CSVs; each CSV should minimally have: Enrollment, Name, <date_column>
        dfs = []
        for f in filenames:
            try:
                df = pd.read_csv(f)
                dfs.append(df)
            except Exception:
                continue

        if len(dfs) == 0:
            text_to_speech("No readable attendance files found.")
            tk.messagebox.showinfo("Info", f"No readable files for subject: {Subject}")
            return

        # Merge all by Enrollment + Name (outer join)
        newdf = dfs[0]
        for i in range(1, len(dfs)):
            # union of date columns; keep Enrollment + Name as keys
            newdf = pd.merge(newdf, dfs[i], on=["Enrollment", "Name"], how="outer")

        # Fill NaNs (absent) with 0
        newdf = newdf.fillna(0)

        # Compute percent attendance across all date columns (exclude Enrollment, Name)
        date_cols = [c for c in newdf.columns if c not in ("Enrollment", "Name")]
        if len(date_cols) == 0:
            newdf["Attendance"] = "0%"
        else:
            # Row-wise mean of presence (0/1)
            means = newdf[date_cols].astype(float).mean(axis=1) * 100
            newdf["Attendance"] = means.round(0).astype(int).astype(str) + "%"

        # Save summary as attendance.csv
        out_csv = os.path.join(subject_dir, "attendance.csv")
        newdf.to_csv(out_csv, index=False)

        # Show in a quick Tk viewer
        root = tkinter.Tk()
        root.title("Attendance of " + Subject)
        root.configure(background="black")

        with open(out_csv, newline="") as file:
            reader = csv.reader(file)
            r = 0
            for col in reader:
                c = 0
                for row in col:
                    label = tkinter.Label(
                        root,
                        width=16,
                        height=1,
                        fg="yellow",
                        font=("times", 14, "bold"),
                        bg="black",
                        text=row,
                        relief=tkinter.RIDGE,
                        padx=6, pady=4
                    )
                    label.grid(row=r, column=c, sticky="nsew")
                    c += 1
                r += 1
        root.mainloop()

    subject = Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")

    titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)

    titl = tk.Label(
        subject,
        text="Which Subject of Attendance?",
        bg="black",
        fg="green",
        font=("arial", 25),
    )
    titl.place(x=100, y=12)

    def Attf():
        sub = tx.get().strip()
        if sub == "":
            t = "Please enter the subject name!"
            text_to_speech(t)
            return
        folder = os.path.join("Attendance", sub)
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
            text_to_speech("No attendance records yet for this subject.")
            tk.messagebox.showinfo("Info", f"No records found for subject: {sub}")
            return

        # Open only if something exists
        has_any = any(os.scandir(folder))
        if not has_any:
            text_to_speech("No attendance files found for this subject yet.")
            tk.messagebox.showinfo("Info", f"No records found for subject: {sub}")
            return

        os.startfile(folder)

    attf = tk.Button(
        subject,
        text="Check Sheets",
        command=Attf,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
    )
    attf.place(x=350, y=170)

    sub_lbl = tk.Label(
        subject,
        text="Enter Subject",
        width=12,
        height=2,
        bg="black",
        fg="yellow",
        bd=5,
        relief=RIDGE,
        font=("times new roman", 15),
    )
    sub_lbl.place(x=40, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="black",
        fg="yellow",
        relief=RIDGE,
        font=("times", 30, "bold"),
    )
    tx.place(x=190, y=100)

    fill_a = tk.Button(
        subject,
        text="View Attendance",
        command=calculate_attendance,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=14,
        relief=RIDGE,
    )
    fill_a.place(x=170, y=170)

    subject.mainloop()
