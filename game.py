import json
from typing import Any
import pygame, sys

# from pygamevideo import Video
from Video.player import Video
from director import Director, Scene

from Character import Player, CameraAwareGroupSingle
from camera import Camera
from cursor import Cursor
from music import Player as MusicPlayer

# from hud import HUD
from UI import HUD, Avatar, HealthBar, Ammo, Money, UIElement, UIGroup, Button
from levels import Level


class MenuScene(Scene):
    music = MusicPlayer(
        background_music={
            "background": pygame.mixer.Sound("assets/sounds/main_menu_background.mp3")
        },
        sound_effects={
            "purchase": pygame.mixer.Sound("assets/sounds/purchase.mp3"),
        },
    )

    def __init__(self, director):
        super().__init__(director)
        self.music.play_background_music("background", loop=True)


    def update(self):
        self.menu.update()
        self.music.update()

    def event(self, event):
        self.menu.event(event)

    def draw(self, screen, window_scale):
        screen.blit(
            pygame.transform.scale(
                self.background, (self.director.width, self.director.height)
            ),
            (0, 0),
        )
        self.menu.draw(screen)


class GamePlay(Level):
    music = MusicPlayer(
        sound_effects={
            "shot": pygame.mixer.Sound("assets/sounds/shot.wav"),
            "empty_clip": pygame.mixer.Sound("assets/sounds/empty_clip.wav"),
            "zombie_attack": pygame.mixer.Sound("assets/sounds/zombie_attack.wav"),
            "zombie_attack_2": pygame.mixer.Sound("assets/sounds/zombie_attack_2.wav"),
            "death": pygame.mixer.Sound("assets/sounds/death.wav"),
            "perk": pygame.mixer.Sound("assets/sounds/perk.mp3"),
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
        self.map = self.director.storage.get("map", "city")
        self.music.loop_background_effect(
            [
                "zombie_background_effect_1",
                "zombie_background_effect_2",
                "zombie_background_effect_3",
                "empty_background_effect",
            ]
        )
        self.music.play_background_music("background_music_1", loop=True)
        return super().setup()

    def update(self):
        left_enemies = len(self.EnemyGroup.sprites())
        if left_enemies > 0:
            if left_enemies == 1:
                self.music.background_effects_loop_running_channels = 1
            else:
                self.music.background_effects_loop_running_channels = (
                    self.music.background_effects_channel_count
                )
            self.music.loop_background_effect(
                [
                    "zombie_background_effect_1",
                    "zombie_background_effect_2",
                    "zombie_background_effect_3",
                    "empty_background_effect",
                ]
            )
        else:
            self.music.clear_background_effects_loop()
        self.music.update()
        return super().update()


class Pause(MenuScene):
    background = pygame.image.load("assets/menus/pause.png")
    def __init__(self, director):
        super().__init__(director)

    def setup(self):
        self.menu = UIGroup(
            [
                Button(
                    path=["assets/menus/continue.png", "assets/menus/continue_hover.png"],
                    callback=self.return_to_game,
                    scale=0.7,
                ),
                Button(
                    path=["assets/menus/back.png", "assets/menus/back_hover.png"],
                    callback=self.back_to_main_menu,
                    scale=0.7,
                ),
                Button(
                    path=["assets/menus/quit.png", "assets/menus/quit_hover.png"],
                    callback=sys.exit,
                    scale=0.56,
                ),
            ],
            x=520,
            y=380,
            space_y=20,
        )
        self.menu.stack_vertical()

    def back_to_main_menu(self):
        self.director.set_scene(MainMenu(self.director))

    def return_to_game(self):
        self.director.set_scene(self.director._game)




class Intro(Scene):
    def __init__(self, director):
        super().__init__(director)

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
        self.director.set_scene(MainMenu(self.director))
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


class MainMenu(MenuScene):
    background = pygame.image.load("assets/menus/main_menu.png")

    def __init__(self, director):
        super().__init__(director)

    def setup(self):
        self.menu = UIGroup(
            [
                Button(
                    path=["assets/menus/start.png", "assets/menus/start_hover.png"],
                    callback=self.map_menu,
                    scale=0.7,
                ),
                Button(
                    path=["assets/menus/quit.png", "assets/menus/quit_hover.png"],
                    callback=sys.exit,
                    scale=0.7,
                ),
            ],
            x=200,
            y=310,
            space_y=20,
        )
        self.menu.stack_vertical()

    def map_menu(self):
        self.director.set_scene(SelectMap(self.director), pause_music=False)


class SelectMap(MenuScene):
    background = pygame.image.load("assets/menus/map_menu.png")

    def __init__(self, director):
        super().__init__(director)

    def setup(self):
        self.menu = UIGroup(
            [
                Button(
                    path=["assets/menus/city.png", "assets/menus/city_hover.png"],
                    callback=lambda: self.set_map("city"),
                    scale=0.7,
                ),
                Button(
                    path=["assets/menus/forest.png", "assets/menus/forest_hover.png"],
                    callback=lambda: self.set_map("forest"),
                    scale=0.7,
                ),
            ],
            space_x=20,
            y=200,
        )
        self.menu.stack_horizontal()
        self.menu.x = self.director.width / 2 - self.menu.rect.width / 2
        self.menu.stack_horizontal()

    def set_map(self, map):
        self.director.storage.set("map", map)
        self.director.set_scene(SelectLevel(self.director), flush_music=True)


class SelectLevel(MenuScene):
    background = pygame.image.load("assets/menus/level_menu.png")

    def __init__(self, director):
        super().__init__(director)

    def setup(self):
        self.menu = UIGroup(
            [
                Button(
                    path=["assets/menus/1.png", "assets/menus/1_hover.png"],
                    callback=lambda: self.set_level(1),
                    scale=0.7,
                ),
                Button(
                    path=["assets/menus/2.png", "assets/menus/2_hover.png"],
                    callback=lambda: self.set_level(2),
                    scale=0.7,
                ),
                Button(
                    path=["assets/menus/3.png", "assets/menus/3_hover.png"],
                    callback=lambda: self.set_level(3),
                    scale=0.7,
                ),
            ],
            space_x=20,
            y=200,
        )
        self.menu.stack_horizontal()
        self.menu.x = self.director.width / 2 - self.menu.rect.width / 2
        self.menu.stack_horizontal()

    def set_level(self, level):
        self.director.storage.set("level", level)
        self.director.set_scene(PerkMenu(self.director))


class PerkMenu(MenuScene):
    background = pygame.image.load("assets/menus/perks_menu.png")

    def __init__(self, director):
        super().__init__(director)

    def setup(self):
        self.menu = UIGroup(
            [
                Button(
                    path=["assets/menus/ammo.png", "assets/menus/ammo_hover.png"],
                    callback=lambda: self.buy_perk("ammo"),
                    scale=0.7,
                ),
                Button(
                    path=["assets/menus/health.png", "assets/menus/health_hover.png"],
                    callback=lambda: self.buy_perk("health"),
                    scale=0.7,
                ),
                Button(
                    path=[
                        "assets/menus/multiplier.png",
                        "assets/menus/multiplier_hover.png",
                    ],
                    callback=lambda: self.buy_perk("multiplier"),
                    scale=0.7,
                ),
                UIGroup(
                    [
                        Button(
                            path=[
                                "assets/menus/continue.png",
                                "assets/menus/continue_hover.png",
                            ],
                            callback=self.continue_the_gameplay,
                            scale=0.7,
                        ),
                        Button(
                            path=[
                                "assets/menus/back.png",
                                "assets/menus/back_hover.png",
                            ],
                            callback=self.go_back_to_select_level,
                            scale=0.7,
                        ),
                    ],
                    space_y=5,
                    x=970,
                    y=530,
                ),
            ],
            space_x=20,
            y=100,
            x=410,
        )

        perks = self.menu.elements[:3]
        buttons = self.menu.elements[3]

        self.menu.stack_horizontal(perks)
        buttons.stack_vertical()

    def buy_perk(self, perk):
        price = 100
        amount = self.director.storage.get(perk, 0)
        money = self.director.storage.get("money", 0)
        if money >= price:
            self.director.storage.set("money", money - price)
            self.director.storage.set(perk, amount + 1)
            self.music.play_sound_effect("purchase")

    def continue_the_gameplay(self):
        self.director.set_scene(GamePlay(self.director))

    def go_back_to_select_level(self):
        self.director.set_scene(SelectLevel(self.director))


def main():
    pygame.init()
    director = Director()
    director.set_scene(Intro(director))
    director.setup()
    director.loop()
    pygame.quit()
    sys.exit()




if __name__ == "__main__":
    main()
