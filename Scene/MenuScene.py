from Scene.Scene import Scene
from music import Player as MusicPlayer


import pygame


class MenuScene(Scene):
    """
    A class representing a menu scene that inherits from the Scene class.
    """


    def __init__(self, director):
        """
        Initialize an instance of the Game class with a director parameter.

        Parameters:
        director (Director): The director object.

        Returns:
        None
        """
        super().__init__(director)
        self.music = MusicPlayer()
        self.music.add_background_music({"background": pygame.mixer.Sound("assets/sounds/main_menu_background.mp3")})
        self.music.add_sound_effects({"purchase": pygame.mixer.Sound("assets/sounds/purchase.mp3")})
        self.music.play_background_music("background", loop=True)

    def update(self):
        """
        Update the menu and music components of the game.
        @return None
        """
        self.menu.update()
        self.music.update()

    def event(self, event):
        """
        Handle an event by passing it to the menu object's event handler.
        @param event - the event to handle
        """
        self.menu.event(event)

    def draw(self, screen, window_scale):
        """
        Draw the game screen on the given surface with the specified window scale.
        @param screen - The surface to draw on.
        @param window_scale - The scale factor for the window.
        @return None
        """
        screen.blit(
            pygame.transform.scale(
                self.background, (self.director.width, self.director.height)
            ),
            (0, 0),
        )
        self.menu.draw(screen)