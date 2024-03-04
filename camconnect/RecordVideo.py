import cv2
from Window import WindowClass
import tkinter as tk
import threading

class RecordVideo(WindowClass):
    def __init__(self, cam, width, height, window_name="Record Video", filename="recorded_video.avi"):

        """
        Constructor for RecordVideo Class.

        Attributes:
            cam: cv2.VideoCapture
                Camera Object to Stream Video
            width: int
                Width of the Window
            height: int
                Height of the Window
            window_name: str, default "Record Video"
                Name of the Window
            filename: str, default "recorded_video.avi"
                Name of the Recorded Video

        Returns:
            None
        """

        super().__init__(cam, width, height, window_name)
        self.filename = filename
        self.button_frame = tk.Frame(self.window)
        self.button_frame.place(relx=0.5, rely=0.9, anchor='center')
        self.button_record = tk.Button(self.button_frame, text="Record", command=lambda: self.record_video_process())
        self.button_record.pack(side="left", expand=True)
        self.button_stop = tk.Button(self.button_frame, text="Stop", command=lambda: self.stop_recording())
        self.button_stop.pack(side="right", expand=True)
        self.status_label = tk.Label(self.window, text="")
        self.status_label.place(relx=0.9, rely=0.1, anchor='center')

    def record_video_process(self):

        """
        Function to Start Recording Video with Thread.

        Arguments:
            None

        Returns:
            None
        """

        self.recording_thread = threading.Thread(target=self.record_video)
        self.recording_thread.start()

    def record_video(self):

        """
        Function to Record Video from Camera.

        Attributes:
            None

        Returns:
            None
        """

        self.result = cv2.VideoWriter(self.filename, cv2.VideoWriter_fourcc(*'XVID'), 20, (int(self.cam.get(3)), int(self.cam.get(4))))
        self.status_label.config(text="Recording...")
        while True:
            ret, frame = self.cam.read()
            if ret:
                self.result.write(frame)

    def stop_recording(self):

        """
        Function to Stop Recording Video.

        Attributes:
            None

        Returns:
            None
        """

        self.result.release()
        self.status_label.config(text="Recording Stopped")
