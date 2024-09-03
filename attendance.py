import tkinter as tk
from tkinter import *
import os
import pyttsx3

# project module
import show_attendance
import takeImage
import trainImage
import automaticAttedance


def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()


haarcasecade_path = "haarcascade_frontalface_default.xml"
trainimagelabel_path = "TrainingImageLabel/Trainner.yml"
trainimage_path = "TrainingImage"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

studentdetail_path = "StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

window = Tk()
window.title("Face Recognizer")
window.geometry("800x600")
window.configure(background="#2c3e50")

# Set default font
default_font = "Helvetica"

# Styling options
button_style = {
    "font": (default_font, 16, "bold"),
    "fg": "#ecf0f1",
    "relief": FLAT,
    "cursor": "hand2",
    "bd": 0,
    "highlightthickness": 0,
    "padx": 20,
    "pady": 10,
    "height": 2,
    "width": 20,
    "borderwidth": 0,
}

# Error message for name and no
def err_screen():
    sc1 = tk.Tk()
    sc1.geometry("400x110")
    sc1.title("Warning")
    sc1.configure(background="#e74c3c")
    sc1.resizable(0, 0)
    tk.Label(
        sc1,
        text="Enrollment & Name required!",
        fg="#ffffff",
        bg="#e74c3c",
        font=(default_font, 16, "bold"),
    ).pack(pady=20)
    tk.Button(
        sc1,
        text="OK",
        command=sc1.destroy,
        **button_style,
        bg="#c0392b",
        activebackground="#e74c3c",
        padx=10,
        pady=5,
    ).pack()
    sc1.mainloop()


def testVal(inStr, acttyp):
    if acttyp == "1":  # insert
        if not inStr.isdigit():
            return False
    return True

def TakeImageUI():
    ImageUI = Tk()
    ImageUI.title("Register Face")
    ImageUI.geometry("400x400")
    ImageUI.configure(background="#34495e")
    ImageUI.resizable(0, 0)

    # Title Label
    tk.Label(
        ImageUI,
        text="Register Your Face",
        bg="#34495e",
        fg="#ecf0f1",
        font=(default_font, 20, "bold"),
    ).pack(pady=20)

    # Enrollment Number Entry
    tk.Label(
        ImageUI,
        text="Enrollment No",
        bg="#34495e",
        fg="#ecf0f1",
        font=(default_font, 14),
    ).pack(pady=5)
    txt1 = tk.Entry(
        ImageUI,
        validate="key",
        bg="#ecf0f1",
        fg="#2c3e50",
        font=(default_font, 14),
        relief=FLAT,
    )
    txt1.pack(pady=5)
    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    # Name Entry
    tk.Label(
        ImageUI,
        text="Name",
        bg="#34495e",
        fg="#ecf0f1",
        font=(default_font, 14),
    ).pack(pady=5)
    txt2 = tk.Entry(
        ImageUI,
        bg="#ecf0f1",
        fg="#2c3e50",
        font=(default_font, 14),
        relief=FLAT,
    )
    txt2.pack(pady=5)

    # Notification Label
    message = tk.Label(
        ImageUI,
        text="",
        bg="#34495e",
        fg="#ecf0f1",
        font=(default_font, 12),
    )
    message.pack(pady=5)

    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()
        takeImage.TakeImage(
            l1,
            l2,
            haarcasecade_path,
            trainimage_path,
            message,
            err_screen,
            text_to_speech,
        )
        txt1.delete(0, "end")
        txt2.delete(0, "end")

    # Take Image Button
    tk.Button(
        ImageUI,
        text="Take Image",
        command=take_image,
        **button_style,
        bg="#27ae60",
        activebackground="#2ecc71",
    ).pack(pady=10)

    def train_image():
        trainImage.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )

    # Train Image Button
    tk.Button(
        ImageUI,
        text="Train Image",
        command=train_image,
        **button_style,
        bg="#27ae60",
        activebackground="#2ecc71",
    ).pack(pady=10)


def automatic_attedance():
    automaticAttedance.subjectChoose(text_to_speech)


def view_attendance():
    show_attendance.subjectchoose(text_to_speech)


# Centralized button frame
button_frame = Frame(window, bg="#2c3e50")
button_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

# Register Button
r1 = tk.Button(
    button_frame,
    text="Register a New Student",
    command=TakeImageUI,
    **button_style,
    bg="#2980b9",
    activebackground="#3498db",
)
r1.pack(pady=10)

# Take Attendance Button
r2 = tk.Button(
    button_frame,
    text="Take Attendance",
    command=automatic_attedance,
    **button_style,
    bg="#2980b9",
    activebackground="#3498db",
)
r2.pack(pady=10)

# View Attendance Button
r3 = tk.Button(
    button_frame,
    text="View Attendance",
    command=view_attendance,
    **button_style,
    bg="#2980b9",
    activebackground="#3498db",
)
r3.pack(pady=10)

# Exit Button
r4 = tk.Button(
    button_frame,
    text="EXIT",
    command=quit,
    **button_style,
    bg="#e74c3c",
    activebackground="#c0392b",
)
r4.pack(pady=10)

window.mainloop()
