import pygame
from scripts.constants_and_sources import *

pygame.mixer.init()


class Loot:
    sprite = {}
    descr = []
    deletion = False

    def draw_object(self, display: pygame.Surface, x=0, y=0, direct='left'):
        try:
            if isinstance(self.sprite, dict):
                display.blit(self.sprite[direct], (x, y))
            else:
                display.blit(self.sprite, (x, y))
        except KeyError:
            print(f'Unknown direction for {self}')

    def picked_up(self, entity):
        if len(entity.inventory) < entity.max_capacity:
            entity.inventory.append(self)

    def interact(self, entity):
        pass


class Weapon(Loot):
    damage = None
    capability = None
    hit_range = None
    knockback = None
    hit_sound = None

    def picked_up(self, entity):
        if isinstance(entity.weapon, Fist):
            entity.weapon = self
        else:
            if len(entity.inventory) < entity.max_capacity:
                entity.inventory.append(self)

    def interact(self, entity):
        if not isinstance(entity.weapon, Fist):
            entity.inventory.append(entity.weapon)
            entity.weapon.deletion = False

        entity.weapon = self
        self.deletion = True


class Fist(Weapon):
    sprite = {'left': pygame.image.load('../images/weapons/fist/fist_left.png'),
              'right': pygame.image.load('../images/weapons/fist/fist_right.png')}
    damage = 5
    knockback = 25
    capability = 45
    hit_range = 40
    hit_sound = pygame.mixer.Sound('../sounds/weapons/fist/punch.mp3')


class Knife(Weapon):
    sprite = {'right': pygame.image.load('../images/weapons/knife/iron_knife.png'),
              'left': pygame.transform.flip(pygame.image.load('../images/weapons/knife/iron_knife.png'),
                                            flip_x=True, flip_y=False)}
    descr = ['Острый железный клинок']
    damage = 8
    knockback = 35
    capability = 50
    hit_range = 50
    hit_sound = pygame.mixer.Sound('../sounds/weapons/sword/swing.mp3')


class Money(Loot):
    sprite = None
    value = None

    def picked_up(self, entity):
        if hasattr(entity, 'loot'):
            entity.loot.append(self)
        else:
            entity.actual_money += self.value
            self.value = 0


class GoldCoin(Money):
    sprite = pygame.image.load('../images/Money/gold_coin.png').convert_alpha()
    value = 5


class SilverCoin(Money):
    sprite = pygame.image.load('../images/Money/silver_coin.png').convert_alpha()
    value = 2


class Consumable(Loot):
    effect = ()


class Potion(Consumable):
    descr = ['Неизвестно, что хуже - ',
             "Попробовать эту дрянь или",
             "умереть от ран"]

    effect = ('+ 15', '#FF0000')

    def interact(self, entity):
        entity.actual_health = min(entity.actual_health + 15, 100)
        self.deletion = True
        return self.effect

    sprite = pygame.image.load('../images/Comsubles/live_potion.png')


class Armor(Loot):
    persist = 0.
    max_durab = 100
    section = 'body'
    height = 10
    width = 2

    def __init__(self):
        self.durab = Armor.max_durab

    def draw_object(self, display: pygame.Surface, x=0, y=0, direct='left'):
        display.blit(self.sprite[direct], (x - self.width, y - self.height))


    def interact(self, entity):
        if hasattr(entity, 'body_armor'):
            entity.body_armor = self
            self.deletion = True


# TODO implement armor functionality


class Helmet(Armor):
    width = 3

    descr = ['Простой кожаный шлем,',
             "пробитый несколько раз"]

    max_durab = 50
    persist = 0.25

    section = 'head'
    sprite = {i: pygame.image.load(f'../images/armor/leather_helmet/leather_helmet_{i}.png').convert_alpha() for i in
              directions}

    def interact(self, entity):
        if hasattr(entity, 'head_armor'):
            if isinstance(entity.head_armor, Helmet):
                entity.inventory.append(entity.head_armor)
                entity.head_armor.deletion = False

            entity.head_armor = self
            self.deletion = True
