import pygame


class UIElement:
    _right = 0

    def __init__(
        self, x=0, y=0, image=None, path=None, right=None, width=None, height=None, scale=1
    ):
        if path:
            self.path = path

        if not image:
            if not path:
                raise ValueError(
                    "UIElement must be initialized with either an image or a path"
                )
            self.image = self.load_image(path)
        else:
            self.image = image

        if not width:
            self.width = self.image.get_width()

        if not height:
            self.height = self.image.get_height()

        self.x = x
        self.y = y
        self.right = right
        self.scale = scale
        self.apply_scale()

    def update(self):
        pass

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def load_image(self, path):
        return pygame.image.load(path)

    def apply_scale(self):
        self.width = int(self.width * self.scale)
        self.height = int(self.height * self.scale)

        self.image = pygame.transform.scale(self.image, (self.width, self.height))


    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, value):
        if value is None:
            return
        self._right = value
        self.x = pygame.display.get_surface().get_width() - self._right - self.width

    def set_right(self, value):
        self.right = value

    def set_x(self, value):
        self.x = value

    def set_y(self, value):
        self.y = value