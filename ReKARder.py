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
required_modules = ["tkinter", "pygetwindow", "pyautogui", "opencv-python", "numpy", "pyaudio", "pydub"]

install_modules(required_modules)

import tkinter as tk
from tkinter import ttk, filedialog
import pygetwindow as gw
import pyautogui
from PIL import ImageGrab
import cv2
import numpy as np
import pyaudio
from pydub import AudioSegment

class DesktopRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("ReKARder")

        # Frame rate options
        self.frame_rate_options = [15, 30, 60]
        self.selected_frame_rate = tk.StringVar(value=str(self.frame_rate_options[2]))

        # Bitrate options (in kbps)
        self.bitrate_options = [2000, 5000, 8000]
        self.selected_bitrate = tk.StringVar(value=str(self.bitrate_options[1]))

        # Audio recording options
        self.audio_recording_var = tk.BooleanVar(value=True)  # Set to True for default selection

        # Video file location
        self.video_file_location = tk.StringVar(value="recording.mp4")

        # UI elements
        self.start_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.frame_rate_label = tk.Label(root, text="Frame Rate:")
        self.frame_rate_label.pack(pady=5)

        self.frame_rate_dropdown = ttk.Combobox(root, textvariable=self.selected_frame_rate, values=self.frame_rate_options)
        self.frame_rate_dropdown.pack(pady=5)

        self.bitrate_label = tk.Label(root, text="Bitrate (kbps):")
        self.bitrate_label.pack(pady=5)

        self.bitrate_dropdown = ttk.Combobox(root, textvariable=self.selected_bitrate, values=self.bitrate_options)
        self.bitrate_dropdown.pack(pady=5)

        self.audio_checkbox = tk.Checkbutton(root, text="Record Audio", variable=self.audio_recording_var, onvalue=True, offvalue=False)
        self.audio_checkbox.select()  # This sets the checkbox to be selected by default
        self.audio_checkbox.pack(pady=5)

        self.video_location_label = tk.Label(root, text="Video File Location:")
        self.video_location_label.pack(pady=5)

        self.video_location_entry = tk.Entry(root, textvariable=self.video_file_location, state="readonly")
        self.video_location_entry.pack(pady=5, padx=10, fill="x")

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_video_location)
        self.browse_button.pack(pady=5)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Recording variables
        self.recording = False
        self.video_writer = None
        self.audio_stream = None
        self.audio_frames = []

    def start_recording(self):
        self.recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        screen_width, screen_height = pyautogui.size()
        selected_fps = int(self.selected_frame_rate.get())
        selected_bitrate = int(self.selected_bitrate.get())
        video_file_location = self.video_file_location.get()

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.video_writer = cv2.VideoWriter(video_file_location, fourcc, selected_fps, (screen_width, screen_height))

        if self.audio_recording_var.get():
            self.start_audio_recording()

        self.video_writer.set(cv2.CAP_PROP_FPS, selected_fps)
        self.video_writer.set(cv2.CAP_PROP_BITRATE, selected_bitrate * 1000)  # Set bitrate in kbps

        self.record_screen()

    def stop_recording(self):
        self.recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        if self.video_writer:
            self.video_writer.release()

        if self.audio_recording_var.get():
            self.stop_audio_recording()

    def start_audio_recording(self):
        audio_format = pyaudio.paInt16
        channels = 2
        rate = 44100
        chunk = 1024

        self.audio_stream = pyaudio.PyAudio().open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

    def stop_audio_recording(self):
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()

    def record_screen(self):
        while self.recording:
            screenshot = ImageGrab.grab()
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            self.video_writer.write(frame)

            if self.audio_recording_var.get():
                audio_frame = self.audio_stream.read(1024)
                self.audio_frames.append(audio_frame)

            self.root.update()

    def on_closing(self):
        if self.recording:
            self.recording = False
        self.root.destroy()

    def browse_video_location(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4")])
        if file_path:
            self.video_file_location.set(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopRecorder(root)
    root.mainloop()
