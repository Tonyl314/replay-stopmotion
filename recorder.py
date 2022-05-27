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
        if not os.path.exists(self.capture.name):
            os.mkdir(self.capture.name) # this is where the frames are saved
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
                filename = self.make_four_digit(i) + ".png"
                print(sct.shot(mon=0, output=f"{self.capture.name}\\{filename}"))
        self.is_recording = False
        print("Recording ended.")

    def export_video(self, framerate):
        input_filenames = f"{self.capture.name}\\%04d{self.IMAGE_EXTENSION}"
        output_filename = f"{self.capture.name}\\video{self.VIDEO_EXTENSION}"
        os.system(f"ffmpeg -framerate {framerate} -i {input_filenames} {output_filename}")
        print("Video exported.")

    def make_four_digit(self, number):
        digits = str(number)
        digits = (4-len(digits))*"0" + digits
        return digits


if __name__ == "__main__":
    recorder = Recorder()
    recorder.prepare(input("Enter the capture name:"))
