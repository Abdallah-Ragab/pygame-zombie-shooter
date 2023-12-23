import pygame
from .ui_element import UIElement
from .button import Button
from .ui_group import UIGroup


class HUD(UIGroup):
    def __init__(
        self,
        player,
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
        self.Player = player
        elements = [
            Avatar(self.Player, path="assets/hud/avatars/1.png"),
            HealthBar(
                self.Player,
                elements=[
                    UIElement(path="assets/hud/health_bar_back.png"),
                    UIElement(path="assets/hud/health_bar_front.png"),
                ],
            ),
            Ammo(self.Player, path="assets/hud/ammo.png"),
            Money(self.Player, path="assets/hud/money.png"),
            UIGroup(
                [
                    Button(path="assets/hud/ammo_perk.png",
                           callback=self.Player.use_ammo_perk),
                    Button(path="assets/hud/health_perk.png",
                            callback=self.Player.use_health_perk),
                    Button(path="assets/hud/multiplier_perk.png",
                            callback=self.Player.use_multiplier_perk),
                ],
                scale=1,
                y=0,
                space_x=0,
                padding_x=20,
            )
        ]
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

    def event(self, event):
        super().event(event)

    def position(self):
        super().position()

        avatar = self.elements[0]
        health_bar = self.elements[1]
        ammo = self.elements[2]
        money = self.elements[3]

        elements = [avatar, health_bar, money]

        self.stack_vertical(elements, align="right")

        ammo.set_y(avatar.y + avatar.height - ammo.height - ammo.height * 0.1)
        ammo.set_x(avatar.x - ammo.width)

        money = next(filter(lambda element: isinstance(element, Money), self.elements))
        money.set_x(money.x - 12)
        money.set_y(money.y - 10)

        perks = self.elements[4]
        perks.stack_horizontal()
        perks.set_y(30)



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
        money = self.player.scene.director.storage.get("money", 0)
        super().draw(screen)
        text = self.font.render(str(money), True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (self.x + self.width * 0.45, self.y + self.height * 0.52)
        screen.blit(text, text_rect)

