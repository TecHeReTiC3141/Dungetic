from scripts.constants_and_sources import *


class Heretic:
    strength = 3
    left_stop, right_stop, up_stop, down_stop = [False for i in '....']

    def __init__(self, x, y, width, height, health, direction, inventory,
                 speed=5, target=None, weapon='none', location=None, attack_time=0, half_attack_time=0, backpack=None,
                 size=1.):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.direction = direction
        self.inventory = inventory

        self.light_zone = []
        self.visible_zone = pygame.Surface((self.width, self.height))
        self.phys_rect = pygame.Rect(x, y, self.width, int(self.height))
        self.active_zone = pygame.Rect(x - 50, y - 50, self.width * 2, int(self.height * 1.5))

        self.points = [(x, y), (x + width // 2, y), (x + width, y),
                       (x + width, y + height // 2),
                       (x + width, y + height), (x + width // 2, y + height),
                       (x, y + height),
                       (x, y + height // 50)]

        self.location = location
        self.attack_time = attack_time
        self.half_attack_time = half_attack_time
        self.backpack = backpack
        self.weapon = weapon
        self.target = target
        self.size = size
        self.speed = speed

    def hit(self, entity):
        entity.health -= self.strength
        self.attack_time = self.strength * 10
        print('ouch')

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.x > -3 and not self.left_stop:
            self.x = max(self.x - self.speed, 0)
            self.active_zone.update(self.x, self.y, self.width, self.height)
            self.phys_rect.update(self.x, self.y, self.width, self.height)
            self.direction = 'left'

        if keys[pygame.K_d] and not self.right_stop:
            self.direction = 'right'
            self.x = min(self.x + self.speed, display_width - self.width)
            self.active_zone.update(self.x, self.y, self.width, self.height)
            self.phys_rect.update(self.x, self.y, self.width, self.height)


        if keys[pygame.K_w] and not self.up_stop:
            self.y = max(self.y - self.speed, 0)
            self.active_zone.update(self.x, self.y, self.width, self.height)
            self.phys_rect.update(self.x, self.y, self.width, self.height)
            self.direction = 'up'

        if keys[pygame.K_s] and not self.down_stop:
            self.direction = 'down'
            self.y = min(self.y + self.speed, display_height - self.height)
            self.phys_rect.update(self.x, self.y, self.width, self.height)
            self.active_zone.update(self.x, self.y, self.width, self.height)



    @staticmethod
    def tp(room):
        global curr_room
        curr_room = room

    def draw_object(self, display: pygame.Surface):
        self.visible_zone.fill((0, 0, 0))
        # if self.backpack and self.directions == 'right':
        #     self.backpack.draw_on_self(self.x + 25, self.y + 45)
        # elif self.backpack and self.directions == 'up':
        #     self.backpack.draw_on_self(self.x - 5, self.y + 45)
        # if self.weapon != 'none' and self.directions == 'right':
        #     self.weapon.draw_object(self.x + 65 - ((self.half_attack_time -
        #                                                   self.attack_time) // 2 if self.attack_time > self.half_attack_time else 0),
        #                                self.y + 30)
        # elif self.weapon != 'none' and self.directions == 'up':
        #     self.weapon.draw_object(self.x - 15, self.y + 30 + ((self.half_attack_time -
        #                                                                   self.attack_time) // 2 if self.attack_time > self.half_attack_time else 0))
        pygame.draw.rect(self.visible_zone, (0, 0, 0), (self.x, self.y, 75, 100))
        eye_colour = (0, 0, 0)
        self.visible_zone.blit(heretic_images[self.direction], (0, 0))
        display.blit(self.visible_zone, self.phys_rect)
    #  pygame.draw.rect(self.visible_zone, (0, 0, 0), (self.x - 15, self.y - 30, 110, 25))
    #    pygame.draw.rect(self.visible_zone, RED, (self.x - 10, self.y - 28,
    #       int(100.0 * float(self.health) / 100.0), 21))
