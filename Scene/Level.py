import pygame
from Character import CameraAwareGroupSingle, Player, CameraAwareGroup, EnemyManager
from UI import HUD
from camera import Camera
from Scene.Scene import Scene
from cursor import Cursor
from music import Player as MusicPlayer


class Level(Scene):
    """
    Represents a level in the game.

    Attributes:
    - music: The music player for the level.
    - background: The background image of the level.
    - screen_width: The width of the game screen.
    - screen_height: The height of the game screen.
    - scene_width: The width of the level scene.
    - scene_height: The height of the level scene.
    - camera: The camera object for the level.
    - Player: The player character in the level.
    - PlayerGroup: The group containing the player character.
    - EnemyGroup: The group containing the enemy characters.
    - EnemyManager: The manager for the enemy characters.
    - cursor: The cursor object in the level.
    - hud: The heads-up display in the level.
    """


    def __init__(self, director):
        """
        Initializes a new instance of the Level class.

        Parameters:
        - director: The director object for the game.
        """
        Scene.__init__(self, director)

    def setup(self):
        """
        Sets up the level by loading the background image, initializing the camera,
        creating the player character and enemy groups, and setting up the cursor and HUD.
        """
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
        """
        Updates the level by updating the music player, player group, enemy group,
        enemy manager, camera, cursor, HUD, and checking the win condition.
        """
        self.music.update()
        self.PlayerGroup.update()
        self.EnemyGroup.update()
        self.EnemyManager.update()
        self.camera.update(self.Player)
        self.cursor.update()
        self.hud.update()
        self.check_win_condition()

    def draw(self, screen, window_scale):
        """
        Draws the level by blitting the background image, drawing the player group,
        enemy group, HUD, and cursor on the screen.

        Parameters:
        - screen: The game screen to draw on.
        - window_scale: The scale factor for the game window.
        """
        screen.blit(self.background, self.camera.apply(self.background))
        self.PlayerGroup.draw(screen)
        self.EnemyGroup.draw(screen)
        self.hud.draw(screen)
        self.cursor.draw(screen)

    def event(self, event):
        """
        Handles the events in the level, such as key presses and player/enemy group events.

        Parameters:
        - event: The event to handle.
        """
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            from game import Pause
            self.director.set_scene(Pause(self.director))

        self.PlayerGroup.sprite.event(event)
        self.EnemyGroup.event(event)

    def check_win_condition(self):
        """
        Checks the win condition of the level and sets the appropriate scene if the player wins or loses.
        """
        if self.Player.DEAD:
            self.director.set_scene(GameOver(self.director))
        elif self.EnemyManager.all_dead():
            self.director.set_scene(Win(self.director))

    def reward_player(self):
        """
        Rewards the player by increasing their money in the game storage.
        """
        money = self.director.storage.get("money", 0)
        money += 100
        self.director.storage.set("money", money)


class GameOver(Scene):
    def __init__(self, director):
        """
        Initializes a GameOver object.

        Args:
            director (Director): The game director object.
        """
        Scene.__init__(self, director)

    def setup(self):
        """
        Set up the GameOver scene.
        """
        self.game_over_text = pygame.font.SysFont("Arial", 50).render(
            "Game Over", True, (255, 255, 255)
        )
        window_center = (self.director.width / 2, self.director.height / 2)

    def update(self):
        """
        Update the GameOver scene.
        """
        pass

    def event(self, event):
        """
        Handle events in the GameOver scene.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            from game import MainMenu
            self.director.set_scene(MainMenu(self.director))

    def draw(self, screen, window_scale):
        """
        Draw the GameOver scene.

        Args:
            screen (pygame.Surface): The surface to draw on.
            window_scale (float): The scale factor for the window.
        """
        """
        Draw the GameOver scene.

        Args:
            screen (pygame.Surface): The screen surface to draw on.
            window_scale (float): The scale factor for the window size.
        """
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
        """
        Initializes a Win scene.

        Args:
            director (Director): The game director.
        """
        Scene.__init__(self, director)

    def setup(self):
        """
        Set up the Win scene.
        """
        self.win_text = pygame.font.SysFont("Arial", 50).render(
            "You Win!", True, (255, 255, 255)
        )
        window_center = (self.director.width / 2, self.director.height / 2)

    def update(self):
        """
        Update the Win scene.
        """
        pass

    def event(self, event):
        """
        Handle events in the Win scene.

        Args:
            event (pygame.event.Event): The event to handle.
        """
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            from game import MainMenu
            self.director.set_scene(MainMenu(self.director))
    def draw(self, screen, window_scale):
        """
        Draw the Win scene.

        Args:
            screen (pygame.Surface): The screen to draw on.
            window_scale (float): The scale factor for the window.
        """
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