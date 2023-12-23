import pygame
from .ui_element import UIElement
from .button import Button


class UIGroup:
    _right = 0

    def __init__(
        self,
        elements: [UIElement | Button] = None,
        background: UIElement | Button = None,
        x=0,
        y=0,
        right=None,
        padding_x=0,
        padding_y=0,
        space_x=0,
        space_y=0,
        scale=1,
    ):
        self.background = background
        self.elements = elements or []

        self.x = x
        self.y = y
        self.padding_x = padding_x
        self.padding_y = padding_y
        self.space_x = space_x
        self.space_y = space_y

        self.init_dimensions()

        self.scale = scale
        self.apply_scale()


        if right:
            self.right = right

        self.position()

    def add(self, element):
        self.elements.append(element)

    def remove(self, element):
        self.elements.remove(element)

    def update(self):
        for element in self.elements:
            element.update()

    def apply_scale(self):
        self.width = int(self.width * self.scale)
        self.height = int(self.height * self.scale)

        if self.background:
            self.background.scale = self.scale
            self.background.apply_scale()

        for element in self.elements:
            element.scale = self.scale
            element.apply_scale()

        self.position()


    def draw(self, screen, elements=None):
        if self.background:
            self.background.draw(screen)

        elements = elements or self.elements
        for element in elements:
            element.draw(screen)

    def event(self, event):
        for element in self.elements:
            if hasattr(element, "event"):
                element.event(event)

    def stack_vertical(self, elements=None, align="center"):

        y = self.y + self.padding_y

        elements = elements or self.elements

        for element in elements:

            if align == "center":
                buffer = (self.width - element.width) /2
            elif align == "right":
                buffer = self.width - element.width
            elif align == "left":
                buffer = 0
            else :
                raise ValueError("align must be either 'center', 'right' or 'left'")

            element.set_y(y)
            element.set_x(self.x + self.padding_x + buffer)
            y += element.height + self.space_y

    def stack_horizontal(self, elements=None, align="center"):

        x = self.x + self.padding_x

        elements = elements or self.elements

        for element in elements:

            if align == "center":
                buffer = (self.height - element.height) /2
            elif align == "bottom":
                buffer = self.height - element.height
            elif align == "top":
                buffer = 0

            element.set_x(x)
            element.set_y(self.y + self.padding_y + buffer)
            x += element.width + self.space_x

    def stack_over(self, elements=None):
        elements = elements or self.elements

        for element in elements:
            element.set_x(self.x + self.padding_x)
            element.set_y(self.y + self.padding_y)

    def position(self):
        self.position_background()

    def position_background(self):
        if not self.background:
            return
        self.background.set_x(self.x)
        self.background.set_y(self.y)

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, value):
        self._right = float(value)
        self.x = pygame.display.get_surface().get_width() - self._right - self.width

    def init_dimensions(self):
        if self.background:
            self.width = self.background.width
            self.height = self.background.height
        else:
            if self.elements:
                self.width = max([element.width for element in self.elements])
                self.height = sum([element.height for element in self.elements])
            else:
                self.width = 0
                self.height = 0

    def set_right(self, value):
        for element in self.elements:
            element.right = value

    def set_x(self, value):
        for element in self.elements:
            element.x = value

    def set_y(self, value):
        for element in self.elements:
            element.y = value

    def center(self):
        self.x = pygame.display.get_surface().get_width() / 2 - self.total_width / 2
        self.y = pygame.display.get_surface().get_height() / 2 - self.total_height / 2
        self.position()

    @property
    def rect(self):
        elements = self.elements
        if self.background:
            elements.append(self.background)

        xs = {element.x: element for element in elements}
        ys = {element.y: element for element in elements}

        max_x = max(xs.keys())
        min_x = min(xs.keys())

        max_y = max(ys.keys())
        min_y = min(ys.keys())

        width = max_x - min_x + xs[max_x].width + self.padding_x * 2
        height = max_y - min_y + ys[max_y].height + self.padding_y * 2

        x = min_x - self.padding_x
        y = min_y - self.padding_y

        return pygame.Rect(x, y, width, height)
