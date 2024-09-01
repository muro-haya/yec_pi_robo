import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import PIL.Image, PIL.ImageTk

class TimeDisplayApp:
    def __init__(self, root, camera_task):
        self.root = root
        self.camera_task = camera_task
        self.root.title("Logging Display")

        # Initialize variables to store numbers
        self.numbers = [[None, None], [None, None], [None, None]]

        # Create labels for displaying the numbers and time
        self.label = tk.Label(root, font=('Helvetica', 16))
        self.label.pack(pady=20)

        # Create labels and entry widgets for three numbers
        self.entries = [[] for _ in range(3)]
        for i in range(3):
            frame = tk.Frame(root)
            frame.pack(pady=5)

            label = tk.Label(frame, text=f"CMD{i + 1}:", font=('Helvetica', 16))
            label.pack(side=tk.LEFT, padx=5)

            entry = tk.Entry(frame, font=('Helvetica', 16))
            entry.pack(side=tk.LEFT, padx=5)
            self.entries[i].append(entry)

            label = tk.Label(frame, text=f"VAL{i + 1}:", font=('Helvetica', 16))
            label.pack(side=tk.LEFT, padx=5)

            entry = tk.Entry(frame, font=('Helvetica', 16))
            entry.pack(side=tk.LEFT, padx=5)
            self.entries[i].append(entry)

            button = tk.Button(root, text=f"Send Data {i + 1}", command=lambda i=i: self.update_number(i), font=('Helvetica', 16))
            button.pack(pady=5)

        # Add a Save button
        self.save_button = tk.Button(root, text="Save to File", command=self.save_to_file, font=('Helvetica', 16))
        self.save_button.pack(pady=10)

        # Create a label for video feed
        self.video_label = tk.Label(root)
        self.video_label.pack()

        # Start updating the display and video feed
        self.update_display()
        self.update_video()

    def update_display(self):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sent_text = "\n".join(f"Sent Data {i + 1}: {num}" for i, num in enumerate(self.numbers) if num is not None)
        self.label.config(text=f"{sent_text}\nCurrent time: {current_time}")
        self.root.after(1000, self.update_display)

    def update_video(self):
        frame = self.camera_task.get_frame()
        if frame is not None:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = PIL.Image.fromarray(frame)
            img_tk = PIL.ImageTk.PhotoImage(image=img)
            self.video_label.config(image=img_tk)
            self.video_label.image = img_tk
        self.root.after(30, self.update_video)

    def update_number(self, index):
        try:
            command = int(self.entries[index][0].get())
            values = int(self.entries[index][1].get())
            self.numbers[index] = [command, values]
        except ValueError:
            messagebox.showerror("Error", "One or more entries are not valid numbers.")

    def save_to_file(self):
        with open("numbers.txt", "w") as file:
            for i, num in enumerate(self.numbers):
                file.write(f"Number {i + 1}: {num}\n")
        messagebox.showinfo("Info", "Numbers saved to numbers.txt")
