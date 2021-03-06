import pygame
from scripts.constants import *

pygame.mixer.init()


class Loot:
    sprite = {}
    descr = []
    deletion = False
    autopicked = False

    def draw_object(self, display: pygame.Surface, x=0, y=0, direct='right', in_inventory=False):
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

    def __copy__(self):
        pass


class Note(Loot):

    descr = ['Коричневый кусок пергамента', "На нем чтщто нацарапано"]
    # TODO Implement notes with random text (loren ipsum)


class Experience(Loot):

    sprite = {'left': pygame.transform.scale2x(pygame.image.load('../images/Money/exp.png')).convert_alpha()}
    value = 5
    autopicked = True

    def picked_up(self, entity):
        entity.experience += self.value
        self.value = 0


class Projectile:
    damage = 5
    def_speed = 7
    physics = False
    collided = False
    sprite = pygame.Surface((25, 25))
    eps = 1e-3
    sprite.set_colorkey('black')
    mask = pygame.mask.from_surface(sprite)

    def __init__(self, x, y, vector: pygame.math.Vector2, physics=False):
        pygame.draw.circle(self.sprite, '#0000CA',
                           (self.sprite.get_width() // 2, self.sprite.get_height() // 2),
                           self.sprite.get_width() // 2)

        self.rect = self.sprite.get_rect(topleft=(x, y))
        self.vector = vector
        self.physics = physics
        self.speed = randint(self.def_speed - 1, self.def_speed + 1)

    def draw_object(self, display: pygame.Surface):
        self.sprite.fill('black')
        pygame.draw.circle(self.sprite, '#0000CA',
                           (self.sprite.get_width() // 2, self.sprite.get_height() // 2),
                           self.sprite.get_width() // 2)
        display.blit(self.sprite, self.rect)

    def move(self):
        if self.vector.length():
            norm = self.vector.normalize()
            self.rect.move_ip(norm.x * self.speed, norm.y * self.speed)

        if self.physics:
            self.speed *= (1 - self.eps)
            if self.speed < .5:
                self.collided = True

    def collide(self, obstacles: list):
        pass


class Weapon(Loot):
    damage = None
    capability = None
    hit_range = None
    knockback = None
    hit_sound = None
    max_durability = None

    def __init__(self):
        self.durab = self.max_durability

    def picked_up(self, entity):
        if isinstance(entity.weapon, Fist):
            entity.weapon = self
        else:
            if len(entity.inventory) < entity.max_capacity:
                entity.inventory.append(self)

    def draw_object(self, display: pygame.Surface, x=0, y=0, direct='right', in_inventory=False):
        super().draw_object(display, x, y, direct, )
        if in_inventory:
            pygame.draw.rect(display, 'black', (x, y + self.sprite['right'].get_height(),
                                                self.sprite['right'].get_width(), 10), border_radius=5)
            pygame.draw.rect(display,
                             (255 * (1 - self.durab / self.max_durability), 255 * self.durab / self.max_durability, 0),
                             (x, y + self.sprite['left'].get_height(),
                              round((self.durab / self.max_durability)
                                    * self.sprite['right'].get_width()), 10), border_radius=5)

    def interact(self, entity):
        if not isinstance(entity.weapon, Fist):
            entity.inventory.append(entity.weapon)
            entity.weapon.deletion = False

        entity.weapon = self
        self.deletion = True


class Melee(Weapon):
    pass


class LongRange(Weapon):
    missile = Projectile

    def shoot(self, x, y, vector: pygame.math.Vector2) -> Projectile:
        self.durab -= 1
        return self.missile(x, y, vector)


class MagicBall(LongRange):

    descr = ['Странный сферический предмет', "Излучает непонятную энергию"]
    missile = Projectile
    max_durability = 15
    sprite = {'right': pygame.image.load('../images/weapons/magic_ball/magic_ball.png'),
              'left': pygame.transform.flip(pygame.image.load('../images/weapons/magic_ball/magic_ball.png'),
                                            flip_x=True, flip_y=False)}
    capability = 40



class Fist(Melee):
    sprite = {'left': pygame.image.load('../images/weapons/fist/fist_left.png'),
              'right': pygame.image.load('../images/weapons/fist/fist_right.png')}
    damage = 5
    knockback = 25
    capability = 45
    hit_range = 40
    max_durability = -1
    hit_sound = pygame.mixer.Sound('../sounds/weapons/fist/punch.mp3')


class Knife(Melee):
    sprite = {'right': pygame.image.load('../images/weapons/knife/iron_knife.png'),
              'left': pygame.transform.flip(pygame.image.load('../images/weapons/knife/iron_knife.png'),
                                            flip_x=True, flip_y=False)}

    damage = 8
    knockback = 35
    capability = 50
    hit_range = 50
    max_durability = 15
    descr = ['Острый железный клинок',
             f'Прочность: {max_durability}']
    hit_sound = pygame.mixer.Sound('../sounds/weapons/sword/swing.mp3')


class Money(Loot):
    sprite = None
    value = None
    autopicked = True

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
    max_durability = 100
    section = 'body'
    height = 10
    width = 2

    def __init__(self):
        self.durab = self.max_durability

    def draw_object(self, display: pygame.Surface, x=0, y=0, direct='right', in_inventory=False):
        display.blit(self.sprite[direct], (x - self.width, y - self.height))
        if in_inventory:
            pygame.draw.rect(display, 'black', (x, y + self.sprite['right'].get_height(),
                                                self.sprite['right'].get_width(), 10), border_radius=5)
            pygame.draw.rect(display,
                             (255 * (1 - self.durab / self.max_durability), 255 * self.durab / self.max_durability, 0),
                             (x, y + self.sprite['left'].get_height(),
                              round((self.durab / self.max_durability)
                                    * self.sprite['right'].get_width()), 10), border_radius=5)

    def interact(self, entity):
        if hasattr(entity, 'body_armor'):
            entity.body_armor = self
            self.deletion = True


class Helmet(Armor):
    width = 3

    descr = ['Простой кожаный шлем,',
             "пробитый несколько раз"]

    max_durability = 50
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
