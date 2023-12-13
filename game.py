import pygame, sys
from director import Director, Scene
from player import Player



class Game(Scene):
    def __init__(self, director):
        Scene.__init__(self, director)
        self.PlayerGroup = pygame.sprite.GroupSingle()
        self.Player = Player(0, 0, 300, 300, (255, 0, 0), 1, self.director)
        self.PlayerGroup.add(self.Player)


    def update(self):
        self.PlayerGroup.update()


    def event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            self.director.set_scene(Pause(self.director))
        self.PlayerGroup.sprite.event(event)

    def draw(self, screen, window_scale):
        background = pygame.Rect((0, 0), (self.director.width*window_scale, self.director.height*window_scale))
        pygame.draw.rect(screen, (0, 255, 0), background)

        self.PlayerGroup.draw(screen, window_scale)

    def foo(self):
        pass

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