import pygame
from Character import CameraAwareGroupSingle, Player, CameraAwareGroup, EnemyManager
from UI import HUD
from camera import Camera
from director import Scene
from cursor import Cursor
from music import Player as MusicPlayer


class Level(Scene):
    map = "city"
    music = MusicPlayer()
    def __init__(
        self,
        director,
    ):
        Scene.__init__(self, director)

    def setup(self):
        self.background = pygame.image.load(f"assets/levels/{self.map}.jpg")
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
        self.music.update()
        self.PlayerGroup.update()
        self.EnemyGroup.update()
        self.EnemyManager.update()
        self.camera.update(self.Player)
        self.cursor.update()
        self.hud.update()
        self.check_win_condition()

    def draw(self, screen, window_scale):
        screen.blit(self.background, self.camera.apply(self.background))
        self.PlayerGroup.draw(screen)
        self.EnemyGroup.draw(screen)
        self.hud.draw(screen)
        self.cursor.draw(screen)

    def event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            from game import MainMenu
            self.director.set_scene(MainMenu(self.director))

        self.PlayerGroup.sprite.event(event)
        self.EnemyGroup.event(event)



    def check_win_condition(self):
        if self.Player.DEAD:
            self.director.set_scene(GameOver(self.director))
        elif self.EnemyManager.all_dead():
            self.director.set_scene(Win(self.director))

    def reward_player(self):
        money = self.director.storage.get("money", 0)
        money += 100
        self.director.storage.set("money", money)


class GameOver(Scene):
    def __init__(self, director):
        Scene.__init__(self, director)

    def setup(self):
        self.game_over_text = pygame.font.SysFont("Arial", 50).render(
            "Game Over", True, (255, 255, 255)
        )
        window_center = (self.director.width / 2, self.director.height / 2)


    def update(self):
        pass

    def event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            from game import MainMenu
            self.director.set_scene(MainMenu(self.director))

    def draw(self, screen, window_scale):
        background = pygame.Rect(
            (0, 0),
            (self.director.width * window_scale, self.director.height * window_scale),
        )
        pygame.draw.rect(screen, (0, 0, 255), background)
        # show the pause text at the center of the screen
        screen.blit(
            self.game_over_text,
            (
                self.director.width / 2 - self.game_over_text.get_width() / 2,
                self.director.height / 2 - self.game_over_text.get_height() / 2,
            ),
        )
        self.game_over_text.get_rect().center = (
            self.director.width / 2,
            self.director.height / 2,
        )

class Win(Scene):
    def __init__(self, director):
        Scene.__init__(self, director)

    def setup(self):
        self.win_text = pygame.font.SysFont("Arial", 50).render(
            "You Win!", True, (255, 255, 255)
        )
        window_center = (self.director.width / 2, self.director.height / 2)

    def update(self):
        pass

    def event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            from game import MainMenu
            self.director.set_scene(MainMenu(self.director))

    def draw(self, screen, window_scale):
        background = pygame.Rect(
            (0, 0),
            (self.director.width * window_scale, self.director.height * window_scale),
        )
        pygame.draw.rect(screen, (0, 0, 255), background)
        # show the pause text at the center of the screen
        screen.blit(
            self.win_text,
            (
                self.director.width / 2 - self.win_text.get_width() / 2,
                self.director.height / 2 - self.win_text.get_height() / 2,
            ),
        )
        self.win_text.get_rect().center = (
            self.director.width / 2,
            self.director.height / 2,
        )