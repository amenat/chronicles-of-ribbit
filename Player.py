import pygame
from Constants import Constants as const
from Sprite import *
from character import Character
from projectile import spell_img


# basics of jumping is commented out for now unless we add later
class Player(Character):

    def __init__(self, x=const.SCREEN_W / 2, y=const.SCREEN_H / 2, speed=const.PLAYER_SPEED):
        super().__init__(x, y, speed,
                         Sprite([pygame.image.load("images/Rabbit_Idle_Front.png")],     #standing
                                [pygame.image.load("images/Rabbit_Idle_Left.png")],     #left
                                [pygame.image.load("images/Rabbit_Idle_Right.png")],     #right
                                [pygame.image.load("images/Rabbit_Idle_Back.png")],     #up
                                [pygame.image.load("images/Rabbit_Idle_Front.png")]))    #down
        # amount of time after death player is invuln
        self.last_move = LEFT
        self.invuln = 0
        self.spawn_at = None
        self.death_sequence = [pygame.image.load("images/Rabbit_Death_1.png"),
                               pygame.image.load("images/Rabbit_Death_2.png"),
                               pygame.image.load("images/Rabbit_Death_3.png"),
                               pygame.image.load("images/Rabbit_Death_4.png"),
                               pygame.image.load("images/Rabbit_Death_5.png"),
                               pygame.image.load("images/Rabbit_Death_6.png"),
                               pygame.image.load("images/Rabbit_Death_7.png"),
                               pygame.image.load("images/Rabbit_Death_8.png")]

    def warp(self, coords):
        """Sets the x, y position of the player to a given set of coordinates"""
        self.x = coords[0]
        self.y = coords[1]

    def move(self, keys):
        if self.spawn_at:
            return

        is_moving = False

        if keys[pygame.K_LEFT]:
            is_moving = True
            self.move_left()

        if keys[pygame.K_RIGHT]:
            is_moving = True
            self.move_right()

        if keys[pygame.K_UP]:
            is_moving = True
            self.move_up()

        if keys[pygame.K_DOWN]:
            is_moving = True
            self.move_down()

        if not is_moving:
            if self.sprite.direction != STANDING:
                self.last_move = self.sprite.direction
            self.sprite.face_forwards()

    def died(self, enemies, room):
        if self.invuln <= 0:
            for enemy in enemies:
                if self.get_rect().colliderect(enemy.get_rect()):
                    self.spawn_at = room.get_player_spawn_point()
                    self.invuln = 90
                    return True
        elif self.invuln > 0:
            self.invuln -= 1

    def draw(self, screen):
        if self.spawn_at is None:
            Character.draw(self, screen)

        elif self.invuln > 0:
            if self.invuln >= 51:
                idx = int((90 - self.invuln) / 5)
                screen.blit(self.death_sequence[idx], (self.x, self.y))

        else:
            self.warp(self.spawn_at)
            self.spawn_at = None

