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
            if not self.normal_image:
                self.normal_image = self.load_image(self.normal_path)

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

    def update(self):
        super().update()
        if self.is_hovered and self.hover_image:
            self.switch_image(self.hover_image)
        elif self.normal_image:
            self.switch_image(self.normal_image)

    def switch_image(self, image):
        self.image = image
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def event(self, event):
        print("EVENT got called")
        if event.type == pygame.MOUSEBUTTONUP:
            if self.is_hovered and self.callback:
                self.callback()


    def apply_scale(self):
        self.width = int(self.width * self.scale)
        self.height = int(self.height * self.scale)
        if self.image:
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        if self.normal_image:
            self.normal_image = pygame.transform.scale(self.normal_image, (self.width, self.height))
        if self.hover_image:
            self.hover_image = pygame.transform.scale(self.hover_image, (self.width, self.height))