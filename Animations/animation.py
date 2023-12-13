
import os
from .frame import Frame


class Animation:
    DEFAULT_SPEED = 1

    def __init__(self, name, dir, speed = DEFAULT_SPEED, end=None, start=None, inverse=False, loop=False):
        self.name = name
        self.dir = dir
        self.speed = float(speed)
        self.inverse = inverse
        self.loop = loop

        self.files = os.listdir(self.dir)
        self.files.sort()
        if self.inverse:
            self.files.reverse()

        self.end = int(end) if end else len(self.files) - 1
        self.start = int(start) if start else 0
        self.index = self.start

    def generator(self):
        while not self.END_FLAG:
            self.index += self.speed
            self.index = int(self.index)
            print("start: ", self.start, "end: ", self.end, "index: ", self.index, "END: ", self.END_FLAG)
            yield Frame(dir=self.dir, file=self.files[self.index], name=self.name)


    @property
    def END_FLAG(self):
        return self.index >= self.end

    @property
    def PRE_END_FLAG(self):
        return self.index >= self.end - 1

    def reset(self):
        self.index = self.start

    def skip(self):
        pass