import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, number, group):
        super().__init__(group)
        self.number = number
        self.image = pygame.image.load(f"ressources/knights/knight-{number}.png")
        self.pos = [0, number]
        self.rect = self.image.get_rect()
        self.kills = 0

    def move_up(self):
        if self.pos[1] - 1 >= 0:
            self.pos[1] -= 1

    def move_down(self):
        if self.pos[1] + 1 <= 9:
            self.pos[1] += 1

    def move_right(self):
        if self.pos[0] + 1 <= 5:
            self.pos[0] += 1

    def move_left(self):
        if self.pos[0] - 1 >= 0:
            self.pos[0] -= 1

    def update(self, screen):
        space_y = (screen.get_height() - 700) / 2
        self.rect.x = 10 + (self.number * 8) + (self.pos[0] * 65)
        self.rect.y = space_y + self.pos[1] * 70
