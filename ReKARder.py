import importlib
import subprocess

def install_modules(module_names):
    for module_name in module_names:
        try:
            importlib.import_module(module_name)
            print(f"{module_name} is already installed.")
        except ImportError:
            print(f"{module_name} not found. Installing...")
            subprocess.call(["pip", "install", module_name])
            print(f"{module_name} installed successfully.")

# Example usage:
required_module = ["tkinter", "pygetwindow", "pyautogui", "opencv-python", "numpy"]

install_modules(required_module)

# Now you can import the module without any issues
#import example_module

import tkinter as tk
from tkinter import ttk
import pygetwindow as gw
import pyautogui
from PIL import ImageGrab
import cv2
import numpy as np

class DesktopRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("ReKARder")

        # Frame rate options
        self.frame_rate_options = [15, 30, 60]  # Add more frame rates if needed
        self.selected_frame_rate = tk.StringVar(value=str(self.frame_rate_options[0]))

        # UI elements
        self.start_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.frame_rate_label = tk.Label(root, text="Frame Rate:")
        self.frame_rate_label.pack(pady=5)

        self.frame_rate_dropdown = ttk.Combobox(root, textvariable=self.selected_frame_rate, values=self.frame_rate_options)
        self.frame_rate_dropdown.pack(pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Recording variables
        self.recording = False
        self.video_writer = None

    def start_recording(self):
        self.recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        screen_width, screen_height = pyautogui.size()
        selected_fps = int(self.selected_frame_rate.get())
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.video_writer = cv2.VideoWriter("recording.mp4", fourcc, selected_fps, (screen_width, screen_height))

        self.record_screen()

    def stop_recording(self):
        self.recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        if self.video_writer:
            self.video_writer.release()

    def record_screen(self):
        while self.recording:
            screenshot = ImageGrab.grab()
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            self.video_writer.write(frame)
            self.root.update()

    def on_closing(self):
        if self.recording:
            self.recording = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopRecorder(root)
    root.mainloop()
