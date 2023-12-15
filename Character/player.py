import pygame
from .character import Character
from Animation import AnimationController, Animation, SequenceAnimation, TransitionRule


class Player(Character):
    animation = AnimationController(
            animations=[
                Animation('idle', "D:\\game assets\\zombie\\idle"),
                Animation("walk", "D:\\game assets\\zombie\\walk"),
                Animation("idle_to_walk", "D:\\game assets\\zombie\\idle to walk"),
                SequenceAnimation(
                    name="scream_run",
                    animations=[
                        Animation("scream", "D:\\game assets\\zombie\\scream"),
                        Animation("run", "D:\\game assets\\zombie\\run")
                    ]
                ),
                Animation("attack", "D:\\game assets\\zombie\\attack"),
            ],
            default="idle",
            transitions=[
                TransitionRule("idle", "walk", "idle_to_walk", True),
            ]
        )

    def update(self):
        return super().update()

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN):
                self.animation.switch_animation("walk")
                self.moving = True
                if event.key == pygame.K_RIGHT:
                    self.speed = (1, 0)
                elif event.key == pygame.K_LEFT:
                    self.speed = (-1, 0)
                if event.key == pygame.K_UP:
                    self.speed = (0, -1)
                elif event.key == pygame.K_DOWN:
                    self.speed = (0, 1)
            if event.key == pygame.K_SPACE:
                self.animation.switch_animation("attack", loop=False)
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN):
                self.animation.switch_animation("idle")
                self.moving = False
                self.speed = (0, 0)

        return super().event(event)



