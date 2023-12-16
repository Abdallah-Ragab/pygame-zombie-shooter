import pygame


class Character(pygame.sprite.Sprite):
    moving = False

    def __init__(
        self,
        scene,
        x,
        y,
        height=None,
        width=None,
        speed: tuple = (1, 1),
        direction: int = 1,
        *args,
        **kwargs
    ):
        super().__init__()

        self.scene = scene
        self.speed = speed
        self.height = height
        self.width = width
        self.direction = direction

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        if not self.width:
            self.width = frame.image.get_width()
        if not self.height:
            self.height = frame.image.get_height()

        self.x_speed = 0
        self.y_speed = 0

    @property
    def image(self):
        frame = self.animation.update()
        print("frame: ", frame)


        if self.direction == -1:
            return pygame.transform.flip(frame.image, True, False)

        return pygame.transform.scale(frame.image, (self.width, self.height))

    def update(self):
        self.apply_movement()

    def apply_movement(self):
        if self.moving:
            self.rect.x += self.x_speed
            self.rect.y += self.y_speed

    def event(self, event):
        pass
