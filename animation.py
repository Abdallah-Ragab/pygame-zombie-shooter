import os
import pygame


class AnimationSequence:
    _sequence = []

    def __init__(self, name, loop=False, repeat_last=False):
        self.name = name
        self.loop = loop
        self.repeat_last = repeat_last

    def add(self, animation, repeats=1):
        for i in range(repeats):
            self._sequence.append(animation)

    @property
    def sequence(self):
        return self._sequence

    def generator(self):
        for idx, animation in enumerate(self._sequence):
            while not animation.ENDED:
                yield animation.generator().__next__()
            animation.reset()

            if idx == len(self._sequence) - 1 and self.repeat_last:
                while True:
                    yield animation.generator().__next__()


class AnimationManager:
    def __init__(self, animations: dict, default_animation=None):
        self.animations = animations
        self.default_animation = default_animation
        self.queue = []

    def add_animation(self, name, animation):
        self.animations[name] = animation

    def play_animation(self, animation_name):
        if animation_name in self.animations.keys():
            self.queue.append(animation_name)
        else:
            raise ValueError(f"No animation found with name '{animation_name}'")

    @property
    def active_animation(self):
        if self.queue:
            return self.animations[self.queue.pop(0)]
        elif self.default_animation:
            return self.animations[self.default_animation]

    def frame(self):
        if self.current_animation:
            return self.active_animation.generator().__next__()
        else:
            return None



class Animation:
    DEFAULT_SPEED = 1

    def __init__(self, name, dir, loop=False, speed = DEFAULT_SPEED, end=None, start=None, inverse=False):
        self.name = name
        self.dir = dir
        self.speed = float(speed)
        self.inverse = inverse
        self.loop = loop

        self.files = os.listdir(self.dir)
        self.files.sort()
        if inverse:
            self.files.reverse()

        self.end = int(end) if end else len(self.files) - 1
        self.start = int(start) if start else 0
        self.index = self.start

    def generator(self):
        while self.index <= self.end:
            self.index += self.speed
            yield Frame(dir=self.dir, file=self.files[self.index], name=self.name)

    @property
    def ENDED(self):
        return self.index >= self.end

    def reset(self):
        self.index = self.start

class Frame:
    def __init__(self, path=None, dir=None, file=None, name=None):
        self._name = name
        if path:
            self.dir = os.path.dirname(path)
            self.file = os.path.basename(path)
        else:
            self.dir = dir
            self.file = file

        if not self.dir:
            raise ValueError("No directory specified")
        if not self.file:
            raise ValueError("No file specified")

        self.file_name = self.file.split(".")[0]


    @property
    def z_index(self):
        return str(self.index).zfill(4)

    @property
    def name(self):
        if self._name:
            return self._name

        if self.dir[-1] == "/" or self.dir[-1] == "\\":
            self.dir = self.dir[:-1]
        if "/" in self.dir:
            return self.dir.split("/")[-1]
        else:
            return self.dir.split("\\")[-1]

    @property
    def index(self):
        return int(self.file_name)

    @property
    def path(self):
        return os.path.join(self.dir, self.file)

    @property
    def image(self):
        return pygame.image.load(self.path)


    def __repr__(self):
        return f"{self.name}.{self.z_index}"
