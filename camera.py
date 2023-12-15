import pygame


class Camera:
    def __init__(self, width, height, scene_width, scene_height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.scene_width = scene_width
        self.scene_height = scene_height

    def apply(self, entity):
        if not hasattr(entity, "rect"):
            rect = entity.get_rect()
        else:
            rect = entity.rect
        return rect.move(self.camera.topleft)

    def update(self, target):
        shooting_x_pos = self.width // 3
        target_x_offset = shooting_x_pos - target.rect.centerx
        reaction_x = min(0, target_x_offset)


        reaction_x = max(-(self.scene_width - self.width), reaction_x)  # right
        # x = max(min(0, self.width // 3 - target.rect.x), x)  # right
        y = 0

        print(f"error: {reaction_x}, {self.camera.x}")
        self.camera.x = reaction_x