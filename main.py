import random

import pygame
from Constants import Constants as const
from room import Room
from Player import Player
from projectile import *
from enemies import Enemies
from pygame import mixer

# initialize pygame
pygame.init()


class Game:
    enemy_speed = const.ENEMY_SPEED_STARTING
    enemy_count = const.ENEMY_COUNT_STARTING

    def __init__(self):
        self.screen = pygame.display.set_mode((const.SCREEN_W, const.SCREEN_H))
        self.timer = pygame.time.Clock()
        pygame.display.set_caption(const.GAME_NAME)
        icon = pygame.image.load(const.ICON_FILE)
        pygame.display.set_icon(icon)
        self.player = Player()
        self.room = None
        self.score = 0
        self.lives = 5
        self.font = pygame.font.Font('freesansbold.ttf', 18)
        self.spell_sound = mixer.Sound(const.SPELL_SOUND)
        self.death_rattle = mixer.Sound(const.PLAYER_DEATH_SOUND)
        self.floor_tile = pygame.image.load("images/Floor_64px.gif")


    def new_room(self, last_exit):
        self.room = Room(entrance=Room.OPPOSITE_DIRECTIONS[last_exit])
        self.player.warp(self.room.get_player_spawn_point())
        self.room.enemies = Enemies(self.enemy_count, speed=self.enemy_speed)

    def run(self):
        run = True

        while run:

            # Create first room
            if self.room is None:
                self.new_room(Room.SOUTH)

            for event in pygame.event.get():
                # exit game
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN:
                    self.react_to_key_event(event.key)

            if len(self.room.enemies.alive_enemies) > 0:
                pass
                # for enemy in self.room.enemies.alive_enemies:
                #     if self.player.is_colliding(enemy.x, enemy.y, 32, 32):
                #         print("Dead!!!")
            elif not self.room.complete:
                self.room.complete_room()
                self.increase_difficulty()

            if self.room.complete:
                for exit_tile in self.room.exits:
                    if self.player.is_colliding(exit_tile.x, exit_tile.y, const.TILE_SIZE*2, const.TILE_SIZE*2):
                        self.new_room(last_exit=self.room.exit)

            self.react_to_keys()
            self.update_objects()
            self.draw()

            pygame.display.update()
            pygame.time.delay(50)
            self.timer.tick(const.FPS)

        pygame.quit()

    def react_to_key_event(self, key):
        if key == pygame.K_SPACE:     # fire bullet
            self.spell_sound.play()
            Bullet.fire_bullet(self.player)
        # if key == pygame.K_k:  # kill an enemy key TODO Remove, this is for debugging
        #     print('Enemy killed!')
        #     enemy = random.choice(self.room.enemies.alive_enemies)
        #     self.room.enemies.alive_enemies.remove(enemy)
        # if key == pygame.K_n and self.room.complete:  # next room key TODO Remove, this is for debugging
        #     self.new_room(self.room.exit, 4)

    def react_to_keys(self):
        self.player.move(pygame.key.get_pressed())

    def update_objects(self):
        Projectile.move_projectiles()

    def draw(self):
        self.screen.fill(const.BG_COLOUR)
        self.player.draw(self.screen)
        self.room.draw(self.screen) # TODO don't do this every time
        Projectile.draw_projectiles(self.screen)
        for i in range(10):
            for j in range(10):
                self.screen.blit(self.floor_tile, (i * 64, j * 64))

        self.room.draw(self.screen)

        # check kills and update score
        self.score += self.room.enemies.check_if_dead(Projectile.projectiles)
        for dead_enemy in self.room.enemies.dead_enemies:
            mixer.Sound(dead_enemy.get_death_sound()).play()
            self.room.enemies.dead_enemies.remove(dead_enemy)

        if self.lives <= 0:
            game_over = self.font.render('GAME OVER!', True, (255, 255, 255))
            self.screen.blit(game_over, (const.SCREEN_W//2, const.SCREEN_H//2))
            return

        self.player.draw(self.screen)
        Projectile.draw_projectiles(self.screen)


        self.room.enemies.check_if_dead(Projectile.projectiles)
        self.room.enemies.draw(self.screen)
        self.room.enemies.move()

        #check if enemy killed player
        if self.player.died(self.room.enemies.alive_enemies, self.room):
            self.death_rattle.play()
            self.lives -= 1

        # draw scoreboard
        scoreboard = self.font.render(f"Score: {self.score} | Lives: {self.lives}", True, (255,255,255))
        self.screen.blit(scoreboard, (const.TILE_SIZE + 5, const.TILE_SIZE + 5))

    def increase_difficulty(self):
        """Randomly increase either enemy speed or enemy count to increase difficulty"""
        difficulty_options = [const.INCREASE_COUNT, const.INCREASE_SPEED]
        difficulty_option = random.choice(difficulty_options)
        if difficulty_option == const.INCREASE_SPEED:
            print('increased speed')
            self.enemy_speed += const.SPEED_INCREASE
        elif difficulty_option == const.INCREASE_COUNT:
            print('increased count')
            self.enemy_count += const.COUNT_INCREASE


if __name__ == "__main__":
    game = Game()
    game.run()
