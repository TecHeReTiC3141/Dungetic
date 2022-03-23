import pygame


class Particle(pygame.Surface):

    def __init__(self, x, y, width, height, life_time: int, direction: str):
        super().__init__((width, height))
        self.life_time = life_time
        self.directions = direction.split()
        self.deleted = False

    def draw_object(self, display):
        pass

    def move(self):
        pass

    def delete(self):
        self.deleted = True


