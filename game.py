import pygame, sys
from Scene.MenuScene import MenuScene
from Scene.Scene import Scene

from Video.player import Video
from director import Director

from music import Player as MusicPlayer

from UI import UIGroup, Button
from Scene.Level import Level


class GamePlay(Level):
    """
    This is a class called `GamePlay` that inherits from `Level`. It has a `music` attribute which is an instance of `MusicPlayer`. The `MusicPlayer` is initialized with a dictionary of sound effects, where each sound effect is associated with a key. The sound effects are loaded from specific file paths.
    """

    def setup(self):
        """
        Perform the setup for the game.
        @return The result of the superclass's setup method.
        """
        self.map = self.director.storage.get("map", "city")
        self.music = MusicPlayer(
            sound_effects={
                "shot": pygame.mixer.Sound("assets/sounds/shot.wav"),
                "empty_clip": pygame.mixer.Sound("assets/sounds/empty_clip.wav"),
                "zombie_attack": pygame.mixer.Sound("assets/sounds/zombie_attack.wav"),
                "zombie_attack_2": pygame.mixer.Sound(
                    "assets/sounds/zombie_attack_2.wav"
                ),
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
        """
        Update the game state. Check the number of enemies left. If there are enemies remaining, adjust the background effects loop based on the number of enemies. If there is only one enemy left, set the background effects loop to 1 channel. Otherwise, set it to the specified number of channels. Start playing a looped background effect with a list of effect names. If there are no enemies left, clear the background effects loop. Finally, update the music.
        """
        """
        Update the game state. Check the number of enemies left. If there are enemies remaining, adjust the background effects loop based on the number of enemies. If there is only one enemy left, set the background effects loop to 1 channel. Otherwise, set it to the specified number of channels. Start playing a looped background effect with a list of effect names. If there are no enemies left, clear the background effects loop. Finally, update the music.
        """
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
    """
    A class representing the pause menu scene in a game.
    """

    background = pygame.image.load("assets/menus/pause.png")

    def __init__(self, director):
        """
        Initialize an instance of the class with a director object.
        @param director - the director object
        @return None
        """
        super().__init__(director)

    def setup(self):
        """
        Set up the UI group for the menu. The menu consists of two buttons: "Continue" and "Quit".
        - The "Continue" button has two images for normal and hover states, and when clicked, it calls the `return_to_game` callback function. It is scaled to 0.7.
        - The "Quit" button also has two images for normal and hover states, and when clicked, it calls the `sys.exit` function to exit the program. It is scaled to 0.56.
        - The menu is positioned at coordinates (520, 380) and has a vertical spacing of 20 between the buttons.
        """
        self.menu = UIGroup(
            [
                Button(
                    path=[
                        "assets/menus/continue.png",
                        "assets/menus/continue_hover.png",
                    ],
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
        """
        Return to the main menu by setting the current scene to the MainMenu scene.
        @param self - the current object
        @return None
        """
        self.director.set_scene(MainMenu(self.director))

    def return_to_game(self):
        """
        Return to the game scene by setting the current scene of the director to the game scene.
        """
        self.director.set_scene(self.director._game)


class Intro(Scene):
    """
    A class representing an introductory scene in a video game or animation.
    @param director - the director controlling the scene
    @method setup - sets up the scene by initializing a video and setting its size
    @method update - updates the scene, currently checks if the video is active
    @method skip - allows the user to skip the intro by seeking to the next key moment in the video
    @return None
    """

    def __init__(self, director):
        """
        Initialize an instance of the class with a director object.
        @param director - the director object
        @return None
        """
        super().__init__(director)

    def setup(self):
        """
        Set up the video by creating a Video object with the specified video file path. Set the size of the video to match the width and height of the director.
        @return None
        """
        self.video = Video("assets/intro.mp4")
        self.video.set_size((self.director.width, self.director.height))

    def update(self):
        """
        Check if the video is active. If it is not active, call the `finish()` method.
        @return None
        """
        if self.video.active == False:
            self.finish()

    def event(self, event):
        """
        Handle a specific event in a Pygame application. If the event is a key press event and the key pressed is the spacebar, call the `skip()` method.
        @param event - the event to handle
        """
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.skip()

    def draw(self, screen, window_scale):
        """
        Draw the video on the screen at the specified position.
        @param screen - the screen to draw on
        @param window_scale - the scale of the window
        @return None
        """
        self.video.draw(screen, (0, 0))

    def finish(self):
        """
        Finish the current scene and set the scene to the main menu. Close the video.
        @return None
        """
        self.director.set_scene(MainMenu(self.director))
        self.video.close()

    def skip(self):
        """
        Skip to the next key moment in the video playback.
        @return None
        """
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
    """
    A class representing the main menu scene in a game. Inherits from the MenuScene class.
    """

    background = pygame.image.load("assets/menus/main_menu.png")

    def __init__(self, director):
        """
        Initialize an instance of the class with a director object.
        @param director - the director object
        @return None
        """
        super().__init__(director)

    def setup(self):
        """
        Set up the user interface for the game.
        @return None
        """
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
        """
        Display the map menu by setting the current scene to the SelectMap scene.
        @return None
        """
        self.director.set_scene(SelectMap(self.director), pause_music=False)


class SelectMap(MenuScene):
    """
    A scene for selecting a map in a game menu.
    @param MenuScene - The base class for the menu scene.
    @param background - The background image for the scene.
    @param director - The game director.
    @method __init__ - Initializes the SelectMap scene.
    @method setup - Sets up the menu with buttons for map selection.
    @method set_map - Sets the selected map in the game storage.
    """

    background = pygame.image.load("assets/menus/map_menu.png")

    def __init__(self, director):
        """
        Initialize an instance of the class with a director object.
        @param director - the director object
        @return None
        """
        super().__init__(director)

    def setup(self):
        """
        Set up the menu for the game.
        @return None
        """
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
        """
        Set the map for the game by storing it in the storage and then setting the scene to the SelectLevel scene.
        @param map - the map to be set
        @return None
        """
        self.director.storage.set("map", map)
        self.director.set_scene(SelectLevel(self.director), flush_music=True)


class SelectLevel(MenuScene):
    """
    A scene for selecting a level in a game menu.
    @param MenuScene - The base class for the menu scene.
    @param background - The background image for the level menu.
    @param director - The game director.
    @method __init__ - Initializes the SelectLevel scene.
    @method setup - Sets up the level menu by creating buttons and arranging them in a menu group.
    @method set_level - Sets the selected level in the game storage.
    """

    background = pygame.image.load("assets/menus/level_menu.png")

    def __init__(self, director):
        """
        Initialize an instance of the class with a director object.
        @param director - the director object
        @return None
        """
        super().__init__(director)

    def setup(self):
        """
        Set up the menu for the game. The menu consists of multiple buttons, each with its own image, hover image, callback function, and scale. The buttons are arranged horizontally with a spacing of 20 pixels. The menu is positioned vertically at y=200. The menu is then centered horizontally on the screen.
        """
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
        """
        Set the level of the game to the specified level.
        @param level - the level to set
        @return None
        """
        self.director.storage.set("level", level)
        self.director.set_scene(PerkMenu(self.director))


class PerkMenu(MenuScene):
    """
    A class representing a menu scene for perks in a game.
    """

    background = pygame.image.load("assets/menus/perks_menu.png")

    def __init__(self, director):
        """
        Initialize an instance of the class with a director object.
        @param director - the director object
        @return None
        """
        super().__init__(director)

    def setup(self):
        """
        Set up the UI menu for the game. This includes creating a `UIGroup` object and adding `Button` objects to it. The buttons represent different perks that can be purchased in the game. The `path` parameter of each button specifies the image file paths for the button's normal and hover states. The `callback` parameter specifies the function to be called when the button is clicked. The `scale` parameter specifies the size of the button.
        """
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
        """
        Buy a perk for the player.
        @param self - the instance of the class
        @param perk - the perk to buy
        @return None
        """
        price = 100
        amount = self.director.storage.get(perk, 0)
        money = self.director.storage.get("money", 0)
        if money >= price:
            self.director.storage.set("money", money - price)
            self.director.storage.set(perk, amount + 1)
            self.music.play_sound_effect("purchase")

    def continue_the_gameplay(self):
        """
        Continue the gameplay by setting the current scene to a new instance of the GamePlay scene.
        @return None
        """
        self.director.set_scene(GamePlay(self.director))

    def go_back_to_select_level(self):
        """
        Go back to the select level scene by setting the current scene of the director to the SelectLevel scene.
        @param self - the current instance of the class
        @return None
        """
        self.director.set_scene(SelectLevel(self.director))


def main():
    """
    The main function initializes the Pygame library, creates a Director object, sets the initial scene to Intro, sets up the director, starts the game loop, and cleans up resources before exiting the program.
    @return None
    """
    pygame.init()
    pygame.mixer.init()
    director = Director()
    director.set_scene(Intro(director))
    director.setup()
    director.loop()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
