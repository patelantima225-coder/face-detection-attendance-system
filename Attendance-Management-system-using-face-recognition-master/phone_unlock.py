
# Fix working directory issue
import sys
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# phone_unlock.py
import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pyttsx3
import tkinter.simpledialog as simpledialog
import subprocess

# ---------------- Text-to-Speech ----------------
engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 1.0)

# ---------------- Paths ----------------
dataset_dir = "dataset"
os.makedirs(dataset_dir, exist_ok=True)
model_file = "trainer.yml"
background_image_path = r"C:\gunja\RMS\images\images FD\How-Facial-Recognition-Works.jpg"

# ---------------- Face Detection ----------------
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()

# ---------------- Globals ----------------
users = {}  # {id: {"name": ..., "email": ...}}
cap = None
voice_flag = True
unlocked = False

def start_unlock(role_title, email):
    global root, camera_label, status_text, step_text, status_label

    # ---------------- Tkinter GUI ----------------
    root = tk.Tk()
    root.title(f"📱 Phone Unlock Emulator - {role_title}")
    root.state("zoomed")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Background Image
    if os.path.exists(background_image_path):
        bg_img = Image.open(background_image_path).resize((screen_width, screen_height))
        bg_photo = ImageTk.PhotoImage(bg_img)
        bg_label = tk.Label(root, image=bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    else:
        root.configure(bg="black")

    # ---------------- Glassmorphism Frame ----------------
    glass_frame = tk.Frame(root, bg="#111111", bd=0, highlightbackground="#333333", highlightthickness=2)
    glass_frame.place(relx=0.5, rely=0.5, anchor="center", width=500, height=600)

    # ---------------- Labels ----------------
    status_text = tk.StringVar()
    status_text.set("🔒 Phone Locked")
    status_label = tk.Label(glass_frame, textvariable=status_text,
                            fg="white", bg="#111111", font=("Helvetica", 22, "bold"))
    status_label.pack(pady=20)

    step_text = tk.StringVar()
    step_text.set("Step 1️⃣: Capture Face")
    step_label = tk.Label(glass_frame, textvariable=step_text,
                          fg="yellow", bg="#111111", font=("Helvetica", 18, "bold"))
    step_label.pack(pady=10)

    camera_label = tk.Label(glass_frame, bg="#000000")
    camera_label.pack(pady=10)

    # ---------------- Buttons ----------------
    btn_capture = tk.Button(glass_frame, text="1️⃣ Capture Face", command=capture_face,
                            font=("Helvetica", 14, "bold"), bg="#1E90FF", fg="white", width=25)
    btn_capture.pack(pady=10)

    btn_train = tk.Button(glass_frame, text="2️⃣ Train Model", command=train_model,
                          font=("Helvetica", 14, "bold"), bg="#FFA500", fg="white", width=25)
    btn_train.pack(pady=10)

    btn_unlock = tk.Button(glass_frame, text="3️⃣ Face Unlock", command=scan_face,
                           font=("Helvetica", 14, "bold"), bg="#32CD32", fg="white", width=25)
    btn_unlock.pack(pady=10)

    root.mainloop()

# ---------------- Step 1: Capture / Register Face ----------------
def capture_face():
    global users
    step_text.set("Step 1️⃣: Capture Face")
    user_name = simpledialog.askstring("Register", "Enter your name:")
    if not user_name:
        return
    user_email = simpledialog.askstring("Register", "Enter your email (optional):")
    user_id = len(users) + 1
    users[user_id] = {"name": user_name, "email": user_email if user_email else ""}
    count = 0
    cap_local = cv2.VideoCapture(0)
    messagebox.showinfo("Info", f"{user_name} registration starting. Press 'q' to stop early.")

    while True:
        ret, frame = cap_local.read()
        if not ret:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            count += 1
            face_img = gray[y:y+h, x:x+w]
            cv2.imwrite(f"{dataset_dir}/user.{user_id}.{count}.jpg", face_img)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
            cv2.putText(frame, user_name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        cv2.imshow("Capture Face", frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or count >= 30:
            break

    cap_local.release()
    cv2.destroyAllWindows()
    status_text.set(f"✅ Face captured for {user_name}")
    engine.say(f"Face captured successfully for {user_name}")
    engine.runAndWait()
    step_text.set("Step 2️⃣: Train Model")

# ---------------- Step 2: Train Model ----------------
def train_model():
    faces, ids = [], []
    image_files = [f for f in os.listdir(dataset_dir) if f.endswith(".jpg")]
    for img_file in image_files:
        img_path = os.path.join(dataset_dir, img_file)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        try:
            user_id = int(img_file.split(".")[1])
        except:
            continue
        faces.append(img)
        ids.append(user_id)
    if len(faces) == 0:
        messagebox.showerror("Error", "No faces captured. Capture first!")
        return
    recognizer.train(faces, np.array(ids))
    recognizer.save(model_file)
    status_text.set("✅ Model trained successfully!")
    engine.say("Model trained successfully! Ready to unlock.")
    engine.runAndWait()
    step_text.set("Step 3️⃣: Face Unlock")

# ---------------- Step 3: Scan & Unlock ----------------
def scan_face():
    global cap, voice_flag, unlocked
    if cap is None:
        cap = cv2.VideoCapture(0)

    def process_frame():
        global voice_flag, unlocked
        if unlocked:
            return
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            msg, color = "Scanning...", "yellow"

            if len(faces) > 0:
                for (x, y, w, h) in faces:
                    roi = gray[y:y+h, x:x+w]
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255,255,0), 2)
                    try:
                        recognizer.read(model_file)
                        id_, conf = recognizer.predict(roi)
                        if conf < 70 and id_ in users:
                            name = users[id_]["name"]
                            msg = f"✅ {name} Verified - Phone Unlocked"
                            color = "lime"
                            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
                            if voice_flag:
                                engine.say(f"Welcome {name}, phone unlocked")
                                engine.runAndWait()
                                voice_flag = False
                                unlocked = True
                                cap.release()
                                cv2.destroyAllWindows()
                                try:
                                    root.destroy()
                                except:
                                    pass
                                import sys
                                subprocess.Popen([sys.executable, "attendance.py"])
                                return
                        else:
                            msg, color = "❌ Unknown Face - Access Denied", "red"
                            voice_flag = True
                    except:
                        msg, color = "⚠️ Train model first", "orange"

            status_text.set(msg)
            try:
                status_label.config(fg=color)
            except:
                pass

            # Display camera feed
            frame_resized = cv2.resize(frame, (400, 300))
            cv2image = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img, master=root)
            camera_label.imgtk = imgtk
            camera_label.configure(image=imgtk)

        try:
            root.after(10, process_frame)
        except:
            pass

    process_frame()
