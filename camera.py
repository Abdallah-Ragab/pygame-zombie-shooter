import pygame


class Camera:
    def __init__(self, width, height, scene_width, scene_height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.scene_width = scene_width
        self.scene_height = scene_height

    def apply(self, entity):
        if isinstance(entity, pygame.Rect):
            rect = entity
        elif hasattr(entity, "rect"):
            rect = entity.rect
        else:
            rect = entity.get_rect()
        return rect.move(self.camera.topleft)

    def update(self, target):
        shooting_x_pos = self.width // 3
        target_x_offset = shooting_x_pos - target.rect.centerx
        reaction_x = min(0, target_x_offset)
        reaction_x = max(-(self.scene_width - self.width), reaction_x)  # right
        self.camera.x = reaction_x
