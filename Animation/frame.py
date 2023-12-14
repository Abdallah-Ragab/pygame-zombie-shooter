import os

import pygame


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
