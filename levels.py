import pygame
from Character import CameraAwareGroupSingle, Player, CameraAwareGroup, EnemyManager
from UI import HUD
from camera import Camera
from director import Scene
from cursor import Cursor


class Level(Scene):
    def __init__(
        self,
        director,
    ):
        self.name = "city"
        Scene.__init__(self, director)

    def setup(self):
        self.background = pygame.image.load(f"assets/levels/{self.name}.jpg")
        self.screen_width = self.director.width
        self.screen_height = self.director.height
        self.scene_width = self.background.get_width()
        self.scene_height = self.background.get_height()

        self.camera = Camera(
            self.screen_width, self.screen_height, self.scene_width, self.scene_height
        )

        self.Player = Player(
            scene=self, x=0, y=400, height=250, width=250, speed=(4, 2)
        )
        self.PlayerGroup = CameraAwareGroupSingle(self.Player)
        self.PlayerGroup.set_camera(self.camera)

        self.EnemyGroup = CameraAwareGroup()
        self.EnemyGroup.set_camera(self.camera)

        self.EnemyManager = EnemyManager(self, ['zombie girl', 'zombie cop'] , max_enemies=5)

        self.cursor = Cursor(
            self.Player, min_distance=self.Player.width // 2, max_angle=30, DEBUG=False
        )
        self.hud = HUD(
            self.Player,
            right=25,
            y=50,
            scale=0.6,
            space_y=-5,
            padding_x=10,
        )

    def update(self):
        self.PlayerGroup.update()
        self.EnemyGroup.update()
        self.EnemyManager.update()
        self.camera.update(self.Player)
        self.cursor.update()
        self.hud.update()

    def draw(self, screen, window_scale):
        screen.blit(self.background, self.camera.apply(self.background))
        self.PlayerGroup.draw(screen)
        self.EnemyGroup.draw(screen)
        self.hud.draw(screen)
        self.cursor.draw(screen)

    def event(self, event):
        self.PlayerGroup.sprite.event(event)
        self.EnemyGroup.event(event)
