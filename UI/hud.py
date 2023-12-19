import pygame
from .ui_element import UIElement
from .button import Button
from .ui_group import UIGroup


class HUD(UIGroup):
    def __init__(
        self,
        player,
        elements: [UIElement | Button | UIGroup] = None,
        background: UIElement | Button | UIGroup = None,
        x=0,
        y=0,
        right=None,
        padding_x=0,
        padding_y=0,
        space_x=0,
        space_y=0,
    ):
        super().__init__(
            elements, background, x, y, right, padding_x, padding_y, space_x, space_y
        )
        self.player = player

    def update(self):
        super().update()
        print("-"*20)
        for element in self.elements:
            print(f"{element.__class__.__name__}| x:{element.x}, y:{element.y}| w:{element.width}, h:{element.height}")
        print("-"*20)


    def draw(self, screen):
        super().draw(screen)

    def position(self):
        super().position()

        ammo = next(filter(lambda element: isinstance(element, Ammo), self.elements))
        avatar = next(
            filter(lambda element: isinstance(element, Avatar), self.elements)
        )
        elements = list(
            filter(lambda element: not isinstance(element, Ammo), self.elements)
        )

        self.stack_vertical(elements)

        ammo.set_y(avatar.y + avatar.height - ammo.height)
        ammo.set_right(avatar.right + avatar.width + self.padding_x)

        print("-"*10, "POSITION", "-"*10)
        for element in self.elements:
            print(f"{element.__class__.__name__}| x:{element.x}, y:{element.y}| w:{element.width}, h:{element.height}")
        print("-"*20)


class Avatar(UIElement):
    pass


class HealthBar(UIGroup):
    def __init__(
        self,
        player,
        elements: [UIElement | Button] = None,
        background: UIElement | Button = None,
        x=0,
        y=0,
        right=None,
        padding_x=0,
        padding_y=0,
        space_x=0,
        space_y=0,
    ):
        super().__init__(
            elements, background, x, y, right, padding_x, padding_y, space_x, space_y
        )
        self.player = player

    def position(self):
        super().position()
        self.stack_over()

    def update(self):
        super().update()
        self.elements[1].width = (
            self.elements[0].width * self.player.health / self.player.max_health
        )


class Ammo(UIElement):
    def __init__(
        self,
        player,
        x=0,
        y=0,
        image=None,
        path=None,
        right=None,
        width=None,
        height=None,
    ):
        super().__init__(x, y, image, path, right, width, height)
        self.font = pygame.font.Font(None, 28)
        self.player = player

    def draw(self, screen):
        super().draw(screen)
        text = self.font.render(str(self.player.bullets), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (self.x + self.width / 2, self.y + self.height / 2 + 7)
        screen.blit(text, text_rect)


class Money(UIElement):
    def __init__(
        self,
        player,
        x=0,
        y=0,
        image=None,
        path=None,
        right=None,
        width=None,
        height=None,
    ):
        super().__init__(x, y, image, path, right, width, height)
        self.font = pygame.font.Font(None, 28)
        self.player = player

    def draw(self, screen):
        super().draw(screen)
        text = self.font.render(str(1350), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (self.x + self.width / 2 - 5, self.y + self.height / 2 - 5)
        screen.blit(text, text_rect)
