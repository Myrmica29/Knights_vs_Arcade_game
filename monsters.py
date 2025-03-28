import pygame
import random


class Monster(pygame.sprite.Sprite):

    def __init__(self, screen, time, group):
        super().__init__(group)

        # Image
        sprite_sheet = pygame.image.load("ressources/monsters/alien_spaceships.png")
        self.image = pygame.Surface([32, 32])
        x = random.randint(0, 15)
        y = random.randint(0, 15)
        self.image.blit(sprite_sheet, (0, 0), (32 * x, 32 * y, 32, 32))

        # Position
        self.rect = self.image.get_rect()
        self.space_y = (screen.get_height() - 700) / 2
        self.line = random.randint(0, 9)
        self.rect.y = self.space_y + self.line * 70 + (70 - self.rect.height) / 2
        self.rect.x = screen.get_width() + 50

        # Ability
        self.ability = 0
        if 1200 > time >= 120:
            self.ability = 75
        elif 1020 > time >= 900:
            self.ability = 65
        elif 1200 > time >= 1020:
            self.ability = 60
        elif time >= 1200:
            self.ability = 50


        # Speed
        self.speed = 1
        # Speed 2
        if 180 > time >= 180:
            if random.randint(0, 20) == 0:
                self.speed = 2
        elif 240 > time >= 180:
            if random.randint(0, 12) == 0:
                self.speed = 2
        elif 300 > time >= 240 == 0:
            if random.randint(0, 6):
                self.speed = 2
        elif 360 > time >= 300:
            if random.randint(0, 3) == 0:
                self.speed = 2
        elif 420 > time >= 360:
            if random.randint(0, 2) == 0:
                self.speed = 2
        elif 480 > time >= 420:
            self.speed = 2
            if random.randint(0, 3) == 0:
                self.speed = 1
        elif time >= 480:
            if random.randint(0, 5) == 0:
                self.speed = 2
        # Speed 3
        if 540 > time >= 480:
            if random.randint(0, 70) == 0:
                self.speed = 3
        elif 600 > time >= 540:
            if random.randint(0, 55) == 0:
                self.speed = 3
        elif time >= 600:
            if random.randint(0, 40) == 0:
                self.speed = 3

    def change_line(self):
        if self.line == 0:
            self.line = 1
        elif self.line == 9:
            self.line = 8
        else:
            r = random.randint(0, 1)
            if r == 0:
                self.line -= 1
            else:
                self.line += 1
        self.rect.y = self.space_y + self.line * 70 + (70 - self.rect.height) / 2

    def update(self, player_group):
        self.rect.x -= self.speed
        if self.ability:
            if random.randint(0, self.ability) == 0:
                self.change_line()

        # Destroy if touching player
        if pygame.sprite.spritecollide(self, player_group, False):
            self.kill()

    def check_end(self):
        if self.rect.x <= -50:
            return True
        return False
