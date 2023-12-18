import pygame


class HUD:
    def __init__(self, player):
        self.player = player
        self.elements = [
            Avatar(self.player),
            HealthBar(self.player),
            Ammo(),
            Money()
        ]
        self.scale(0.7)

    def update(self):
        for element in self.elements:
            element.update()

    def draw(self, screen):
        # self.stack(screen, self.elements)
        self.Organize(screen)

    def stack (self, screen, elements = None, padding=5, start_y = 20):
        if elements is None:
            elements = self.elements

        y = start_y

        for element in elements:
            element.y = y
            element.draw(screen)
            y += element.height + padding

    def Organize(self, screen, padding_x=5, padding_y=5, start_y = 50, start_right = 50):

        elements = list(filter(lambda element: not isinstance(element, Ammo), self.elements))
        for element in elements:
            element.right = float(start_right)

        self.stack(screen, elements, padding_y, start_y)

        ammo = filter(lambda element: isinstance(element, Ammo), self.elements).__next__()
        avatar = filter(lambda element: isinstance(element, Avatar), self.elements).__next__()


        y = avatar.y + avatar.height - ammo.height
        right = avatar.right + avatar.width + padding_x

        ammo.y = y
        ammo.right = right

        ammo.draw(screen)

    def scale(self, scale_by):
        for element in self.elements:
            element.width *= scale_by
            element.height *= scale_by
            element.right *= scale_by
            element.y *= scale_by
            if isinstance(element, HealthBar):
                element.fore_bar = pygame.transform.scale(element.fore_bar, (element.fore_bar_width, element.height))
                element.back_bar = pygame.transform.scale(element.back_bar, (element.width, element.height))
            else:
                element.image = pygame.transform.scale(element.image, (element.width, element.height))



class HUDElement:
    def __init__(self):
        self.assets_dir = "assets/hud"

    def update(self):
        pass

    def draw(self, screen):
        pass

    def x_from_right(self, screen, distance, width):
        return screen.get_width() - distance - width



class Avatar(HUDElement):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.image = pygame.image.load(self.assets_dir + "/avatar.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = None
        self.y = 20
        self.right = 50

    def update(self):
        pass

    def draw(self, screen):
        self.x = self.x_from_right(screen, self.right, self.width)
        screen.blit(self.image, (self.x, self.y))




class HealthBar(HUDElement):
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.back_bar = pygame.image.load(self.assets_dir + "/health_bar_empty.png")
        self.fore_bar = pygame.image.load(self.assets_dir + "/health_bar_full.png")
        self.width = self.back_bar.get_width()
        self.height = self.back_bar.get_height()

        self.x = None
        self.y = 80

        self.right = 50
        self.max_health = self.player.health

    @property
    def fore_bar_width(self):
        health = self.player.health
        return max(self.width * health / self.max_health, 0)

    def update(self):
        # self.fore_bar = pygame.transform.scale(self.fore_bar, (self.fore_bar_width, self.back_bar.get_height()))
        self.fore_bar = self.fore_bar.subsurface((0, 0, self.fore_bar_width, self.height))
        print(self.fore_bar_width)

    def draw(self, screen):
        self.x = self.x_from_right(screen, self.right, self.width)
        screen.blit(self.back_bar, (self.x, self.y))
        screen.blit(self.fore_bar, (self.x, self.y))


class Ammo(HUDElement):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(self.assets_dir + "/ammo.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = None
        self.y = 140
        self.right = 50

    def update(self):
        pass

    def draw(self, screen):
        self.x = self.x_from_right(screen, self.right, self.width)
        screen.blit(self.image, (self.x, self.y))



class Money(HUDElement):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(self.assets_dir + "/money.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.x = None
        self.y = 200
        self.right = 50

    def update(self):
        pass

    def draw(self, screen):
        self.x = self.x_from_right(screen, self.right, self.width)
        screen.blit(self.image, (self.x, self.y))