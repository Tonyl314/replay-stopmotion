import time
import os
from pynput import keyboard

class Capturer:
    ALPHANUMERIC_SNAP_KEY = "f"

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
        if key.char == self.ALPHANUMERIC_SNAP_KEY:
            self.capture.snap()
            print("Snap!")

    @classmethod
    def load_snap_key(cls):
        try:
            with open("snap_key.txt") as file:
                char = file.read().strip()
            if len(char) != 1 or not char.isalnum():
                print("Couldn't load snap key: must be a single alphanumeric character.")
            else:
                cls.ALPHANUMERIC_SNAP_KEY = char.lower()
        except:
            pass # default

    @classmethod
    def print_help_message(cls):
        snap_key = cls.ALPHANUMERIC_SNAP_KEY.upper()
        print(f"""CAPTURER – create captures with frame timings
Default controls:
    Home: start a new capture
    {snap_key} key: snap a frame
    End: stop and save
    Delete: terminate the program""")


class Capture:
    EXTENSION = ".capture"
    # the file contains timestamps separated by commas

    @classmethod
    def load(cls, name):
        capture = cls(name)
        if not os.path.exists(capture.get_path()):
            input(f"Couldn't load capture {name} as it doesn't exist. Press enter to quit.")
            quit()
        with open(capture.get_path(), "r") as file:
            # we make it a tuple so that no timestamps can be accidentally added
            capture.timestamps = tuple(map(float,file.read().split(",")))
        return capture

    def __init__(self, inputted_name=None):
        self.start_time = time.time()
        self.timestamps = []
        self.folders = self.extract_folders(inputted_name)
        self.name = self.extract_name(inputted_name)
        if not self.name:
            self.name = self.generate_name()

    def snap(self):
        self.timestamps.append(time.time() - self.start_time)

    def save(self):
        if not os.path.exists(self.get_folder_path()):
            os.makedirs(self.get_folder_path())
        with open(self.get_path(), "w") as file:
            file.write(",".join(map(str,self.timestamps)))

    def generate_name(self):
        return str(time.time())

    def get_path(self):
        if self.folders and not os.path.exists(self.folders):
            os.makedirs(self.folders)
        return f"{self.folders}{self.name}\\{self.name}{self.EXTENSION}"

    def get_folder_path(self):
        return f"{self.folders}{self.name}"

    def extract_folders(self, inputted_name):
        if "\\" not in inputted_name:
            return ""
        backslash_pos = inputted_name.rfind("\\")
        return inputted_name[:backslash_pos+1]

    def extract_name(self, inputted_name):
        if "\\" not in inputted_name:
            return inputted_name
        backslash_pos = inputted_name.rfind("\\")
        return inputted_name[backslash_pos+1:]

if __name__ == "__main__":
    Capturer.load_snap_key()
    Capturer.print_help_message()
    capturer = Capturer(input("Enter a new capture name:"))