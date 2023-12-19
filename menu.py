import pygame

class MenuElement:
    def __init__(self, *args, **kwargs):
        self.image = None
        self.width = 0
        self.height = 0
        self.right = 0
        self.x = 0
        self.y = 0

    def update(self):
        pass

    def draw(self, screen, y, x=None, right=None):
        if not (x or right):
            pass
        elif x:
            self.x = x
        elif right:
            self.x = self.x_from_right(screen, right, self.width)
        
        self.y = y
    
    def x_from_right(self, screen, right, width):
        return screen.get_width() - right - width
    
class Menu:
    elemnents = []

    def __init__(self, *args, **kwargs):
        pass

    def update(self):
        for element in self.elemnents:
            element.update()

    def draw(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))

        for element in self.elemnents:
            element.draw()

    def stack(self, x, y)