import pygame
from Animations import Animation, AnimationSequence, AnimationManager

PRESSED_KEYS = []

class Player(pygame.sprite.Sprite):
    animation_manager = AnimationManager(
        animations={
            "idle": Animation("idle", "C:\\Users\\BigBoss\\Desktop\\zombie\\idle"),
            "idle_walk_idle" : AnimationSequence(
                                    name="idle_walk_idle",
                                    animations=[
                                        Animation("idle_to_walk", "C:\\Users\\BigBoss\\Desktop\\zombie\\idle to walk"),
                                        Animation("walk", "C:\\Users\\BigBoss\\Desktop\\zombie\\walk", loop=True),
                                        Animation("walk_to_idle", "C:\\Users\\BigBoss\\Desktop\\zombie\\idle to walk", inverse=True),
                                    ],
                                ),
            "attack": Animation("attack", "C:\\Users\\BigBoss\\Desktop\\zombie\\attack"),
        },
        default_animation="idle",
    )

    base_speed = 2

    def __init__(self, x, y, width, height, color, speed, director):
        super().__init__()

        self.animation = "idle"

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.director = director
        self.width = width
        self.height = height

        self.x_speed = 0


    @property
    def image(self):
        frame = self.animation_manager.frame().__next__()
        print('frame: ', frame)
        return frame.image

    def update(self):
        self.rect.x += self.x_speed

        if self.rect.x > self.director.width:
            self.rect.x = -self.width
        if self.rect.x < -self.width:
            self.rect.x = self.director.width

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print("left pressed")
                self.x_speed = -self.base_speed*self.speed
                self.animation_manager.play_animation("idle_walk_idle")
            if event.key == pygame.K_RIGHT:
                print("right pressed")
                self.x_speed = self.base_speed*self.speed
                self.animation_manager.play_animation("idle_walk_idle")
            if event.key == pygame.K_SPACE:
                self.animation_manager.play_animation("attack")

            PRESSED_KEYS.append(event.key)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                print("left released")
                self.x_speed = 0
                if event.key in PRESSED_KEYS and self.animation_manager.active_animation.name == "idle_walk_idle":
                    self.animation_manager.active_animation.skip()
            if event.key in PRESSED_KEYS and event.key == pygame.K_RIGHT:
                print("right released")
                self.x_speed = 0
                if self.animation_manager.active_animation.name == "idle_walk_idle":
                    if self.animation_manager.active_animation.active_animation.name == "idle_to_walk":
                        self.animation_manager.active_animation.skip(2)
                    elif self.animation_manager.active_animation.active_animation.name == "walk":
                        self.animation_manager.active_animation.skip(1)

            PRESSED_KEYS.remove(event.key)

        if event.type == pygame.VIDEORESIZE:
            self.scale(self.director.scale)
    def scale(self, window_scale):
        print(window_scale)
        self.rect = pygame.Rect((self.rect.x*window_scale, self.rect.y*window_scale), (self.rect.width*window_scale, self.rect.height*window_scale))
        self.image = pygame.transform.scale(
            self.image,
            (int(self.width*window_scale), int(self.height*window_scale))
        )
