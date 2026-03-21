import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime
import json
import os

# File to save chat (simulate database)
CHAT_FILE = "attendance_chat.json"

# Load old chats
if os.path.exists(CHAT_FILE):
    with open(CHAT_FILE, "r") as f:
        chat_history = json.load(f)
else:
    chat_history = []


# Save chat history
def save_chat():
    with open(CHAT_FILE, "w") as f:
        json.dump(chat_history, f, indent=4)


# Generate bot reply based on message
def generate_bot_reply(user_msg):
    user_msg_lower = user_msg.lower()

    if user_msg_lower in ["hi", "hello"]:
        return "Hello! Please enter your email to mark attendance."
    elif "attendance" in user_msg_lower:
        return "Sure! Tell me your email so I can mark your attendance."
    elif "bye" in user_msg_lower:
        return "Goodbye! Have a nice day."
    elif "thank" in user_msg_lower:
        return "You're welcome!"
    elif "joke" in user_msg_lower:
        return "Why did the student eat his homework? Because the teacher said it was a piece of cake!"
    elif "mark" in user_msg_lower:
        # Example of marking attendance
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        return f"Attendance marked successfully on {now}."
    else:
        return "I'm here to help with attendance. Please ask clearly."


# Send message function
def send_message():
    user_msg = entry.get().strip()
    if user_msg == "":
        return

    # Add user message to chatbox
    chat_area.insert(tk.END, f"You: {user_msg}\n")
    chat_history.append({"sender": "user", "message": user_msg})

    # Generate bot reply
    bot_reply = generate_bot_reply(user_msg)
    chat_area.insert(tk.END, f"Bot: {bot_reply}\n\n")
    chat_history.append({"sender": "bot", "message": bot_reply})

    # Save chat
    save_chat()

    # Clear entry field
    entry.delete(0, tk.END)


# Tkinter UI
root = tk.Tk()
root.title("Attendance Chatbot")
root.geometry("500x500")

chat_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=20, state="normal")
chat_area.pack(padx=10, pady=10)

entry = tk.Entry(root, width=40, font=("Arial", 12))
entry.pack(side=tk.LEFT, padx=10, pady=10)

send_button = tk.Button(root, text="Send", command=send_message)
send_button.pack(side=tk.LEFT, padx=5)

root.mainloop()
