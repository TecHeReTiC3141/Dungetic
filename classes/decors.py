import pygame
from scripts.constants_and_sources import *

class Decor(pygame.Surface):

    def draw_object(self, display, x=None, y=None):
        pass

    def move(self):
        pass


class Particle(Decor):

    def __init__(self, x, y, width, height, life_time: int, direction: str):
        super().__init__((width, height))
        self.life_time = life_time
        self.directions = direction.split()
        self.deleted = False

    def draw_object(self, display, x=0, y=0):
        pass

    def move(self):
        pass


class Banner(Decor):

    def __init__(self, x, y, text, life_time: int, color='Black'):
        self.text = active_font.render(text, True, 'Black')
        self.surf = pygame.Surface(self.text.get_size())
        self.rect = self.surf.get_rect(topleft=(x, y))
        self.surf.fill('White')
        self.surf.blit(self.text, (0, 0))
        self.life_time = life_time

    def draw_object(self, display: pygame.Surface, x=0, y=0):
        display.blit(self.surf, self.rect if x == y == 0 else (x, y))
        self.life_time -= 1

# TODO create some concrete particles
