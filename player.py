import pygame
from animation import Animation

class Player(pygame.sprite.Sprite):
    animations = {
        "idle": Animation("idle", "C:\\Users\\BigBoss\\Desktop\\zombie\\idle", loop=True),
        "idle_to_walk": Animation("idle_to_walk", "C:\\Users\\BigBoss\\Desktop\\zombie\\idle to walk", loop=True),
        "walk": Animation("walk", "C:\\Users\\BigBoss\\Desktop\\zombie\\walk"),
        "walk_inverse": Animation("walk_inverse", "C:\\Users\\BigBoss\\Desktop\\zombie\\walk", inverse=True),
        "attack": Animation("attack", "C:\\Users\\BigBoss\\Desktop\\zombie\\attack"),
    }
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
    @property
    def image(self):
        frame = self.animation_object.generator().__next__()
        print('frame: ', frame)
        return frame.image

    @property
    def animation_object(self):
        return self.animations[self.animation]

    def update(self):
        self.rect.x += self.speed
        if self.animation_object.ENDED:
            print('*'*20)
            print('animation: ', self.animation, ' ended')
            print('*'*20)


        # if self.rect.x > self.director.width:
        #     self.rect.x = -self.width
        # if self.rect.x < -self.width:
        #     self.rect.x = self.director.width

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.speed = -2
                self.set_animation("walk_inverse")
            if event.key == pygame.K_RIGHT:
                self.speed = 2
                self.set_animation("walk")
            if event.key == pygame.K_SPACE:
                self.set_animation("attack")
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.speed = 0
                self.set_animation("idle")
            if event.key == pygame.K_RIGHT:
                self.speed = 0
                self.set_animation("idle")

        if event.type == pygame.VIDEORESIZE:
            self.scale(self.director.scale)
    def scale(self, window_scale):
        print(window_scale)
        self.rect = pygame.Rect((self.rect.x*window_scale, self.rect.y*window_scale), (self.rect.width*window_scale, self.rect.height*window_scale))
        self.image = pygame.transform.scale(
            self.image,
            (int(self.width*window_scale), int(self.height*window_scale))
        )

    def set_animation(self, animation):
        if animation == self.animation:
            return
        self.animation = animation
        self.animation_object.reset()
