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
trainimagelabel_path = "TrainingImageLabel/Trainner.yml"
trainimage_path = "TrainingImage"
studentdetail_path = "StudentDetails/studentdetails.csv"
attendance_path = "Attendance"

# for choosing the subject and filling attendance
def subjectChoose(text_to_speech):
    def FillAttendance():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            try:
                recognizer.read(trainimagelabel_path)
            except:
                e = "Model not found, please train the model"
                Notifica.configure(
                    text=e,
                    bg="#FF5733",
                    fg="white",
                    width=33,
                    font=("Helvetica", 12, "bold"),
                )
                Notifica.place(x=20, y=250)
                text_to_speech(e)
                return
            
            facecasCade = cv2.CascadeClassifier(haarcasecade_path)
            df = pd.read_csv(studentdetail_path)
            cam = cv2.VideoCapture(0)
            font = cv2.FONT_HERSHEY_SIMPLEX
            col_names = ["Enrollment", "Name"]
            attendance = pd.DataFrame(columns=col_names)

            now = time.time()
            future = now + 20

            while True:
                ___, im = cam.read()
                gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                faces = facecasCade.detectMultiScale(gray, 1.2, 5)
                for (x, y, w, h) in faces:
                    global Id

                    Id, conf = recognizer.predict(gray[y : y + h, x : x + w])
                    if conf < 70:
                        global Subject
                        global aa
                        global date
                        global timeStamp
                        Subject = tx.get()
                        ts = time.time()
                        date = datetime.datetime.fromtimestamp(ts).strftime(
                            "%Y-%m-%d"
                        )
                        timeStamp = datetime.datetime.fromtimestamp(ts).strftime(
                            "%H:%M:%S"
                        )
                        aa = df.loc[df["Enrollment"] == Id]["Name"].values
                        global tt
                        tt = str(Id) + "-" + aa
                        attendance.loc[len(attendance)] = [
                            Id,
                            aa,
                        ]
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        cv2.putText(
                            im, str(tt), (x + h, y), font, 1, (255, 255, 255), 2
                        )
                    else:
                        Id = "Unknown"
                        tt = str(Id)
                        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 2)
                        cv2.putText(
                            im, str(tt), (x + h, y), font, 1, (0, 0, 255), 2
                        )
                if time.time() > future:
                    break

                attendance = attendance.drop_duplicates(
                    ["Enrollment"], keep="first"
                )
                cv2.imshow("Filling Attendance...", im)
                key = cv2.waitKey(30) & 0xFF
                if key == 27:
                    break

            ts = time.time()
            attendance[date] = 1
            date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")
            Hour, Minute, Second = timeStamp.split(":")
            path = os.path.join(attendance_path, Subject)
            if not os.path.exists(path):
                os.makedirs(path)
            fileName = (
                f"{path}/"
                + Subject
                + "_"
                + date
                + "_"
                + Hour
                + "-"
                + Minute
                + "-"
                + Second
                + ".csv"
            )
            attendance.to_csv(fileName, index=False)

            m = "Attendance Filled Successfully for " + Subject
            Notifica.configure(
                text=m,
                bg="#28B463",
                fg="white",
                width=33,
                relief=RIDGE,
                bd=5,
                font=("Helvetica", 12, "bold"),
            )
            Notifica.place(x=20, y=250)
            text_to_speech(m)

            cam.release()
            cv2.destroyAllWindows()

            # Displaying the CSV file content in a dialogue box
            root = Tk()
            root.title("Attendance of " + Subject)
            root.configure(background="#34495E")
            with open(fileName, newline="") as file:
                reader = csv.reader(file)
                r = 0
                for col in reader:
                    c = 0
                    for row in col:
                        label = Label(
                            root,
                            width=10,
                            height=1,
                            fg="#F7DC6F",
                            font=("Helvetica", 12, "bold"),
                            bg="#34495E",
                            text=row,
                            relief=RIDGE,
                        )
                        label.grid(row=r, column=c)
                        c += 1
                    r += 1
            root.mainloop()

    subject = Tk()
    subject.title("Subject Selection")
    subject.geometry("580x320")
    subject.resizable(0, 0)
    subject.configure(background="#1C2833")

    titl = tk.Label(subject, bg="#1C2833", relief=RIDGE, bd=10, font=("Helvetica", 25))
    titl.pack(fill=X)
    
    titl = tk.Label(
        subject,
        text="Enter the Subject Name",
        bg="#1C2833",
        fg="#AED6F1",
        font=("Helvetica", 20, "bold"),
    )
    titl.place(x=160, y=12)

    Notifica = tk.Label(
        subject,
        text="Attendance filled Successfully",
        bg="#F7DC6F",
        fg="#1C2833",
        width=33,
        height=2,
        font=("Helvetica", 12, "bold"),
    )

    def Attf():
        sub = tx.get()
        if sub == "":
            t = "Please enter the subject name!!!"
            text_to_speech(t)
        else:
            os.startfile(
                f"Attendance\\{sub}"
            )

    # attf = tk.Button(
    #     subject,
    #     text="Check Sheets",
    #     command=Attf,
    #     bd=7,
    #     font=("Helvetica", 12, "bold"),
    #     bg="#1C2833",
    #     fg="#AED6F1",
    #     height=2,
    #     width=10,
    #     relief=RIDGE,
    # )
    # attf.place(x=360, y=170)

    sub = tk.Label(
        subject,
        text="Enter Subject",
        width=10,
        height=2,
        bg="#1C2833",
        fg="#AED6F1",
        bd=5,
        relief=RIDGE,
        font=("Helvetica", 15, "bold"),
    )
    sub.place(x=50, y=100)

    tx = tk.Entry(
        subject,
        width=15,
        bd=5,
        bg="#1C2833",
        fg="#AED6F1",
        relief=RIDGE,
        font=("Helvetica", 20, "bold"),
    )
    tx.place(x=190, y=100)

    fill_a = tk.Button(
        subject,
        text="Fill Attendance",
        command=FillAttendance,
        bd=7,
        font=("Helvetica", 12, "bold"),
        bg="#1C2833",
        fg="#AED6F1",
        height=2,
        width=12,
        relief=RIDGE,
    )
    fill_a.place(x=195, y=170)

    subject.mainloop()
