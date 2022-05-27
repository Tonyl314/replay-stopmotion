import time
from pynput import keyboard

class Capturer:
    def __init__(self, capture_name=None):
        self.capture = None
        self.capture_name = capture_name
        self.start_listening()

    @property
    def is_capturing(self):
        return self.capture is not None

    def start_listening(self):
        with keyboard.Listener(on_press=self.on_press) as listener:
            listener.join()

    def start_capturing(self):
        if self.is_capturing:
            return
        self.capture = Capture(self.capture_name)
        print("Capturing started.")

    def end_capturing(self):
        if not self.is_capturing:
            return
        self.capture.save()
        self.capture = None
        print("Capturing ended, capture saved.")

    def on_press(self, key):
        # special keys
        if key == keyboard.Key.home:
            self.start_capturing()
        if key == keyboard.Key.end:
            self.end_capturing()
        if key == keyboard.Key.delete:
            return False
        # alphanumeric
        if type(key) != keyboard.KeyCode:
            return # not an alphanumeric key
        if not self.is_capturing:
            return
        if key.char == "l":
            self.capture.snap()
            print("Snap!")


class Capture:
    EXTENSION = ".capture"
    # the file contains timestamps separated by commas

    @classmethod
    def load(cls, name):
        capture = cls(name)
        with open(name+cls.EXTENSION, "r") as file:
            # we make it a tuple so that no timestamps can be accidentally added
            capture.timestamps = tuple(map(float,file.read().split(",")))
        return capture

    def __init__(self, name=None):
        self.start_time = time.time()
        self.timestamps = []
        if name is None:
            name = str(time.time())
        self.name = name

    def snap(self):
        self.timestamps.append(time.time() - self.start_time)

    def save(self):
        with open(self.name+self.EXTENSION, "w") as file:
            file.write(",".join(map(str,self.timestamps)))


if __name__ == "__main__":
    capturer = Capturer(input("Enter the capture name:"))