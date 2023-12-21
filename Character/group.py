import pygame


class CameraAwareGroup(pygame.sprite.Group):
    def __init__(self, *sprites):
        super().__init__(*sprites)
        self.camera = None

    def set_camera(self, camera):
        self.camera = camera

    def draw(self, surface):
        for spr in self.sprites():
            self.spritedict[spr] = surface.blit(spr.image, self.camera.apply(spr))
        self.lostsprites = []

    def event(self, event):
        for spr in self.sprites():
            spr.event(event)


class CameraAwareGroupSingle(pygame.sprite.GroupSingle):
    def __init__(self, *sprites):
        super().__init__(*sprites)
        self.camera = None

    def set_camera(self, camera):
        self.camera = camera

    def draw(self, surface):
        for spr in self.sprites():
            surface.blit(spr.image, self.camera.apply(spr))

    def event(self, event):
        self.sprite.event(event)
