import random
from Animation import AnimationController, Animation, SequenceAnimation, TransitionRule
from .character import Character


class Enemy(Character):
    sense_range = 700
    DEAD = False
    melee_damage = 10

    def __init__(
        self,
        scene,
        name,
        x,
        y,
        height=None,
        width=None,
        speed: tuple = (2, 1),
        direction: int = -1,
    ):
        self.name = name
        self.animation = AnimationController(
            animations=[
                Animation("idle", f"D:\\game assets\\{self.name}\\idle", speed=0.5),
                Animation("walk", f"D:\\game assets\\{self.name}\\walk", speed=0.5),
                Animation("die", f"D:\\game assets\\{self.name}\\die", speed=0.5),
                Animation("hit", f"D:\\game assets\\{self.name}\\hit", speed=0.5),
                Animation("idle_to_walk", f"D:\\game assets\\{self.name}\\idle to walk", speed=0.5),
                SequenceAnimation(
                    name="scream_run",
                    animations=[
                        Animation("scream", f"D:\\game assets\\{self.name}\\scream"),
                        Animation("run", f"D:\\game assets\\{self.name}\\run"),
                    ],
                ),
                Animation("attack 1", f"D:\\game assets\\{self.name}\\attack 1", speed=0.5),
                Animation("attack 2", f"D:\\game assets\\{self.name}\\attack 2", speed=0.5),
            ],
            default="idle",
            transitions=[
                TransitionRule("idle", "walk", "idle_to_walk", True),
            ],
        )
        super().__init__(scene, x, y, height, width, speed, direction)

    def update(self):
        self.chase_player(self.scene.Player)
        if self.animation.active_animation.name == "die" and self.animation.active_animation.FINISHED_FLAG:
            self.DEAD = True
            self.scene.EnemyManager.kill_enemy(self)

        animation = self.animation.active_animation if isinstance(self.animation.active_animation, Animation) else self.animation.active_animation.active_animation
        if not self.animation.active_animation.name == "walk":
            self.moving = False

        super().update()

    def sense_player(self, player):
        x = self.rect.x - player.rect.x
        y = self.rect.y - player.rect.y
        within_range = abs(x) < self.sense_range

        return x, y, within_range

    def chase_player(self, player):
        if self.animation.active_animation.name in ["die", "hit"]:
            return
        x, y, within_range = self.sense_player(player)
        if within_range:
            if self.collide_player(player):
                self.attack_player(player)
            else:
                self.direction = -1 if x > 0 else 1
                self.moving = True
                self.animation.set_animation("walk")
                self.x_speed = self.speed[0]
                self.x_speed = -self.speed[0] if x > 0 else self.speed[0]
                self.y_speed = -self.speed[1] if y > 0 else self.speed[1]
        else:
            self.moving = False
            self.animation.set_animation("idle")
            self.x_speed = 0
            self.y_speed = 0

    def collide_player(self, player):
        return abs(self.rect.centerx - player.rect.centerx) < 100 and abs(self.rect.centery - player.rect.centery) < 100

    def attack_player(self, player):
        if player.health <= 0 or self.health <= 0 or self.animation.active_animation.name == "hit":
            return
        self.moving = False
        attacks = ["attack 1", "attack 2"]
        if self.animation.active_animation.name in attacks:
            return  # already attacking
        attack = random.choice(attacks)
        print("enemy started attcking")
        self.animation.set_animation(attack, loop=False)
        if self.animation.active_animation.FINISHED_FLAG:
            print("enemy finished attcking")
            player.get_hit(self.melee_damage)
            self.animation.set_animation("idle")

    def die(self):
        self.moving = False
        self.animation.set_animation("die", loop=False)
        self.animation.LOCKED = True
        print("enemy started dying")
        print(f'Animation: {self.animation.active_animation.name}')
        print(f'Finished flag: {self.animation.active_animation.FINISHED_FLAG}')

    def get_hit(self, damage):
        self.health -= damage
        print("enemy health: ", self.health)
        if self.health <= 0:
            self.die()
        self.animation.set_animation("hit", loop=False)
        if self.animation.active_animation.FINISHED_FLAG:
            print("enemy finished getting hit")
            self.animation.set_animation("idle")

class EnemyManager:
    def __init__(self, scene, enemies, max_enemies=5):
        self.scene = scene
        self.max_enemies = max_enemies
        self.enemy_types = enemies
        self.enemies = []
        self.distribute_enemies()

    def update(self):
        self.render_enemies()

    def spawn_enemy(self, enemy):
        if self.scene.EnemyGroup.has(enemy):
            return
        self.scene.EnemyGroup.add(enemy)
        print("spawned enemy: ", enemy.name)

    def kill_enemy(self, enemy):
        print("killing enemy: ", enemy.name)
        self.despawn_enemy(enemy)
        enemy.DEAD = True

    def despawn_enemy(self, enemy):
        if self.scene.EnemyGroup.has(enemy):
            self.scene.EnemyGroup.remove(enemy)
            print("despawned enemy: ", enemy.name)

    def distribute_enemies(self):
        level_width = self.scene.background.get_width()
        enemy_rate = level_width // self.max_enemies
        # render enemies only when the camera edge is near

        enemy_height = 250
        for i in range(self.max_enemies):
            name = random.choice(self.enemy_types)
            x = (
                enemy_rate * i
                + random.randint(-enemy_rate/2, enemy_rate/2)
            )
            x = min(x, level_width - enemy_rate)
            x = max(x, self.scene.director.width)

            # turn x from scene coordinates to camera coordinates
            x = x - self.scene.camera.rect.x

            y = random.randint(
                self.scene.scene_height - enemy_height - 120,
                self.scene.scene_height - enemy_height,
            )
            self.enemies.append(
                Enemy(self.scene, name, x, y, enemy_height, enemy_height)
            )

    def render_enemies(self):
        for enemy in self.enemies:
            if not enemy.DEAD:
                camera = self.scene.camera
                camera.rect.x = abs(camera.rect.x)
                if camera.rect.colliderect(enemy.rect) and not enemy.DEAD:
                    self.spawn_enemy(enemy)
                else:
                    self.despawn_enemy(enemy)

    def all_dead(self):
        return all([enemy.DEAD for enemy in self.enemies])