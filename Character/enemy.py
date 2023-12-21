import random
from Animation import AnimationController, Animation, SequenceAnimation, TransitionRule
from .character import Character


class Enemy(Character):
    sense_range = 500
    DEAD = False

    def __init__(
        self,
        scene,
        name,
        x,
        y,
        height=None,
        width=None,
        speed: tuple = (2, 1),
        direction: int = 1,
    ):
        self.name = name
        self.animation = AnimationController(
            animations=[
                Animation("idle", f"D:\\game assets\\{self.name}\\idle", speed=1.5),
                Animation("walk", f"D:\\game assets\\{self.name}\\walk", speed=1.5),
                Animation(
                    "idle_to_walk",
                    f"D:\\game assets\\{self.name}\\idle to walk",
                    speed=1.5,
                ),
                SequenceAnimation(
                    name="scream_run",
                    animations=[
                        Animation("scream", f"D:\\game assets\\{self.name}\\scream"),
                        Animation("run", f"D:\\game assets\\{self.name}\\run"),
                    ],
                ),
                Animation("attack", f"D:\\game assets\\{self.name}\\attack", speed=1.5),
            ],
            default="idle",
            transitions=[
                TransitionRule("idle", "walk", "idle_to_walk", True),
            ],
        )
        super().__init__(scene, x, y, height, width, speed, direction)

    def update(self):
        super().update()
        self.chase_player(self.scene.Player)

    def sense_player(self, player):
        x = self.rect.x - player.rect.x
        y = self.rect.y - player.rect.y
        within_range = abs(x) < self.sense_range

        return x, y, within_range

    def chase_player(self, player):
        x, y, within_range = self.sense_player(player)
        print("x, y, within_range: ", x, y, within_range)
        if within_range:
            direction = -1 if x > 0 else 1
            self.moving = True
            if self.direction == -1:
                self.animation.set_animation("turn_walk")
            else:
                self.animation.set_animation("walk")
            self.x_speed = self.speed[0]
            self.x_speed = -self.speed[0] if x > 0 else self.speed[0]
            self.y_speed = -self.speed[1] if y > 0 else self.speed[1]
        else:
            self.moving = False
            self.animation.set_animation("idle")
            self.x_speed = 0
            self.y_speed = 0


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

        enemy_height = 300
        for i in range(self.max_enemies):
            name = random.choice(self.enemy_types)
            x = (
                enemy_rate * i
                + 1
                + random.randint(0, enemy_rate)
                - random.randint(0, enemy_rate)
            )
            x = min(x, level_width - enemy_rate)

            # turn x from scene coordinates to camera coordinates
            x = x - self.scene.camera.rect.x

            y = random.randint(
                self.scene.scene_height - enemy_height - 150,
                self.scene.scene_height - enemy_height,
            )
            self.enemies.append(
                Enemy(self.scene, name, x, y, enemy_height, enemy_height)
            )

    def render_enemies(self):
        for enemy in self.enemies:
            camera = self.scene.camera
            camera.rect.x = abs(camera.rect.x)
            if camera.rect.colliderect(enemy.rect):
                self.spawn_enemy(enemy)
            else:
                self.despawn_enemy(enemy)
