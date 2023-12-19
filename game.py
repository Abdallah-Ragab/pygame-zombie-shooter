import pygame, sys
# from pygamevideo import Video
from Video.player import Video
from director import Director, Scene

from Character import Player, CameraAwareGroupSingle
from camera import Camera
from cursor import Cursor

# from hud import HUD
from UI import HUD, Avatar, HealthBar, Ammo, Money, UIElement


class Game(Scene):
    def __init__(
        self,
        director,
    ):
        Scene.__init__(self, director)

    def setup(self):
        self.screen_width = self.director.width
        self.screen_height = self.director.height
        self.background = pygame.image.load("assets/levels/forest.png")
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

        self.cursor = Cursor(
            self.Player, min_distance=self.Player.width // 2, max_angle=30, DEBUG=False
        )
        self.hud = HUD(
            self.Player,
            elements=[
                Avatar(self.Player, path="assets/hud/avatars/1.png"),
                HealthBar(
                    self.Player,
                    elements=[
                        UIElement(path="assets/hud/health_bar_back.png"),
                        UIElement(path="assets/hud/health_bar_front.png"),
                    ],
                ),
                Ammo(self.Player, path="assets/hud/ammo.png"),
                Money(self.Player, path="assets/hud/money.png"),
            ],
            right=25,
            y=50,
            scale=0.6,
            space_y=-5,
            padding_x=10,
        )
        # self.hud.stack_over()

    def update(self):
        self.PlayerGroup.update()
        self.camera.update(self.Player)
        self.cursor.update()
        self.hud.update()

    def draw(self, screen, window_scale):
        screen.blit(self.background, self.camera.apply(self.background))
        self.PlayerGroup.draw(screen)
        self.hud.draw(screen)
        self.cursor.draw(screen)

    def event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            self.director.set_scene(Pause(self.director))
        self.PlayerGroup.sprite.event(event)


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


class Intro(Scene):
    def __init__(self, director):
        Scene.__init__(self, director)

    def setup(self):
        self.video = Video("assets/intro.mp4")
        # self.video.play()

    def update(self):
        # if self.video.remaining_frames == 0:
        #     self.finish()
        if self.video.active == False:
            self.finish()


    def event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.skip()

    def draw(self, screen, window_scale):
        # self.video.draw_to(screen, (0, 0), (screen.get_width(), screen.get_height()))
        self.video.draw(screen, (0, 0))

    def finish(self):
        self.director.set_scene(Game(self.director))
        # self.video.stop()
        self.video.close()

    def skip(self):
        key_moments = [5, 13, 17 ]
        current_time = self.video.get_playback_data()["time"]
        if current_time > key_moments[-1]:
            self.finish()
            return
        next_key_moment = [x for x in key_moments if x > current_time][0]
        self.video.seek(next_key_moment, accurate=True)
        print("skipped from", current_time, ", to:", next_key_moment)
        print("time now:", self.video.get_playback_data()["time"])


def main():
    pygame.init()
    director = Director()
    director.set_scene(Intro(director))
    # director.set_scene(Game(director))
    director.setup()
    director.loop()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
