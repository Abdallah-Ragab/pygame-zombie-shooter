import math
import pygame


class Cursor:
    def __init__(self, player, min_distance=150, max_distance=700, max_angle=45, DEBUG=False):
        """
        Initialize a Cursor object.

        Args:
            player (Player): The player object.
            min_distance (int, optional): The minimum distance between the cursor and the player. Defaults to 150.
            max_distance (int, optional): The maximum distance between the cursor and the player. Defaults to 700.
            max_angle (int, optional): The maximum angle of rotation for the cursor. Defaults to 45.
            DEBUG (bool, optional): Flag to enable debugging mode. Defaults to False.
        """
        self.player = player
        self.image = pygame.image.load("assets/cursor.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()

        self.DEBUG = DEBUG

        self.min_distance = min_distance
        self.max_distance = max_distance
        self.max_angle = max_angle
        self.x_player_offset = 0
        self.y_player_offset = -100

        self.player_pos = self.claculate_player_pos()

    def claculate_player_pos(self):
        """
        Calculate the position of the player relative to the camera.

        Returns:
            tuple: The x and y coordinates of the player.
        """
        camera = self.player.scene.camera
        player_rect = camera.apply(self.player.rect)
        return (
            player_rect.centerx + self.x_player_offset,
            player_rect.centery + self.y_player_offset,
        )

    def calculate_point(self, distance, angle):
        """
        Calculate the x and y coordinates of a point based on distance and angle.

        Args:
            distance (float): The distance from the origin.
            angle (float): The angle in degrees.

        Returns:
            tuple: The x and y coordinates of the point.
        """
        x = distance * math.cos(math.radians(angle))
        y = distance * math.sin(math.radians(angle))
        return x, y

    def convert_point(self, x, y):
        """
        Convert x and y coordinates to distance and angle.

        Args:
            x (float): The x coordinate.
            y (float): The y coordinate.

        Returns:
            tuple: The distance and angle of the point.
        """
        distance = math.sqrt(x**2 + y**2)
        angle = math.degrees(math.atan2(y, x))
        return distance, angle

    def point_from_player(self, distance, angle):
        """
        Calculate the x and y coordinates of a point relative to the player.

        Args:
            distance (float): The distance from the player.
            angle (float): The angle in degrees.

        Returns:
            tuple: The x and y coordinates of the point.
        """
        x, y = self.calculate_point(distance, angle)
        return x * self.player.direction + self.player_pos[0], y + self.player_pos[1]

    def calculate_position(self, screen):
        """
        Calculate the position of the cursor on the screen.

        Args:
            screen (Surface): The screen surface.

        Returns:
            None
        """
        if self.DEBUG:
            self.draw_debug(screen)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        if self.player.direction == -1 and mouse_x > self.player_pos[0]:
            return
        elif self.player.direction == 1 and mouse_x < self.player_pos[0]:
            return

        dx = (mouse_x - self.player_pos[0])
        dy = (mouse_y - self.player_pos[1])

        if self.player.direction == -1:
            dx *= -1

        distance, angle = self.convert_point(dx, dy)

        angle_abs = abs(angle)
        angle_sign = 1 if angle > 0 else -1

        max_angle = abs(self.max_angle / 2)
        max_distance = min(
            self.max_distance,
            screen.get_rect().width - self.player_pos[0],
        )
        if self.player.direction == -1:
            max_distance = min(self.max_distance, self.player_pos[0])

        min_distance = self.min_distance

        distance = max(min_distance, distance)
        distance = min(max_distance, distance)
        _angle = min(max_angle, angle_abs) * angle_sign

        x, y = self.point_from_player(distance, _angle)

        self.rect.center = (x, y)

    def draw_debug(self, screen):
        """
        Draw debug lines and circles on the screen.

        Args:
            screen (Surface): The screen surface.

        Returns:
            None
        """
        pygame.draw.circle(screen, (255, 0, 0), self.player_pos, self.min_distance, 1)
        pygame.draw.circle(screen, (255, 0, 0), self.player_pos, self.max_distance, 1)

        pygame.draw.line(
            screen,
            (255, 255, 0),
            self.player_pos,
            self.point_from_player(self.max_distance, abs(self.max_angle / 2)),
        )
        pygame.draw.line(
            screen,
            (0, 255, 0),
            self.player_pos,
            self.point_from_player(self.max_distance, 0),
        )
        pygame.draw.line(
            screen,
            (255, 255, 0),
            self.player_pos,
            self.point_from_player(self.max_distance, -abs(self.max_angle / 2)),
        )

    def draw(self, screen):
        """
        Draw the cursor on the screen.

        Args:
            screen (Surface): The screen surface.

        Returns:
            None
        """
        self.calculate_position(screen)
        screen.blit(self.image, self.rect)

    def update(self):
        """
        Update the position of the player.

        Returns:
            None
        """
        self.player_pos = self.claculate_player_pos()

