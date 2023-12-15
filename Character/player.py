import pygame
from .character import Character
from Animation import AnimationController, Animation, SequenceAnimation, TransitionRule


class Player(Character):
    animation = AnimationController(
            animations=[
                Animation('idle', "D:\\game assets\\swat 1\\idle", speed=1.5),
                Animation("walk", "D:\\game assets\\swat 1\\walk", speed=1.5),
                Animation("turn", "D:\\game assets\\swat 1\\turn", speed=1.5),
                SequenceAnimation(
                    name="turn_walk",
                    animations=[
                        Animation("turn", "D:\\game assets\\swat 1\\turn"),
                        Animation("walk", "D:\\game assets\\swat 1\\walk")
                    ]
                ),
                Animation("fire", "D:\\game assets\\swat 1\\fire", speed=1.5),
            ],
            default="idle",
            # transitions=[
            #     TransitionRule("idle", "walk", "idle_to_walk", True),
            # ]
        )

    def update(self):
        return super().update()

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN):
                self.moving = True
                if event.key == pygame.K_RIGHT:
                    self.animation.switch_animation("walk")
                    self.x_speed = self.speed[0]
                elif event.key == pygame.K_LEFT:
                    self.animation.switch_animation("turn_walk")
                    self.x_speed = -self.speed[0]
                if event.key == pygame.K_UP:
                    self.animation.switch_animation("walk")
                    self.y_speed = -self.speed[1]
                elif event.key == pygame.K_DOWN:
                    self.animation.switch_animation("walk")
                    self.y_speed = self.speed[1]
            if event.key == pygame.K_SPACE:
                self.animation.switch_animation("fire", loop=False)
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN):
                self.animation.switch_animation("idle")
                self.moving = False
                self.x_speed, self.y_speed = 0, 0

        return super().event(event)



