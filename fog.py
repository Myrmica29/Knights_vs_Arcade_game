import pygame
import random


class Fog(pygame.sprite.Sprite):

    def __init__(self, screen, time, group):
        super().__init__(group)

        # Image "lvl"
        lvl = 1
        if 660 > time >= 540:
            lvl = 2
            if random.randint(0, 5) == 0:
                lvl = 1
        elif 720 > time >= 660:
            lvl = 3
            if random.randint(0, 6) == 0:
                lvl = 1
            if random.randint(0, 5) == 0:
                lvl = 2
        elif 780 > time >= 720:
            lvl = 3
            if random.randint(0, 10) == 0:
                lvl = 1
            if random.randint(0, 6) == 0:
                lvl = 2
        elif time >= 780:
            lvl = 3
            if random.randint(0, 20) == 0:
                lvl = 1
            if random.randint(0, 10) == 0:
                lvl = 2

        # Load image and affect position
        self.image = pygame.image.load(f"ressources/fog/fog_{lvl}_1.png").convert_alpha()
        self.rect = self.image.get_rect()
        y = 0 - self.rect.height / 2
        x = random.randint(screen.get_width() - 500, screen.get_width() - self.rect.width)
        if time > 20:  # 480
            x = random.randint(screen.get_width() - 750, screen.get_width())
        elif time > 40:
            x = random.randint(350, screen.get_width())
        self.rect = self.image.get_rect(center=(x, y))

        # Point of destruction
        self.max = screen.get_height() + self.rect.height

    def update(self):
        # Move
        self.rect.y += 1
        # Check if out of view to destroy
        if self.rect.y > self.max:
            self.kill()
