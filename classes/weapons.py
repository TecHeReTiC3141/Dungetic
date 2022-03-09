import pygame

class Weapon:
    sprite = None
    damage = None
    capability = None
    hit_range = None

    def draw_object(self, display):
        pass

class Fist(Weapon):
    sprite = {'left': pygame.image.load('../images/weapons/fist/fist_left.png'),
              'right':  pygame.image.load('../images/weapons/fist/fist_right.png')}
    damage = 6
    capability = 45
    hit_range = 40



