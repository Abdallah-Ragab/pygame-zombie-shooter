import pygame, sys
from director import Director, Scene

from Character import Player, CameraAwareGroupSingle
from camera import Camera
from cursor import Cursor
from hud import HUD


class Game(Scene):
    def __init__(
        self,
        director,
    ):
        Scene.__init__(self, director)
        self.setup()

    def update(self):
        self.PlayerGroup.update()
        self.camera.update(self.Player)
        self.cursor.update()
        self.hud.update()


    def setup(self):
        self.screen_width = self.director.width
        self.screen_height = self.director.height
        self.background = pygame.image.load("assets/levels/city.jpg")
        self.scene_width = self.background.get_width()
        self.scene_height = self.background.get_height()
        self.camera = Camera(
            self.screen_width, self.screen_height, self.scene_width, self.scene_height
        )

        self.Player = Player(
            scene=self, x=0, y=400, height=250, width=250, speed=(3, 3)
        )
        self.PlayerGroup = CameraAwareGroupSingle(self.Player)
        self.PlayerGroup.set_camera(self.camera)

        self.cursor = Cursor(self.Player, min_distance=self.Player.width//2, max_angle=30, DEBUG=False)
        self.hud = HUD(self.Player)

    def event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            self.director.set_scene(Pause(self.director))
        self.PlayerGroup.sprite.event(event)

    def draw(self, screen, window_scale):
        screen.blit(self.background, self.camera.apply(self.background))
        self.hud.draw(screen)
        self.PlayerGroup.draw(screen)
        self.cursor.draw(screen)


class Pause(Scene):
    def __init__(self, director):
        Scene.__init__(self, director)
        self.pause_text = pygame.font.SysFont("Arial", 50).render(
            "Pause", True, (255, 255, 255)
        )
        window_center = (self.director.width / 2, self.director.height / 2)

    def update(self):
        self.hud.update()

    def event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            self.director.set_scene(Game(self.director))

    def draw(self, screen, window_scale):
        background = pygame.Rect(
            (0, 0),
            (self.director.width * window_scale, self.director.height * window_scale),
        )
        pygame.draw.rect(screen, (0, 0, 255), background)
        # show the pause text at the center of the screen
        screen.blit(
            self.pause_text,
            (
                self.director.width / 2 - self.pause_text.get_width() / 2,
                self.director.height / 2 - self.pause_text.get_height() / 2,
            ),
        )
        self.pause_text.get_rect().center = (
            self.director.width / 2,
            self.director.height / 2,
        )


def main():
    pygame.init()
    director = Director()
    director.set_scene(Game(director))
    director.setup()
    director.loop()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
