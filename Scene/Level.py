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

        num_of_enemies = int(int(self.director.storage.get('level', 1))*5)
        # num_of_enemies = 5

        self.EnemyManager = EnemyManager(self, ['zombie girl', 'zombie cop'] , max_enemies=num_of_enemies)

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
        self.hud.event(event)

    def check_win_condition(self):
        """
        Checks the win condition of the level and sets the appropriate scene if the player wins or loses.
        """
        if self.Player.DEAD:
            from game import DeathScreen
            self.director.set_scene(DeathScreen(self.director))
        elif self.EnemyManager.all_dead():
            from game import VictoryScreen
            self.director.set_scene(VictoryScreen(self.director))

    def reward_player(self):
        """
        Rewards the player by increasing their money in the game storage.
        """
        money = self.director.storage.get("money", 0)
        money += 100
        self.director.storage.set("money", money)
