import pygame, sys

# from pygamevideo import Video
from Video.player import Video
from director import Director, Scene

from Character import Player, CameraAwareGroupSingle
from camera import Camera
from cursor import Cursor
from music import Player as MusicPlayer

# from hud import HUD
from UI import HUD, Avatar, HealthBar, Ammo, Money, UIElement
from levels import Level


class LevelOne(Level):
    music = MusicPlayer(
        sound_effects={
            "shot": pygame.mixer.Sound("assets/sounds/shot.wav"),
            "empty_clip": pygame.mixer.Sound("assets/sounds/empty_clip.wav"),
            "zombie_attack": pygame.mixer.Sound("assets/sounds/zombie_attack.wav"),
            "zombie_attack_2": pygame.mixer.Sound("assets/sounds/zombie_attack_2.wav"),
        },
        background_effects={
            "zombie_background_effect_1": pygame.mixer.Sound(
                "assets/sounds/zombie_background_effect_1.mp3"
            ),
            "zombie_background_effect_2": pygame.mixer.Sound(
                "assets/sounds/zombie_background_effect_2.wav"
            ),
            "zombie_background_effect_3": pygame.mixer.Sound(
                "assets/sounds/zombie_background_effect_3.wav"
            ),
            "empty_background_effect": pygame.mixer.Sound(
                "assets/sounds/empty_background_effect.wav"
            ),

        },
        background_music={
            "background_music_1": pygame.mixer.Sound(
                "assets/sounds/background_music_1.wav"
            ),
        },
    )

    def setup(self):
        self.music.loop_background_effect(["zombie_background_effect_1", "zombie_background_effect_2", "zombie_background_effect_3", "empty_background_effect"])
        self.music.play_background_music("background_music_1", loop=True)
        return super().setup()

    def update(self):
        left_enemies = len(self.EnemyGroup.sprites())
        if left_enemies > 0:
            if left_enemies == 1:
                self.music.background_effects_loop_running_channels = 1
            else:
                self.music.background_effects_loop_running_channels = self.music.background_effects_channel_count
            self.music.loop_background_effect(["zombie_background_effect_1", "zombie_background_effect_2", "zombie_background_effect_3", "empty_background_effect"])
        else:
            self.music.clear_background_effects_loop()
        self.music.update()
        return super().update()

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
        self.video.set_size((self.director.width, self.director.height))

    def update(self):
        if self.video.active == False:
            self.finish()

    def event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.skip()

    def draw(self, screen, window_scale):
        self.video.draw(screen, (0, 0))

    def finish(self):
        self.director.set_scene(LevelOne(self.director))
        self.video.close()

    def skip(self):
        key_moments = [6, 13.9]
        current_time = self.video.get_playback_data()["time"]
        if current_time > key_moments[-1]:
            self.finish()
            return
        next_key_moment = [x for x in key_moments if x > current_time][0]
        self.video.seek(
            next_key_moment, relative=False, accurate=True, seek_by_bytes=False
        )
        # print("skipped from", current_time, ", to:", next_key_moment)
        # print("time now:", self.video.get_playback_data()["time"])


def main():
    pygame.init()
    director = Director()
    # director.set_scene(Intro(director))
    director.set_scene(LevelOne(director))
    director.setup()
    director.loop()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
