import cv2
import tkinter as tk
from PIL import Image, ImageTk
from threading import Thread
import os

def viewfinder(frame_size, cam, label):
    while True:
        # Read Frame and Condition from Camera
        ret, frame = cam.read()

        if ret:
            # Resize Frame to 480x320
            frame = cv2.resize(frame, frame_size)

            # Convert CV Image to PIL Image
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            # Convert PIL Image to Tkinter Image
            image = ImageTk.PhotoImage(image)

            # Show Image in Label
            label.config(image=image)
            label.image = image

def capture_image(frame_size, cam, window):
    # Read Frame and Condition from Camera
    ret, frame = cam.read()

    if ret:
        # Resize Frame to 380x220
        frame = cv2.resize(frame, frame_size)

        # Open New Window
        new_window = tk.Toplevel(window)
        new_label = tk.Label(new_window)
        new_label.pack()

        # Convert CV Image to PIL Image
        image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Convert PIL Image to Tkinter Image
        image = ImageTk.PhotoImage(image)

        # Show Image in Label
        new_label.config(image=image)
        new_label.image = image

        # Save Image to File
        cv2.imwrite("captured_image.jpg", frame)

def camstream(cam, wide=480, high=320):
    # Set Window Size
    window_size = str(wide) + "x" + str(high)

    # Build Tkinter Window
    window = tk.Tk()
    window.title("Model Inference App")
    window.geometry(window_size)

    # Build Label to Show Image
    label = tk.Label(window)
    label.pack()

    # Build Button Frame
    button_frame = tk.Frame(window)
    button_frame.place(relx=0.5, rely=0.9, anchor='center')

    # Build Capture Button
    button_capture = tk.Button(button_frame, text="Capture", command=lambda: capture_image((wide, high), cam, window))
    button_capture.pack(side="left", expand=True)

    # Build Thread to Update Image
    thread = Thread(target=viewfinder, kwargs={'frame_size': (wide, high), 'cam': cam, 'label': label})
    thread.start()

    # Mainloop Tkinter Window
    window.mainloop()

    # Close Camera Connection and Stop Script
    cam.release()
    os._exit(0)
