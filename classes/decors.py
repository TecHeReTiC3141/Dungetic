import pygame
from scripts.constants_and_sources import *

class Decor(pygame.Surface):

    def draw_object(self, display, x=None, y=None):
        pass

    def move(self):
        pass

    def delete(self):
        pass


class Particle(Decor):

    def __init__(self, x, y, width, height, life_time: int, speed=3):
        super().__init__((width, height))
        self.rect = self.get_rect(topleft=(x, y))
        self.life_time = life_time
        self.directions = pygame.math.Vector2()
        self.speed = speed

    def draw_object(self, display, x=0, y=0):
        pass

    def move(self):
        pass

    def delete(self):
        pass

class Blood(Particle):

    def __init__(self, x, y, width, height, life_time: int, type: str, speed=3):
        super().__init__(x, y, width, height, life_time, speed)
        self.type = type
        if type == 'up':
            self.directions = pygame.math.Vector2(random.uniform(-2, 2),
                                                  random.uniform(-6, -3))
        elif type == 'down':
            self.directions = pygame.math.Vector2(0,
                                                  0)
            self.life_time //= 3

    def draw_object(self, display, x=0, y=0):
        self.fill(RED) #e61624
        display.blit(self, self.rect)
        self.life_time -= 1

    def move(self):
        if self.directions.length():
            norm_dir = self.directions.normalize() * self.speed
            self.rect.move_ip(round(norm_dir.x), round(norm_dir.y))
        self.directions.y += phys_eps
        if self.type == 'up':
            self.directions.x = self.directions.x - phys_eps if self.directions.x > 0 else  self.directions.x + phys_eps

    def delete(self):
        return SplatBlood(self.rect.left, self.rect.top,
                          self.rect.width, self.rect.height,
                          random.randint(90, 180), type=None, speed=0)

class SplatBlood(Blood):

    def draw_object(self, display, x=0, y=0):
        super().draw_object(display, x, y)


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
