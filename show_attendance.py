import pandas as pd
from glob import glob
import os
import tkinter as tk
from tkinter import *
import csv

def text_to_speech(user_text):
    # Implement text_to_speech function as needed
    pass

def subjectchoose(text_to_speech):
    def calculate_attendance():
        Subject = tx.get()
        if not Subject:
            text_to_speech('Please enter the subject name.')
            return
        
        subject_path = os.path.join("Attendance", Subject)
        filenames = glob(os.path.join(subject_path, f"{Subject}*.csv"))
        if not filenames:
            text_to_speech('No files found for the specified subject.')
            return

        dfs = [pd.read_csv(f) for f in filenames]
        newdf = pd.concat(dfs, ignore_index=True)
        newdf.fillna(0, inplace=True)
        newdf["Attendance"] = newdf.iloc[:, 2:].mean(axis=1).apply(lambda x: f"{int(round(x * 100))}%")
        
        attendance_csv_path = os.path.join(subject_path, "attendance.csv")
        newdf.to_csv(attendance_csv_path, index=False)

        display_attendance(attendance_csv_path, Subject)

    def display_attendance(csv_path, subject):
        root = tk.Tk()
        root.title(f"Attendance of {subject}")
        root.geometry("600x400")
        root.configure(background="#34495e")

        with open(csv_path, newline='') as file:
            reader = csv.reader(file)
            for r, row in enumerate(reader):
                for c, item in enumerate(row):
                    label = tk.Label(
                        root,
                        width=15,
                        height=1,
                        fg="#ecf0f1",
                        font=("Helvetica", 12),
                        bg="#34495e",
                        text=item,
                        relief=tk.RIDGE
                    )
                    label.grid(row=r, column=c, padx=5, pady=5)

        root.mainloop()

    def open_sheets():
        subject = tx.get()
        if subject:
            os.startfile(os.path.join("Attendance", subject))

    subject = tk.Tk()
    subject.title("Subject Selection")
    subject.geometry("600x400")
    subject.configure(background="#2c3e50")
    subject.resizable(0, 0)

    # Title Label
    tk.Label(
        subject,
        text="Select Subject for Attendance",
        bg="#2c3e50",
        fg="#ecf0f1",
        font=("Helvetica", 20, "bold"),
    ).pack(pady=20)

    # Subject Entry
    tk.Label(
        subject,
        text="Enter Subject",
        bg="#2c3e50",
        fg="#ecf0f1",
        font=("Helvetica", 14),
    ).pack(pady=5)
    tx = tk.Entry(
        subject,
        bg="#ecf0f1",
        fg="#2c3e50",
        font=("Helvetica", 14),
        relief=FLAT,
        width=20
    )
    tx.pack(pady=5)

    # Button Frame
    button_frame = tk.Frame(subject, bg="#2c3e50")
    button_frame.pack(pady=20)

    # Check Sheets Button
    tk.Button(
        button_frame,
        text="Check Sheets",
        command=open_sheets,
        font=("Helvetica", 16, "bold"),
        fg="#ecf0f1",
        bg="#2980b9",
        activebackground="#3498db",
        relief=FLAT,
        padx=20,
        pady=10,
        width=15
    ).pack(pady=10)

    # View Attendance Button
    tk.Button(
        button_frame,
        text="View Attendance",
        command=calculate_attendance,
        font=("Helvetica", 16, "bold"),
        fg="#ecf0f1",
        bg="#27ae60",
        activebackground="#2ecc71",
        relief=FLAT,
        padx=20,
        pady=10,
        width=15
    ).pack(pady=10)

    subject.mainloop()
