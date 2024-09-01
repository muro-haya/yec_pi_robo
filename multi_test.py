import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import cv2
import PIL.Image, PIL.ImageTk
import threading

class TimeDisplayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenCV Main Task with Tkinter Subtasks")

        # Initialize variables to store numbers
        self.numbers = [None, None, None]

        # Create labels for displaying the numbers and time
        self.label = tk.Label(root, font=('Helvetica', 16))
        self.label.pack(pady=20)

        # Create labels and entry widgets for three numbers
        self.entries = [[] for _ in range(3)]
        for i in range(3):
            frame = tk.Frame(root)
            frame.pack(pady=5)

            for j in range(2):
                label = tk.Label(frame, text=f"Number {i*2 + j + 1}:", font=('Helvetica', 16))
                label.pack(side=tk.LEFT, padx=5)
                
                entry = tk.Entry(frame, font=('Helvetica', 16))
                entry.pack(side=tk.LEFT, padx=5)
                self.entries[i].append(entry)
        
            button = tk.Button(root, text=f"Send Number {i + 1}", command=lambda i=i: self.update_number(i), font=('Helvetica', 16))
            button.pack(pady=5)

        # Add a Save button
        self.save_button = tk.Button(root, text="Save to File", command=self.save_to_file, font=('Helvetica', 16))
        self.save_button.pack(pady=10)

        # Initialize video capture
        self.cap = cv2.VideoCapture(0)

        # Create a label for video feed
        self.video_label = tk.Label(root)
        self.video_label.pack()

        # Start the camera thread
        self.camera_thread = threading.Thread(target=self.update_video, daemon=True)
        self.camera_thread.start()

        # Start the UI thread
        self.ui_thread = threading.Thread(target=self.ui_main, daemon=False)
        self.ui_thread.start()

    def update_display(self):
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        numbers_text = "\n".join(f"Number {i + 1}: {num}" for i, num in enumerate(self.numbers) if num is not None)
        self.label.config(text=f"{numbers_text}\nCurrent time: {current_time}")
        self.root.after(1000, self.update_display)  # Schedule the next update in 1 second

    def update_video(self):
        while True:
            ret, frame = self.cap.read()
            if ret:
                # Convert the frame to RGB (tkinter uses RGB, OpenCV uses BGR)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Convert to PIL Image
                img = PIL.Image.fromarray(frame)
                img_tk = PIL.ImageTk.PhotoImage(image=img)
                # Use thread-safe method to update GUI
                self.root.after(0, self.update_video_label, img_tk)
            # Sleep for a short period to allow other tasks to execute
            cv2.waitKey(1)

    def update_video_label(self, img_tk):
        # Update the label with the new image
        self.video_label.config(image=img_tk)
        self.video_label.image = img_tk

    def update_number(self, index):
        try:
            values = [float(self.entries[index][0].get()), float(self.entries[index][1].get())]
            self.numbers[index] = sum(values)
            for entry in self.entries[index]:
                entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "One or more entries are not valid numbers.")

    def save_to_file(self):
        with open("numbers.txt", "w") as file:
            for i, num in enumerate(self.numbers):
                file.write(f"Number {i + 1}: {num}\n")
        messagebox.showinfo("Info", "Numbers saved to numbers.txt")

    def ui_main(self):
        # This method can be used to handle other UI tasks
        self.update_display()
        self.root.mainloop()

    def __del__(self):
        self.cap.release()

# Create the main window
root = tk.Tk()
app = TimeDisplayApp(root)

# Start the Tkinter event loop
root.mainloop()
