import pygame
from scripts.constants_and_sources import *

class Decor(pygame.Surface):

    def draw_object(self, display, x=None, y=None):
        pass

    def move(self):
        pass


class Particle(Decor):

    def __init__(self, x, y, width, height, life_time: int, speed=3):
        super().__init__((width, height))
        self.rect = self.get_rect(topleft=(x, y))
        self.life_time = life_time
        self.directions = pygame.math.Vector2()
        self.speed = speed
        self.deleted = False

    def draw_object(self, display, x=0, y=0):
        pass

    def move(self):
        pass

class Blood(Particle):

    def __init__(self, x, y, width, height, life_time: int, type: str, speed=3):
        super().__init__(x, y, width, height, life_time, speed)
        if type == 'up':
            self.directions = pygame.math.Vector2(random.uniform(-2, 2),
                                                  random.uniform(-2, -1))
        elif type == 'down':
            self.directions = pygame.math.Vector2(random.uniform(-.5, .5),
                                                  1)

    def draw_object(self, display, x=0, y=0):
        self.fill('#e61624')
        display.blit(self, self.rect)
        self.life_time -= 1
        if self.life_time <= 0:
            self.deleted = True

    def move(self):
        if self.directions.length():
            self.rect.move_ip(self.directions.normalize() * self.speed)
        self.directions.y += .1
        self.directions.x = self.directions.x - .1 if self.directions.x > 0 else  self.directions.x - .1



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
