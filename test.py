import pygame
import os

class Animation:
    def __init__(self, name, frames_dir, frames_num, animation_speed, inverted=False):
        self.name = name
        self.frames_dir = frames_dir
        self.frames_num = frames_num
        self.animation_speed = animation_speed
        self.inverted = inverted



fps = 60
pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Test")


def set_animation(name, invert=False):
    global animation, frames_dir, frames, frames_num, frame_index, animation_finished, animation_speed, inverted
    animation = name
    frames_dir = f"C:/Users/BigBoss/Desktop/zombie/{animation}/"
    frames = os.listdir(frames_dir)
    frames.sort()
    frames_num = len(frames)
    frame_index = 0
    animation_speed = 1
    inverted = False
    if invert:
        frames.reverse()
        inverted = True

set_animation("idle")

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if animation == "attack":
                    if animation_finished:
                        set_animation("attack")
                else: set_animation("attack")
            if event.key == pygame.K_w:
                if animation == "idle":
                    set_animation("idle to walk")
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                if animation == "walk":
                    set_animation("idle to walk", invert=True)

    animation_finished = True if frame_index >= frames_num else False


    if animation == "attack" and animation_finished:
        set_animation("idle")

    if animation == "idle to walk" and animation_finished:
        if inverted:
            set_animation("idle")
        else:
            set_animation("walk")

    # display frames
    screen.fill((255, 255, 255))
    frame = pygame.image.load(frames_dir + frames[frame_index%frames_num])
    screen.blit(frame, (0, 0))

    # display frame index at top of screen
    font = pygame.font.SysFont("Arial", 20)
    text = font.render(str(frame_index % frames_num), True, (0, 0, 0))
    screen.blit(text, (0, 0))

    pygame.display.update()
    pygame.time.Clock().tick(fps)
    frame_index += animation_speed
