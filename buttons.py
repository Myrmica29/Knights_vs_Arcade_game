import pygame


class EditButton:
    def __init__(self, number, total, screen):
        self.number = number
        self.image = pygame.image.load(f"ressources/knights/knight-{number}.png")
        # x = ((screen.get_width() - 250) / (total + 1)) * number + 250
        x = 250 + 100 * number
        y = screen.get_height() - 150
        self.pos = (x, y)
        self.rect = self.image.get_rect(center=self.pos)

    def check_collide(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False


class ClassicButton:
    def __init__(self, path, pos):
        self.image = pygame.image.load(path)
        self.pos = pos
        self.rect = self.image.get_rect(center=pos)

    def check_collide(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False


class ConfigButton:
    def __init__(self, name, current_type, current_value, current_joy, pos):
        self.name = name
        self.typ = current_type
        self.value = current_value
        self.joy = current_joy
        # Image
        self.image = pygame.Surface([256, 64], pygame.SRCALPHA)
        self.update_image()
        # Pos
        self.pos = pos
        self.rect = self.image.get_rect(topleft=pos)

    def update_image(self, fill=False):
        self.image = pygame.Surface([256, 64], pygame.SRCALPHA)
        if fill:
            self.image.fill((137, 142, 127))
        image_part_1 = pygame.image.load(f"ressources/controls/{self.typ}.png")
        self.image.blit(image_part_1, (0, 0), (0, 0, 64, 64))
        if self.typ == "JOYBUTTONUP":
            image_part_2 = pygame.image.load(f"ressources/controls/numbers/a{self.value}.png")
            self.image.blit(image_part_2, (96, 0), (0, 0, 64, 64))
        image_part_3 = pygame.image.load(f"ressources/controls/numbers/a{self.joy}.png")
        self.image.blit(image_part_3, (192, 0), (0, 0, 64, 64))

    def check_collide(self, pos):
        if self.rect.collidepoint(pos):
            return True
        return False
