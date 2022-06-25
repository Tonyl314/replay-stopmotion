import time
import os
from mss import mss
from pynput import keyboard
from capturer import Capture

class Recorder:
    IMAGE_EXTENSION = ".png"
    VIDEO_EXTENSION = ".mp4"
    # the recorder is prepared with a capture, then records on a set key press

    def __init__(self):
        self.capture = None
        self.is_recording = False

    def prepare(self, capture_name):
        self.capture = Capture.load(capture_name)
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

    def on_press(self, key):
        if key == keyboard.Key.home:
            self.record()
        if key == keyboard.Key.end:
            self.export_video(int(input("Choose a framerate:")))
        if key == keyboard.Key.delete:
            return False

    def record(self):
        if self.is_recording:
            return
        self.is_recording = True

        start_time = time.time()
        print("Recording started.")
        with mss() as sct:
            for i, snap_time in enumerate(self.capture.timestamps):
                while time.time()-start_time < snap_time:
                    pass
                filename = self.make_four_digit(i) + self.IMAGE_EXTENSION
                print(sct.shot(mon=0, output=f"{self.capture.get_folder_path()}\\{filename}"))
        self.is_recording = False
        print("Recording ended.")

    def export_video(self, framerate):
        print("Exporting video...")
        input_filenames = f"{self.capture.get_folder_path()}\\%04d{self.IMAGE_EXTENSION}"
        output_filename = f"{self.capture.get_folder_path()}\\video{self.VIDEO_EXTENSION}"
        os.system(f"ffmpeg -framerate {framerate} -i {input_filenames} {output_filename}")
        print("Exporting ended.")

    def make_four_digit(self, number):
        digits = str(number)
        digits = (4-len(digits))*"0" + digits
        return digits

    @staticmethod
    def print_help_message():
        print("""RECORDER – load captures to record replayed footage
Default controls:
    Home: record the screen (saves images)
    End: export to a video (requires FFMPEG installed and in PATH)
    Delete: terminate the program""")


if __name__ == "__main__":
    recorder = Recorder()
    recorder.print_help_message()
    recorder.prepare(input("Enter an existing capture name:"))
