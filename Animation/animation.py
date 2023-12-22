import os
from .frame import Frame

class Animation:
    index = 0
    DEFAULT_SPEED = 1
    iterations = 0
    FINISHED_FLAG = False

    def __init__(
        self, name, path, speed=DEFAULT_SPEED, reverse=False, end=9999, start=0
    ):
        self.name = name
        self.path = path
        self.speed = float(speed)
        self.reverse = reverse
        self.discover_files()
        self.end = min(int(end), len(self.files) - 1)
        self.start = int(start)
        self.frame_count = self.end - self.start + 1

    def __repr__(self):
        return f"<Animation: {self.name}>"

    def discover_files(self):
        files = os.listdir(self.path)
        files.sort()
        if self.reverse:
            files.reverse()
        self.files = files

    def get_frame(self):
        index = int(self.index) % self.frame_count
        frame = Frame(os.path.join(self.path, self.files[index]))

        self.index += self.speed

        try:
            end = int(self.files[-1].split(".")[0])
        except ValueError:
            end = self.end

        if self.index >= self.end:
            self.iterations += 1
            self.FINISHED_FLAG = True
        else:
            self.FINISHED_FLAG = False

        return frame

    def get_nth_frame(self, n):
        return Frame(os.path.join(self.path, self.files[n]))

    def reset(self):
        self.index = self.start
        self.FINISHED_FLAG = False

    def hard_reset(self):
        self.reset()
        self.iterations = 0

    def reverse_animation(self):
        self.reverse = not self.reverse
        self.discover_files()

