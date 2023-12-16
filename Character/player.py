import pygame
from .character import Character
from Animation import AnimationController, Animation, SequenceAnimation, TransitionRule


class Player(Character):
    # TODO ADD ACTUAL WALK_FIRE ANIMATION
    animation = AnimationController(
        animations=[
            Animation("walk_fire", "D:\\game assets\\zombie\\idle", speed=1.5),
            Animation("idle", "D:\\game assets\\swat 1\\idle", speed=1.5),
            Animation("walk", "D:\\game assets\\swat 1\\walk", speed=1.5),
            Animation("turn", "D:\\game assets\\swat 1\\turn", speed=1.5),
            Animation("idle_to_walk", "D:\\game assets\\swat 1\\idle to walk", speed=1.5),
            Animation("idle_to_fire", "D:\\game assets\\swat 1\\idle to fire", speed=1.5),
            SequenceAnimation(
                name="turn_walk",
                animations=[
                    Animation("turn", "D:\\game assets\\swat 1\\turn", speed=1.5),
                    Animation("walk", "D:\\game assets\\swat 1\\walk", speed=1.5),
                ],
            ),
            Animation("fire", "D:\\game assets\\swat 1\\fire", speed=1.5),
        ],
        default="idle",
        transitions=[
            TransitionRule("idle", "walk", "idle_to_walk", True),
            # TransitionRule("idle", "fire", "idle_to_fire", True),
        ]
    )

    def update(self):
        active_animation = self.animation.active_animation
        if isinstance(active_animation, SequenceAnimation):
            active_animation = active_animation.active_animation

        if active_animation is not None and active_animation.name == "turn":
            if active_animation.FINISHED_FLAG:
                self.direction *= -1
        return super().update()

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN):
                self.moving = True
                if event.key == pygame.K_RIGHT:
                    if self.direction == -1:
                        self.animation.switch_animation("turn_walk")
                    else:
                        self.animation.switch_animation("walk")
                    self.x_speed = self.speed[0]
                elif event.key == pygame.K_LEFT:
                    if self.direction == 1:
                        self.animation.switch_animation("turn_walk")
                    else:
                        self.animation.switch_animation("walk")
                    self.x_speed = -self.speed[0]
                if event.key == pygame.K_UP:
                    self.animation.switch_animation("walk")
                    self.y_speed = -self.speed[1]
                elif event.key == pygame.K_DOWN:
                    self.animation.switch_animation("walk")
                    self.y_speed = self.speed[1]
            if event.key == pygame.K_SPACE:
                self.animation.switch_animation("fire", loop=False)
                if self.moving:
                    self.animation.switch_animation("walk_fire", loop=False)

        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN):
                self.animation.switch_animation("idle")
                self.moving = False
                self.x_speed, self.y_speed = 0, 0

            if event.key == pygame.K_SPACE:
                self.animation.switch_animation("idle")
                if self.moving:
                    self.animation.switch_animation("walk")

        return super().event(event)
