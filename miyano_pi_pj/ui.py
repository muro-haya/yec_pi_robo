# gui_display_three_numbers.py

import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class TimeDisplayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Logging Display")
        
        # Initialize variables to store three numbers
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

            # Create a button to update each number
            button = tk.Button(root, text=f"Sent Data {i + 1}", command=lambda i=i: self.update_number(i), font=('Helvetica', 16))
            button.pack(pady=5)

        # Start the updating loop
        self.update_display()

    def update_display(self):
        # Get the current time
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Update the label with the current time and numbers
        sent_text = "\n".join(f"Sent Data{i + 1}: {num}" for i, num in enumerate(self.numbers) if num is not None)
        self.label.config(text=f"{sent_text}\nCurrent time: {current_time}")
        # Schedule the update_display function to be called again after 1000 ms
        self.root.after(1000, self.update_display)

    def update_number(self, index):
        # Update the number from the corresponding entry widgets
        try:
            command = int(self.entries[index][0].get())
            values = int(self.entries[index][1].get())
            self.numbers[index] = [command, values]
        except ValueError:
            # Handle invalid input
            messagebox.showerror("Error", "One or more entries are not valid numbers.")

def ui_main():
    # Create the main window
    root = tk.Tk()
    app = TimeDisplayApp(root)
    # Start the Tkinter event loop
    root.mainloop()



