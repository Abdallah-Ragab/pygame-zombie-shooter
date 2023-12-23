import pygame
import sys
from fractions import Fraction
from storage import JsonStorage


class Director:
    """
    The Director class manages the game loop and controls the flow of the game.

    Attributes:
        width (int): The width of the game window.
        height (int): The height of the game window.
        screen (pygame.Surface): The game window surface.
        aspect_ratio (Fraction): The aspect ratio of the game window.
        scale (float): The scaling factor for the game window.
        title (str): The title of the game window.
        scene (Scene): The current scene being displayed.
        quit_flag (bool): Flag indicating whether the game should quit.
        clock (pygame.time.Clock): The game clock for controlling the frame rate.

    Methods:
        setup(): Sets up the game window with the specified title.
        loop(): The main game loop that handles events, updates, and rendering.
        set_scene(scene, pause_music=True, flush_music=False): Sets the current scene.
        aspect_ratio_resize(event_width, event_height): Resizes the game window while maintaining the aspect ratio.
        quit(): Sets the quit flag to True, ending the game loop.
    """
    storage = JsonStorage

    def __init__(self):
        self.width = 1280
        self.height = 720
        self.screen = pygame.display.set_mode(
            (self.width, self.height), pygame.RESIZABLE
        )
        self.aspect_ratio = Fraction(self.screen.get_width(), self.screen.get_height())
        self.scale = 1

        self.title = "Zombie Shooter - Team 7"
        self.scene = None
        self.quit_flag = False
        self.clock = pygame.time.Clock()

    def setup(self):
        """
        Sets up the game window with the specified title.
        """
        pygame.display.set_caption(self.title)

    def loop(self):
        """
        The main game loop that handles events, updates, and rendering.
        """
        while not self.quit_flag:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.VIDEORESIZE:
                    self.aspect_ratio_resize(event.w, event.h)
                if event.type == pygame.QUIT:
                    self.quit()
                self.scene.event(event)  # Call event with the event
            self.scene.update()
            self.scene.draw(self.screen, self.scale)
            pygame.display.update()

    def set_scene(self, scene, pause_music=True, flush_music=False):
        """
        Sets the current scene.

        Args:
            scene (Scene): The scene to set as the current scene.
            pause_music (bool, optional): Flag indicating whether to pause the music. Defaults to True.
            flush_music (bool, optional): Flag indicating whether to flush the music. Defaults to False.
        """
        from Scene.Level import Level
        if isinstance(self.scene, Level) or issubclass(self.scene.__class__, Level):
            self._game = self.scene
        self.scene = scene

    def aspect_ratio_resize(self, event_width, event_height):
        """
        Resizes the game window while maintaining the aspect ratio.

        Args:
            event_width (int): The new width of the game window.
            event_height (int): The new height of the game window.
        """
        delta_width = (
            event_width - self.screen.get_width()
        ) / self.aspect_ratio.numerator
        delta_height = (
            event_height - self.screen.get_height()
        ) / self.aspect_ratio.denominator

        width_factor = event_width / self.width
        height_factor = event_height / self.height
        self.scale = min(width_factor, height_factor)
        new_width = int(self.width * self.scale)
        new_height = int(self.height * self.scale)
        self.screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)

    def quit(self):
        """
        Sets the quit flag to True, ending the game loop.
        """
        self.quit_flag = True


