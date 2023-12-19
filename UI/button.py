import pygame
from .ui_element import UIElement


class Button(UIElement):
    def __init__(self, x=0, y=0, image=None, path=None, right=None, width=None, height=None, callback=None):
        super().__init__(x, y, image, path, right, width, height)
        self.callback = callback

    @property
    def is_hovered(self):
        mouse = pygame.mouse.get_pos()
        if self.x < mouse[0] < self.x + self.width:
            if self.y < mouse[1] < self.y + self.height:
                return True
        return False

    @property
    def is_clicked(self):
        if self.is_hovered:
            if pygame.mouse.get_pressed()[0]:
                return True
        return False

    def update(self):
        super().update()
        if self.is_clicked and self.callback:
            self.callback()