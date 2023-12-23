import pygame


class Scene:
    def __init__(self, director):
        self.director = director
        self.setup()

    def scale(self):
        scale = self.director.scale
        for surface in self.surfaces:
            surface = pygame.transform.scale(
                surface,
                (int(surface.get_width() * scale), int(surface.get_height() * scale)),
            )
        for rect in self.rects:
            rect = pygame.Rect(
                (rect.x * scale, rect.y * scale),
                (rect.width * scale, rect.height * scale),
            )
        for font in self.fonts:
            font = pygame.font.Font(font.font, int(font.size * scale))
        for text in self.texts:
            text = font.render(text.text, True, text.color)

    def update(self):
        raise NotImplementedError("update abstract method must be defined in subclass.")

    def event(self, event):
        raise NotImplementedError("event abstract method must be defined in subclass.")

    def draw(self, screen, scale):
        raise NotImplementedError("draw abstract method must be defined in subclass.")

    def setup(self):
        raise NotImplementedError("setup abstract method must be defined in subclass.")