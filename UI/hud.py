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
        scale=1,
    ):
        super().__init__(
            elements,
            background,
            x,
            y,
            right,
            padding_x,
            padding_y,
            space_x,
            space_y,
            scale,
        )
        self.player = player

    def update(self):
        super().update()

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

        self.stack_vertical(elements, align="right")

        ammo.set_y(avatar.y + avatar.height - ammo.height - ammo.height * 0.1)
        ammo.set_x(avatar.x - ammo.width)

        money = next(filter(lambda element: isinstance(element, Money), self.elements))
        money.set_x(money.x - 12)
        money.set_y(money.y - 10)


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
        scale=1,
    ):
        super().__init__(
            elements,
            background,
            x,
            y,
            right,
            padding_x,
            padding_y,
            space_x,
            space_y,
            scale,
        )
        self.player = player

    def position(self):
        super().position()
        self.stack_over()

    def update(self):
        super().update()
        front_bar = self.elements[1]
        back_bar = self.elements[0]

        front_bar.width = max(
            back_bar.width * self.player.health / self.player.max_health, 0
        )
        front_bar.image = front_bar.image.subsurface(
            0, 0, front_bar.width, front_bar.height
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
        scale=1,
    ):
        super().__init__(x, y, image, path, right, width, height, scale)
        self.font = pygame.font.Font(None, 28)
        self.player = player

    def draw(self, screen):
        super().draw(screen)
        text = self.font.render(str(self.player.bullets), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (self.x + self.width * 0.45, self.y + self.height * 0.55)
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
        scale=1,
    ):
        super().__init__(x, y, image, path, right, width, height, scale)
        self.font = pygame.font.Font(None, int(28 * self.scale))
        self.player = player

    def draw(self, screen):
        super().draw(screen)
        text = self.font.render(str(1050), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (self.x + self.width * 0.45, self.y + self.height * 0.52)
        screen.blit(text, text_rect)
