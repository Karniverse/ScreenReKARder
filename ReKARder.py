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
required_module = ["tkinter", "pygetwindow", "pyautogui"]

install_modules(required_module)

# Now you can import the module without any issues
#import example_module



import tkinter as tk
import pygetwindow as gw
import pyautogui
from PIL import ImageGrab

class DesktopRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("Desktop Recorder")

        self.start_button = tk.Button(root, text="Start Recording", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.recording = False

    def start_recording(self):
        self.recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.record_screen()

    def stop_recording(self):
        self.recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def record_screen(self):
        while self.recording:
            screenshot = ImageGrab.grab()
            screenshot.save("recording.png")  # Save the screenshot (you can use a different format)
            self.root.update()

    def on_closing(self):
        if self.recording:
            self.recording = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopRecorder(root)
    root.mainloop()
