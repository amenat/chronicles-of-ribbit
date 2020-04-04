import pygame
from Constants import Constants as const


class Character:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

        # TO be defined by child class
        self.img = None

        # TODO: update these dynamically from imagesize using functions
        self.width = 16
        self.height = 32

    def draw(self, screen):
        # draw the image on x, y; else draw a red rectangle
        # TODO: consider image size and centre it
        if self.img:
            screen.blit(self.img, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (255,0,0), (self.x, self.y, self.width, self.height), 0)

    def move_left(self):
        self.x = max(self.x - self.speed, 0)

    def move_right(self):
        self.x = min(self.x + self.speed, const.SCREEN_W - self.width)

    def move_up(self):
        self.y = max(self.y - self.speed, 0)

    def move_down(self):
        self.y = min(self.y + self.speed, const.SCREEN_H - self.height)

    # TODO: thinking sprite class will be used by this class
    def advance_animation(self):
        pass

    def stop_moving_animation(self):
        pass

