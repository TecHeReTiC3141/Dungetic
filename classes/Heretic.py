import pygame

from scripts.constants_and_sources import *


class Heretic:
    left_stop, right_stop, up_stop, down_stop = [False for i in '....']
    colliding = None

    def __init__(self, x, y, width, height, health, direction, inventory,
                 speed=5, strength=5, target=None, weapon='none', location=None, attack_time=0,
                 half_attack_time=0, backpack=None, size=1.):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.direction = direction
        self.inventory = inventory
        self.strength = strength

        self.light_zone = []
        self.visible_zone = pygame.Surface((self.width, self.height))
        self.phys_rect = pygame.Rect(x, y, self.width, int(self.height))
        self.active_zone = pygame.Rect(x - 50, y - 50, self.width * 2, int(self.height * 1.5))

        self.attack_rect = None
        self.attack_surf = pygame.Surface((50, 50))
        self.attack_surf.set_colorkey(BLACK)

        self.collised_walls = {}

        self.location = location
        self.attack_time = attack_time
        self.half_attack_time = half_attack_time
        self.backpack = backpack
        self.weapon = weapon
        self.target = target
        self.size = size
        self.speed = speed

    def hit(self, entities: list):
        if self.attack_time <= 0:
            if self.direction == 'left':
                self.attack_rect = pygame.Rect(self.x - 50, self.y + self.height // 5,
                                          50, self.height // 5 * 3)
            elif self.direction == 'right':
                self.attack_rect = pygame.Rect(self.phys_rect.right, self.y + self.height // 5,
                                          50, self.height // 5 * 3)
            elif self.direction == 'up':
                self.attack_rect = pygame.Rect(self.x + self.width // 5, self.y - 30,
                                          self.width // 5 * 3, self.height // 5 * 3)
            elif self.direction == 'down':
                self.attack_rect = pygame.Rect(self.x + self.width // 5, self.y + self.height,
                                          self.width // 5 * 3, self.height // 5 * 3)
            for entity in entities:
                if entity.phys_rect.colliderect(self.attack_rect):
                    entity.health -= self.strength
                    dist_x, dist_y = get_rect_dist(entity.phys_rect, self.phys_rect)
                    entity.x += dist_x
                    entity.y += dist_y
                    entity.phys_rect.move_ip(dist_x, dist_y)
                    entity.active_zone.move_ip(dist_x, dist_y)

        self.attack_time = self.strength * 10
        self.half_attack_time = self.strength * 5
        print('ouch')

    def move(self):
        global curr_room
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.x > -3 and not self.left_stop:
            self.direction = 'left'
            self.x -= self.speed
            self.active_zone.move_ip(-self.speed, 0)
            self.phys_rect.move_ip(-self.speed, 0)
            if isinstance(self.attack_rect, pygame.Rect):
                self.attack_rect.move_ip(-self.speed, 0)

        if keys[pygame.K_d] and self.x < display_width - self.width - 5\
                and not self.right_stop:
            self.direction = 'right'
            self.x += self.speed
            self.active_zone.move_ip(self.speed, 0)
            self.phys_rect.move_ip(self.speed, 0)
            if isinstance(self.attack_rect, pygame.Rect):
                self.attack_rect.move_ip(self.speed, 0)

        if keys[pygame.K_w] and self.y > -3 and not self.up_stop:
            self.direction = 'up'
            self.y -= self.speed
            self.active_zone.move_ip(0, -self.speed)
            self.phys_rect.move_ip(0, -self.speed)
            if isinstance(self.attack_rect, pygame.Rect):
                self.attack_rect.move_ip(0, -self.speed)

        if keys[pygame.K_s] and self.y < display_height - self.height - 5 \
                and not self.down_stop:
            self.direction = 'down'
            self.y += self.speed
            self.active_zone.move_ip(0, self.speed)
            self.phys_rect.move_ip(0, self.speed)
            if isinstance(self.attack_rect, pygame.Rect):
                self.attack_rect.move_ip(0, self.speed)

        if self.phys_rect.colliderect(left_border):
            curr_room -= 1
        elif self.phys_rect.colliderect(right_border):
            curr_room += 1
        elif self.phys_rect.colliderect(upper_border):
            curr_room -= dung_length
        elif self.phys_rect.colliderect(lower_border):
            curr_room += dung_length

    def update(self):
        if self.attack_time:
            if self.attack_time == self.half_attack_time:
                self.attack_rect = None
            self.attack_time -= 1

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
        eye_colour = (0, 0, 0)
        if self.attack_rect:
            pygame.draw.rect(display, RED, self.attack_rect)
        self.visible_zone.blit(heretic_images[self.direction], (0, 0))
        display.blit(self.visible_zone, self.phys_rect)
    #  pygame.draw.rect(self.visible_zone, (0, 0, 0), (self.x - 15, self.y - 30, 110, 25))
    #    pygame.draw.rect(self.visible_zone, RED, (self.x - 10, self.y - 28,
    #       int(100.0 * float(self.health) / 100.0), 21))
