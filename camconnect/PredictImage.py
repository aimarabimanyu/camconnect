import cv2
from Window import WindowClass
import tkinter as tk
from PIL import Image, ImageTk

class PredictImage(WindowClass):
    def __init__(self, cam, width, height, save_image=True, window_name="Predict Image", inference_model=lambda frame: (globals().update({'frame_var': frame}), "Model Not Loaded")[1]):

        """
        Constructor for CaptureImage Class.

        Attributes:
            cam: cv2.VideoCapture
                Camera Object to Stream Video
            width: int
                Width of the Window
            height: int
                Height of the Window
            window_name: str, default "Capture Image"
                Name of the Window
            filename: str, default "captured_image.jpg"
                Name of the Captured Image

        Returns:
            None
        """

        super().__init__(cam, width, height, window_name)
        self.button_frame = tk.Frame(self.window)
        self.button_frame.place(relx=0.5, rely=0.9, anchor='center')
        self.button_capture = tk.Button(self.button_frame, text="Predict", command=lambda: self.predict_image())
        self.button_capture.pack(side="left", expand=True)
        self.inference_model = inference_model
        self.save_image = save_image

    def predict_image(self):

        """
        Function to Capture Image from Camera.

        Attributes:
            None

        Returns:
            None
        """

        ret, frame = self.cam.read()
        if ret:
            result = self.inference_model(frame)
            frame = cv2.resize(frame, (self.width, self.height))
            new_window = tk.Toplevel(self.window)
            new_label = tk.Label(new_window)
            new_label.pack()
            image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            image = ImageTk.PhotoImage(image)
            new_label.config(image=image)
            new_label.image = image
            if self.save_image:
                cv2.imwrite(result + ".jpg", frame)
            result_label = tk.Label(new_window, text=str(result))
            result_label.pack()

PredictImage(cv2.VideoCapture(0), 480, 320).run()
