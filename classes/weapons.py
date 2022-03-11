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
    damage = 5
    capability = 45
    hit_range = 40

class Knife(Weapon):
    sprite = {'left': pygame.image.load('../images/weapons/iron_knife.jpg'),
              'right': pygame.transform.flip(pygame.image.load('../images/weapons/iron_knife.jpg'),
                                             flip_x=True, flip_y=False)}
    damage = 8
    capability = 50
    hit_range = 50



