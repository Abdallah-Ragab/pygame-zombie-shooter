import pygame
from .ui_element import UIElement


class Button(UIElement):

    normal_image = None
    hover_image = None
    normal_path = None
    hover_path= None

    def __init__(self, x=0, y=0, image=None, path=None, right=None, width=None, height=None, scale=1, callback=None):
        if isinstance(image, list):
            self.normal_image = image[0]
            self.hover_image = image[1]
            image = self.normal_image
        if isinstance(path, list):
            self.normal_path = path[0]
            self.hover_path = path[1]

            if not self.hover_image:
                self.hover_image = self.load_image(self.hover_path)

            path = self.normal_path

        super().__init__(x, y, image, path, right, width, height, scale)
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
        if self.is_hovered and self.hover_image:
            self.image = self.hover_image
        else:
            self.image = self.normal_image