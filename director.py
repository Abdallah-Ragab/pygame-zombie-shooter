import pygame
import sys
from fractions import Fraction

class Director:
    def __init__(self):
        self.width = 1280
        self.height = 720
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        self.aspect_ratio = Fraction(self.screen.get_width(), self.screen.get_height())
        self.scale = 1

        print(self.aspect_ratio)

        self.title = "Game Name"
        self.scene = None
        self.quit_flag = False
        self.clock = pygame.time.Clock()

    def setup(self):
        pygame.display.set_caption(self.title)


    def loop(self):
        while not self.quit_flag:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    self.aspect_ratio_resize(event.w, event.h)
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.quit()
                self.scene.event(event)  # Call event with the event
            self.scene.update()
            self.scene.draw(self.screen, self.scale)
            pygame.display.update()

    def set_scene(self, scene):
        self.scene = scene

    def aspect_ratio_resize(self, event_width, event_height):
        delta_width = (event_width - self.screen.get_width())/self.aspect_ratio.numerator
        delta_height = (event_height - self.screen.get_height())/self.aspect_ratio.denominator

        print(delta_width, delta_height)

        width_factor = event_width / self.width
        height_factor = event_height / self.height
        self.scale = min(width_factor, height_factor)
        new_width = int(self.width * self.scale)
        new_height = int(self.height * self.scale)
        self.screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)

    def quit(self):
        self.quit_flag = True

class Scene:
    def __init__(self, director):
        self.director = director

    def scale(self):
        scale = self.director.scale
        for surface in self.surfaces:
            surface = pygame.transform.scale(surface, (int(surface.get_width()*scale), int(surface.get_height()*scale)))
        for rect in self.rects:
            rect = pygame.Rect((rect.x*scale, rect.y*scale), (rect.width*scale, rect.height*scale))
        for font in self.fonts:
            font = pygame.font.Font(font.font, int(font.size*scale))
        for text in self.texts:
            text = font.render(text.text, True, text.color)

    def update(self):
        raise NotImplementedError("update abstract method must be defined in subclass.")

    def event(self, event):
        raise NotImplementedError("event abstract method must be defined in subclass.")

    def draw(self, screen, scale):
        raise NotImplementedError("draw abstract method must be defined in subclass.")
