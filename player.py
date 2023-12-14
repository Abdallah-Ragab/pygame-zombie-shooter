import pygame
# from Animations import Animation, AnimationSequence, AnimationManager
from Animation import Animation, AnimationManager, SequenceAnimation, TransitionRule

PRESSED_KEYS = []

class Player(pygame.sprite.Sprite):
    base_x_speed = 2
    base_y_speed = 1

    def __init__(self, x, y, width, height, color, speed, director):
        super().__init__()

        self.director = director
        self.speed = speed
        self.width = width
        self.height = height

        # self.animation_manager = AnimationManager(
        #     animations={
        #         "idle": Animation("idle", "D:\\game assets\\\zombie\\idle"),
        #         "idle_walk_idle" : AnimationSequence(
        #                                 name="idle_walk_idle",
        #                                 animations=[
        #                                     Animation("idle_to_walk", "D:\\game assets\\\zombie\\idle to walk", speed=self.speed),
        #                                     Animation("walk", "D:\\game assets\\\zombie\\walk", speed=self.speed, loop=True),
        #                                     Animation("walk_to_idle", "D:\\game assets\\\zombie\\idle to walk", speed=self.speed, inverse=True),
        #                                 ],
        #                             ),
        #         "idle_walk_backwards_idle" : AnimationSequence(
        #                                 name="idle_walk_idle",
        #                                 animations=[
        #                                     Animation("idle_to_walk", "D:\\game assets\\\zombie\\idle to walk", speed=self.speed),
        #                                     Animation("walk", "D:\\game assets\\\zombie\\walk", speed=self.speed, loop=True, inverse=True),
        #                                     Animation("walk_to_idle", "D:\\game assets\\\zombie\\idle to walk", speed=self.speed, inverse=True),
        #                                 ],
        #                             ),
        #         "attack": Animation("attack", "D:\\game assets\\\zombie\\attack", speed=self.speed),
        #         "scream": Animation("scream", "D:\\game assets\\\zombie\\scream", speed=self.speed),
        #         "scream_run": AnimationSequence(
        #             name="scream_run",
        #             animations=[
        #                 Animation("scream", "D:\\game assets\\\zombie\\scream"),
        #                 Animation("run", "D:\\game assets\\\zombie\\run", loop=True)
        #             ]
        #             ),

        #     },
        #     default_animation="idle",
        # )

        self.animation_manager = AnimationManager(
            animations={
                "idle": Animation("idle", "D:\\game assets\\zombie\\idle"),
                "walk": Animation("walk", "D:\\game assets\\zombie\\walk"),
                "idle_to_walk": Animation("idle_to_walk", "D:\\game assets\\zombie\\idle to walk"),
                "scream_run": SequenceAnimation(
                    name="scream_run",
                    animations=[
                        Animation("scream", "D:\\game assets\\zombie\\scream"),
                        Animation("run", "D:\\game assets\\zombie\\run")
                    ]
                ),
                "attack": Animation("attack", "D:\\game assets\\zombie\\attack"),
            },
            default="idle",
            transitions=[
                TransitionRule("idle", "walk", "idle_to_walk", True),
            ]
        )
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


        self.x_speed = 0
        self.y_speed = 0


    @property
    def image(self):
        frame = self.animation_manager.update()
        print('frame: ', frame)
        return pygame.transform.scale(frame.image, (self.width, self.height))

    def update(self):
        self.apply_speed()
        if self.rect.x > self.director.width:
            self.rect.x = -self.width
        if self.rect.x < -self.width:
            self.rect.x = self.director.width

    def apply_speed(self):
        if "walk" in self.animation_manager.active_animation.name:
            self.rect.x += self.x_speed
            self.rect.y += self.y_speed


    def move_left(self):
        self.x_speed = -self.base_x_speed*self.speed
        self.animation_manager.play_animation("idle_walk_backwards_idle")

    def move_right(self):
        self.x_speed = self.base_x_speed*self.speed
        # self.animation_manager.play_animation("idle_walk_idle")
        self.animation_manager.switch_animation("walk")

    def move_up(self):
        self.y_speed = -self.base_y_speed*self.speed
        self.animation_manager.play_animation("idle_walk_idle")

    def move_down(self):
        self.y_speed = self.base_y_speed*self.speed
        self.animation_manager.play_animation("idle_walk_idle")


    def stop(self):
        self.x_speed = 0
        self.y_speed = 0
        if self.animation_manager.active_animation.name == "idle_walk_idle":
            if self.animation_manager.active_animation.active_animation.name == "idle_to_walk":
                self.animation_manager.active_animation.skip(2)
            elif self.animation_manager.active_animation.active_animation.name == "walk":
                self.animation_manager.active_animation.skip(1)

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                 self.move_left()

            if event.key == pygame.K_RIGHT:
                self.move_right()


            if event.key == pygame.K_UP:
                self.move_up()

            if event.key == pygame.K_DOWN:
                self.move_down()

            if event.key == pygame.K_SPACE:
                self.animation_manager.switch_animation("attack")

            if event.key == pygame.K_LSHIFT:
                self.animation_manager.switch_animation("scream_run")



            PRESSED_KEYS.append(event.key)

        if event.type == pygame.KEYUP:
            if event.key in PRESSED_KEYS and event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]:
                # self.stop()
                self.animation_manager.switch_animation("idle")



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
