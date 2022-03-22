import pygame


class Particle(pygame.Surface):

    def __init__(self, x, y, width, height, life_time: int, direction: str):
        super().__init__((width, height))

