import random
import pygame
from .character import Character
from Animation import AnimationController, Animation, SequenceAnimation, TransitionRule


class Player(Character):
    animation = AnimationController(
        animations=[
            Animation("idle", "D:\\game assets\\swat 1\\idle", speed=1.5),
            Animation("walk", "D:\\game assets\\swat 1\\walk", speed=1.5),
            Animation("turn", "D:\\game assets\\swat 1\\turn", speed=1.5),
            Animation("elbow", "D:\\game assets\\swat 1\\elbow", speed=1.5),
            Animation("kick", "D:\\game assets\\swat 1\\kick", speed=1.5),
            Animation("die", "D:\\game assets\\swat 1\\die", speed=1.5),
            Animation("fire", "D:\\game assets\\swat 1\\fire", speed=1.5),
            Animation(
                "idle_to_walk", "D:\\game assets\\swat 1\\idle to walk", speed=1.5
            ),
            SequenceAnimation(
                name="turn_walk",
                animations=[
                    Animation("turn", "D:\\game assets\\swat 1\\turn", speed=1.5),
                    Animation("walk", "D:\\game assets\\swat 1\\walk", speed=1.5),
                ],
            ),
        ],
        default="idle",
        transitions=[
            TransitionRule("idle", "walk", "idle_to_walk", True),
        ],
    )
    max_bullets = 32
    bullets = max_bullets

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
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.bullets > 0:
                self.animation.switch_animation("fire", loop=False)
                self.bullets -= 1 if self.bullets > 0 else 0
                self.health -= 5 if self.health > 0 else 0
                # print(self.health)
                if self.moving:
                    self.animation.switch_animation("walk_fire", loop=False)

        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN):
                self.animation.switch_animation("idle")
                self.moving = False
                self.x_speed, self.y_speed = 0, 0

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.bullets > 0:
                self.animation.switch_animation("idle")
                if self.moving:
                    self.animation.switch_animation("walk")

        return super().event(event)

    def event(self, event):
        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mousebuttondown(event)
        elif event.type == pygame.KEYUP:
            self.handle_keyup(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.handle_mousebuttonup(event)

        return super().event(event)

    def handle_keydown(self, event):
        if event.key == pygame.K_RIGHT:
            self.walk_right()
        elif event.key == pygame.K_LEFT:
            self.walk_left()
        elif event.key == pygame.K_UP:
            self.walk_up()
        elif event.key == pygame.K_DOWN:
            self.walk_down()

    def walk_right(self):
        if not self.within_right_limit():
            return
        self.moving = True
        if self.direction == -1:
            self.animation.switch_animation("turn_walk")
        else:
            self.animation.switch_animation("walk")
        self.x_speed = self.speed[0]

    def walk_left(self):
        if not self.within_left_limit():
            return
        self.moving = True
        if self.direction == 1:
            self.animation.switch_animation("turn_walk")
        else:
            self.animation.switch_animation("walk")
        self.x_speed = -self.speed[0]

    def walk_up(self):
        if not self.within_top_limit():
            return
        self.moving = True
        self.animation.switch_animation("walk")
        self.y_speed = -self.speed[1]

    def walk_down(self):
        if not self.within_bottom_limit():
            return
        self.moving = True
        self.animation.switch_animation("walk")
        self.y_speed = self.speed[1]

    def handle_mousebuttondown(self, event):
        self.moving = False
        if event.button == 1:
            if self.bullets > 0:
                self.shoot()
        elif event.button == 3:
            self.melee()

    def melee(self):
        animations = ["elbow", "kick"]
        random_animation = random.choice(animations)
        self.animation.switch_animation(random_animation, loop=False)

    def shoot(self):
        self.animation.switch_animation("fire", loop=False)
        self.bullets -= 1 if self.bullets > 0 else 0

    def handle_keyup(self, event):
        if event.key in (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN):
            self.idle()

    def idle(self):
        self.animation.switch_animation("idle")
        self.moving = False
        self.x_speed, self.y_speed = 0, 0

    def handle_mousebuttonup(self, event):
        if event.button == 1 and self.bullets > 0:
            self.idle()
            if self.moving:
                self.animation.switch_animation("walk")

    def within_top_limit(self):
        feet_y = self.rect.bottom - self.height * 0.10
        top_condition = feet_y >= 500
        print("within_top_limit:", top_condition)  # Add this line
        return top_condition

    def within_bottom_limit(self):
        bottom_condition = (
            self.rect.bottom <= pygame.display.get_surface().get_rect().bottom
        )
        print("within_bottom_limit:", bottom_condition)  # Add this line
        return bottom_condition

    def within_right_limit(self):
        right_condition = self.rect.right <= self.scene.background.get_rect().right
        print("within_right_limit:", right_condition)  # Add this line
        return right_condition

    def within_left_limit(self):
        left_condition = self.rect.left >= self.scene.background.get_rect().left
        print("within_left_limit:", left_condition)  # Add this line
        return left_condition
