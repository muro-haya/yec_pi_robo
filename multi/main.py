import tkinter as tk
from camera_task import CameraTask
from gui_display_three_numbers import TimeDisplayApp

def main():
    # Initialize the camera task
    camera_task = CameraTask()
    camera_task.start()

    # Create the main window
    root = tk.Tk()

    # Initialize the GUI task
    app = TimeDisplayApp(root, camera_task)

    # Start the Tkinter event loop
    root.mainloop()

    # Clean up
    camera_task.stop()

if __name__ == "__main__":
    main()
