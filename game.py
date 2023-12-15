import pygame, sys
from director import Director, Scene
# from player import Player
from Character import Player
from camera import Camera



class Game(Scene):
    def __init__(self, director, ):
        Scene.__init__(self, director)
        self.PlayerGroup = pygame.sprite.GroupSingle()
        self.Player = Player(scene=self, x=0, y=720-220, height=200, width=200, speed=(1, 1))
        self.PlayerGroup.add(self.Player)
        self.background = pygame.image.load("D:\\game assets\\level1.jpg")
        self.screen_width = self.director.width
        self.screen_height = self.director.height
        self.scene_width = self.background.get_width()
        self.scene_height = self.background.get_height()
        self.camera = Camera(self.screen_width, self.screen_height, self.scene_width, self.scene_height)


    def update(self):
        self.PlayerGroup.update()
        self.camera.update(self.Player)



    def event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            self.director.set_scene(Pause(self.director))
        self.PlayerGroup.sprite.event(event)

    def draw(self, screen, window_scale):
        screen.blit(self.background, self.camera.apply(self.background))

        # self.camera.apply(self.PlayerGroup.sprite)
        # self.PlayerGroup.sprite.rect = self.camera.apply(self.PlayerGroup.sprite)

        self.PlayerGroup.draw(screen, window_scale)

class Pause(Scene):
    def __init__(self, director):
        Scene.__init__(self, director)
        self.pause_text = pygame.font.SysFont("Arial", 50).render("Pause", True, (255, 255, 255))
        window_center = (self.director.width/2, self.director.height/2)

    def update(self):
        pass

    def event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            self.director.set_scene(Game(self.director))

    def draw(self, screen, window_scale):
        background = pygame.Rect((0, 0), (self.director.width*window_scale, self.director.height*window_scale))
        pygame.draw.rect(screen, (0, 0, 255), background)
        # show the pause text at the center of the screen
        screen.blit(self.pause_text, (self.director.width/2 - self.pause_text.get_width()/2, self.director.height/2 - self.pause_text.get_height()/2))
        self.pause_text.get_rect().center = (self.director.width/2, self.director.height/2)


def main():
    pygame.init()
    director = Director()
    director.set_scene(Game(director))
    director.setup()
    director.loop()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()