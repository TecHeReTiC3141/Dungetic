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

    def __init__(self, x, y, width, height, life_time: int, type: str, speed=3):
        super().__init__((width, height))
        self.rect = self.get_rect(topleft=(x, y))
        self.life_time = life_time
        self.directions = pygame.math.Vector2()
        self.speed = speed
        self.type = type

    def draw_object(self, display, x=0, y=0):
        pass

    def move(self, tick=0):
        pass


    def delete(self):
        pass

class Blood(Particle):

    def __init__(self, x, y, width, height, life_time: int, type: str, speed=3):
        super().__init__(x, y, width, height, life_time, type, speed=speed)
        self.type = type
        if type == 'up':
            self.directions = pygame.math.Vector2(random.uniform(-4, 4),
                                                  random.uniform(-4, -2))
        elif type == 'down':
            self.directions = pygame.math.Vector2(0, 0)
            self.life_time //= 3

    def draw_object(self, display, x=0, y=0):
        self.fill(RED) #e61624
        display.blit(self, self.rect)
        self.life_time -= 1

    def move(self, tick=0):
        if self.directions.length():
            norm_dir = self.directions.normalize() * self.speed
            self.rect.move_ip(round(norm_dir.x), round(norm_dir.y))
        self.directions.y += phys_eps
        if self.type == 'up':
            self.directions.x = self.directions.x - phys_eps if self.directions.x > 0 else  self.directions.x + phys_eps

    def delete(self):
        return SplatBlood(self.rect.left, self.rect.top,
                          100, 100,
                          random.randint(120, 180), type='background', speed=1)

class SplatBlood(Blood):

    def __init__(self, x, y, width, height, life_time: int, type: str, speed=3):
        super().__init__(x, y, width, height, life_time, type, speed=speed)
        self.rect.width = random.randint(12, 18)
        self.rect.height = random.randint(12, 18)
        self.half_life_time = self.life_time // 2
        self.set_colorkey(BLACK)
        self.set_alpha(255)
        self.directions = pygame.math.Vector2(-1, -1)

    def draw_object(self, display, x=0, y=0):
        pygame.draw.ellipse(self, RED, (0, 0, self.rect.width, self.rect.height))
        display.blit(self, self.rect)
        self.life_time -= 1

    def move(self, tick=0):
        if not tick % 15 and self.life_time >= self.half_life_time:
            norm_dir = self.directions.normalize() * self.speed
            self.rect.move_ip(norm_dir * 1.5)
            self.rect.width -= norm_dir.x * 1.5
            self.rect.height -= norm_dir.y * 1.5
        else:
            self.set_alpha(round(255 * self.life_time / self.half_life_time))

    def delete(self):
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

# TODO add particles which show hit damage
