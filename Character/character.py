import pygame


class Character(pygame.sprite.Sprite):
    moving = False
    max_health = 100
    health = max_health
    DEAD = False

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
        **kwargs,
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

        if not width:
            self.width = self.image.get_width()
        if not height:
            self.height = self.image.get_height()

        self.x_speed = 0
        self.y_speed = 0

    @property
    def image(self):
        if self.DEAD:
            return self.animation.active_animation.get_nth_frame(-1).image
        frame = self.animation.update()
        image = frame.image
        # print(f"{'.'.join(frame.path.split('/'))}: ", frame)

        if self.direction == -1:
            image = pygame.transform.flip(image, True, False)

        if self.width and self.height:
            return pygame.transform.scale(image, (self.width, self.height))
        return image

    def update(self):
        self.apply_movement()

    def apply_movement(self):
        if self.moving:
            self.rect.x += self.x_speed
            self.rect.y += self.y_speed

    def event(self, event):
        pass

    def get_hit(self, damage):
        self.health -= damage
