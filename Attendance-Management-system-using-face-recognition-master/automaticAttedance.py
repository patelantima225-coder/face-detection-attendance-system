import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.ttk as tkk
import tkinter.font as font

haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = os.path.join("TrainingImageLabel", "Trainner.yml")
trainimage_path = "TrainingImage"
studentdetail_path = os.path.join("StudentDetails", "studentdetails.csv")
attendance_path = "Attendance"

# for choose subject and fill attendance
def subjectChoose(text_to_speech):
    def FillAttendance():
        sub = tx.get().strip()
        now = time.time()
        future = now + 20  # run camera for ~20s

        if sub == "":
            t = "Please enter the subject name!"
            text_to_speech(t)
            return

        # Ensure attendance root + subject folder exist
        subject_dir = os.path.join(attendance_path, sub)
        os.makedirs(subject_dir, exist_ok=True)

        try:
            # Load model
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            try:
                recognizer.read(trainimagelabel_path)
            except Exception:
                e = "Model not found. Please train the model first."
                Notifica.configure(
                    text=e, bg="black", fg="yellow", width=33, font=("times", 15, "bold"),
                )
                Notifica.place(x=20, y=250)
                text_to_speech(e)
                return

            # Load face detector and student details
            facecasCade = cv2.CascadeClassifier(haarcasecade_path)

            if not os.path.exists(studentdetail_path):
                msg = "Student details file not found."
                Notifica.configure(text=msg, bg="black", fg="yellow", width=33, font=("times", 15, "bold"))
                Notifica.place(x=20, y=250)
                text_to_speech(msg)
                return

            df = pd.read_csv(studentdetail_path)

            # Normalize Enrollment type to int if possible
            if "Enrollment" in df.columns:
                try:
                    df["Enrollment"] = df["Enrollment"].astype(int)
                except Exception:
                    pass  # keep as-is if mixed

            cam = cv2.VideoCapture(0)
            cv_font = cv2.FONT_HERSHEY_SIMPLEX

            col_names = ["Enrollment", "Name"]
            attendance = pd.DataFrame(columns=col_names)

            while True:
                ret, im = cam.read()
                if not ret:
                    break

                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = facecasCade.detectMultiScale(gray, 1.2, 5)

                for (x, y, w, h) in faces:
                    try:
                        pred_id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                    except Exception:
                        continue

                    if conf < 70:
                        # Find name for the predicted ID
                        name_val = ""
                        try:
                            match = df.loc[df["Enrollment"] == pred_id, "Name"]
                            if len(match) > 0:
                                name_val = str(match.values[0])
                        except Exception:
                            pass

                        attendance.loc[len(attendance)] = [pred_id, name_val]

                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        label_text = f"{pred_id}-{name_val}" if name_val else str(pred_id)
                        cv2.putText(im, label_text, (x, y - 10), cv_font, 0.8, (255, 255, 0), 2)
                    else:
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 2)
                        cv2.putText(im, "Unknown", (x, y - 10), cv_font, 0.8, (0, 25, 255), 2)

                if time.time() > future:
                    break

                # Keep only first entry per Enrollment during the session
                if "Enrollment" in attendance.columns:
                    attendance = attendance.drop_duplicates(["Enrollment"], keep="first")

                cv2.imshow("Filling Attendance...", im)
                key = cv2.waitKey(30) & 0xFF
                if key == 27:
                    break

            ts = time.time()
            date_str = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
            Hour, Minute, Second = timeStamp.split(":")

            # Mark presence for this date
            if len(attendance) == 0:
                msg = "No recognized faces for attendance."
                Notifica.configure(text=msg, bg="black", fg="yellow", width=33, font=("times", 15, "bold"))
                Notifica.place(x=20, y=250)
                text_to_speech(msg)
            else:
                attendance[date_str] = 1  # present

                fileName = f"{sub}_{date_str}_{Hour}-{Minute}-{Second}.csv"
                filePath = os.path.join(subject_dir, fileName)

                # Ensure columns order: Enrollment, Name, date
                base_cols = ["Enrollment", "Name"]
                other_cols = [c for c in attendance.columns if c not in base_cols]
                attendance = attendance[base_cols + other_cols]

                attendance.to_csv(filePath, index=False)

                m = f"Attendance filled successfully for {sub}"
                Notifica.configure(
                    text=m, bg="black", fg="yellow", width=33, relief=RIDGE, bd=5, font=("times", 15, "bold"),
                )
                Notifica.place(x=20, y=250)
                text_to_speech(m)

                # Quick viewer window
                import tkinter
                root = tkinter.Tk()
                root.title("Attendance of " + sub)
                root.configure(background="black")
                with open(filePath, newline="") as file:
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

        except Exception as ex:
            text_to_speech("No Face found for attendance")
        finally:
            try:
                cam.release()
            except Exception:
                pass
            cv2.destroyAllWindows()

    # Window for subject chooser
    subject = Tk()
    subject.title("Subject...")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="black")

    titl = tk.Label(subject, bg="black", relief=RIDGE, bd=10, font=("arial", 30))
    titl.pack(fill=X)

    titl = tk.Label(
        subject,
        text="Enter the Subject Name",
        bg="black",
        fg="green",
        font=("arial", 25),
    )
    titl.place(x=160, y=12)

    Notifica = tk.Label(
        subject,
        text="",
        bg="black",
        fg="yellow",
        width=33,
        height=2,
        font=("times", 15, "bold"),
    )

    def Attf():
        sub = tx.get().strip()
        if sub == "":
            t = "Please enter the subject name!"
            text_to_speech(t)
            return
        folder = os.path.join(attendance_path, sub)
        if not os.path.exists(folder):
            # Create it so next time it exists, but inform user there are no files yet.
            os.makedirs(folder, exist_ok=True)
            text_to_speech("No attendance records yet for this subject.")
            tk.messagebox.showinfo("Info", f"No records found for subject: {sub}")
            return

        # Open only if there is something inside
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
        text="Fill Attendance",
        command=FillAttendance,
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        height=2,
        width=12,
        relief=RIDGE,
    )
    fill_a.place(x=170, y=170)

    subject.mainloop()
