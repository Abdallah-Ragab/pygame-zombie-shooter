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
            Animation("hit 1", "D:\\game assets\\swat 1\\hit 1", speed=1.5),
            Animation("hit 2", "D:\\game assets\\swat 1\\hit 2", speed=1.5),
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
    melee_animations = ["elbow", "kick"]

    max_bullets = 32
    bullets = max_bullets
    ranged_damage = 10
    melee_damage = 5

    def update(self):
        active_animation = self.animation.active_animation
        if isinstance(active_animation, SequenceAnimation):
            active_animation = active_animation.active_animation

        if active_animation is not None and active_animation.name == "turn":
            if active_animation.FINISHED_FLAG:
                self.direction *= -1

        if active_animation is not None and not active_animation.name == "walk":
            self.walking = False

        if self.health <= 0:
            self.die()

        # FIXME: it only check at first key down, not when key is held down

        return super().update()

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

    def hold_event(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_RIGHT]:
            self.walk_right()
        elif pressed[pygame.K_LEFT]:
            self.walk_left()
        elif pressed[pygame.K_UP]:
            self.walk_up()
        elif pressed[pygame.K_DOWN]:
            self.walk_down()

    def walk_right(self):
        if not self.within_right_limit():
            self.moving = False
            return
        self.moving = True
        if self.direction == -1:
            self.animation.set_animation("turn_walk")
        else:
            self.animation.set_animation("walk")
        self.x_speed = self.speed[0]

    def walk_left(self):
        if not self.within_left_limit():
            self.moving = False
            return
        self.moving = True
        if self.direction == 1:
            self.animation.set_animation("turn_walk")
        else:
            self.animation.set_animation("walk")
        self.x_speed = -self.speed[0]

    def walk_up(self):
        if not self.within_top_limit():
            self.moving = False
            return
        self.moving = True
        self.animation.set_animation("walk")
        self.y_speed = -self.speed[1]

    def walk_down(self):
        if not self.within_bottom_limit():
            self.moving = False
            return
        self.moving = True
        self.animation.set_animation("walk")
        self.y_speed = self.speed[1]

    def handle_mousebuttondown(self, event):
        self.moving = False
        if event.button == 1:
            if self.bullets > 0:
                if self.scene.cursor.rect.collidepoint(event.pos):
                    self.shoot()
            else:
                self.scene.music.play_sound_effect("empty_clip")
        elif event.button == 3:
            self.melee()

    def melee(self):
        random_animation = random.choice(self.melee_animations)
        active_animation = self.animation.active_animation
        if hasattr(active_animation, "active_animation"):
            active_animation = active_animation.active_animation
        if active_animation is not None and active_animation.name in self.melee_animations:
            return
        self.animation.set_animation(random_animation, loop=False)
        for enemy in self.enemies_colliding_player():
            enemy.get_hit(self.melee_damage)

    def shoot(self):
        self.animation.set_animation("fire", loop=False)
        self.scene.music.play_sound_effect("shot")
        self.bullets -= 1 if self.bullets > 0 else 0
        enemies = self.enemies_colliding_cursor()
        if len(enemies) > 0:
            print("enemies hit:", len(enemies))
            for enemy in enemies:
                enemy.get_hit(self.ranged_damage)

    def handle_keyup(self, event):
        if event.key in (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN):
            self.idle()

    def idle(self):
        self.animation.set_animation("idle")
        self.moving = False
        self.x_speed, self.y_speed = 0, 0

    def die(self):
        self.animation.set_animation("die", loop=False)
        self.scene.music.play_sound_effect("death")
        self.moving = False
        self.x_speed, self.y_speed = 0, 0
        if self.animation.active_animation.FINISHED_FLAG:
            self.DEAD = True

    def get_hit(self, damage):
        print("Player got hit")
        animation = random.choice(["hit 1", "hit 2"])
        self.animation.set_animation(animation, loop=False)
        self.moving = False
        self.health -= damage
        if self.health <= 0:
            self.die()


    def handle_mousebuttonup(self, event):
        if event.button == 1 and self.bullets > 0:
            self.idle()
            if self.moving:
                self.animation.set_animation("walk")

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

    def check_limits(self):

        if not self.x_speed == 0:
            if self.x_speed > 0:
                if self.within_right_limit():
                    return
            else:
                if self.within_left_limit():
                    return

        if not self.y_speed == 0:
            if self.y_speed > 0:
                if self.within_bottom_limit():
                    return
            else:
                if self.within_top_limit():
                    return


        self.moving = False
        self.animation.set_animation("idle")

    def enemies_colliding_cursor(self):
        enemies = []
        cursor = self.scene.cursor
        print("cursor:", cursor.rect)
        print("mouse:", pygame.mouse.get_pos())
        enemy_group = self.scene.EnemyGroup.sprites()
        for enemy in enemy_group:
            print("enemy:", enemy.rect, "cursor:", cursor.rect)
            # if cursor.collide(enemy.rect):
            if self.scene.camera.apply(enemy.rect).colliderect(cursor.rect):
                enemies.append(enemy)
        return enemies

    def enemies_colliding_player(self):
        enemies = []
        enemy_group = self.scene.EnemyGroup.sprites()
        for enemy in enemy_group:
            if enemy.rect.colliderect(self.rect):
                enemies.append(enemy)
        return enemies

    def use_ammo_perk(self):
        owned = int(self.scene.director.storage.get("ammo", 0))
        if owned > 0:
            self.bullets = self.max_bullets
            self.scene.director.storage.set("ammo", owned - 1)
            self.scene.music.play_sound_effect("perk")
            print("ammo perk used")
        else:
            print("ammo perk not owned")

    def use_health_perk(self):
        owned = int(self.scene.director.storage.get("health", 0))
        if owned > 0:
            self.health = self.max_health
            self.scene.director.storage.set("health", owned - 1)
            self.scene.music.play_sound_effect("perk")
            print("health perk used")
        else:
            print("health perk not owned")

    def use_multiplier_perk(self):
        owned = int(self.scene.director.storage.get("multiplier", 0))
        if owned > 0:
            self.scene.director.storage.set("multiplier", owned - 1)
            self.scene.music.play_sound_effect("perk")
            print("multiplier perk used")
        else:
            print("multiplier perk not owned")

