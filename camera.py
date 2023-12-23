import pygame


class Camera:
    def __init__(self, width, height, scene_width, scene_height):
        """
        Initializes a Camera object.

        Args:
            width (int): The width of the camera view.
            height (int): The height of the camera view.
            scene_width (int): The width of the scene.
            scene_height (int): The height of the scene.
        """
        self.rect = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.scene_width = scene_width
        self.scene_height = scene_height

    def apply(self, entity):
        """
        Applies the camera's position to the given entity.

        Args:
            entity (pygame.Rect or object with 'rect' attribute): The entity to apply the camera to.

        Returns:
            pygame.Rect: The updated position of the entity.
        """
        if isinstance(entity, pygame.Rect):
            rect = entity
        elif hasattr(entity, "rect"):
            rect = entity.rect
        else:
            rect = entity.get_rect()
        return rect.move(self.rect.topleft)

    def update(self, target):
        """
        Updates the camera's position based on the target entity.

        Args:
            target (object with 'direction' and 'rect' attributes): The target entity.

        """
        shooting_x_pos = self.width // 3
        if target.direction == -1:
            shooting_x_pos = self.width - shooting_x_pos
        target_x_offset = shooting_x_pos - target.rect.centerx
        reaction_x = min(0, target_x_offset)
        reaction_x = max(-(self.scene_width - self.width), reaction_x)
        self.rect.x = reaction_x
