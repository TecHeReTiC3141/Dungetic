import pygame

class Weapon:
    sprite = None
    damage = None
    capability = None
    hit_range = None
    knockback = None
    hit_sound = None

    def draw_object(self, display):
        pass

    def picked_up(self, entity):
        entity.weapon = self



class Fist(Weapon):
    sprite = {'left': pygame.image.load('../images/weapons/fist/fist_left.png'),
              'right':  pygame.image.load('../images/weapons/fist/fist_right.png')}
    damage = 5
    knockback = 25
    capability = 45
    hit_range = 40
    hit_sound = pygame.mixer.Sound('../sounds/weapons/fist/punch.mp3')


class Knife(Weapon):
    sprite = {'right': pygame.image.load('../images/weapons/knife/iron_knife.png'),
              'left': pygame.transform.flip(pygame.image.load('../images/weapons/knife/iron_knife.png'),
                                             flip_x=True, flip_y=False)}
    damage = 8
    knockback = 35
    capability = 50
    hit_range = 50
    hit_sound = pygame.mixer.Sound('../sounds/weapons/sword/swing.mp3')


class Money:
    sprite = None
    value = None

    def picked_up(self, entity):
        entity.actual_money += self.value
        self.value = 0


class GoldCoin(Money):
    sprite = pygame.image.load('../images/Money/gold_coin.png').convert_alpha()
    value = 5

class SilverCoin(Money):
    sprite = pygame.image.load('../images/Money/silver_coin.png').convert_alpha()
    value = 2



