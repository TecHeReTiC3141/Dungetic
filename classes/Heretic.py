import scripts.constants_and_sources as c_a_s
from scripts.constants_and_sources import *
from classes.weapons import *
from scripts.Maths import get_rect_dist
import random


class Heretic:


    colliding = None

    def __init__(self, x, y, width, height, health, direction, inventory,
                 speed=5, strength=5, target=None, weapon=None, location=None, attack_time=0,
                 half_attack_time=0, backpack=None, size=1.):
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

        self.weapon = Fist()
        self.attack_rect = pygame.Rect(self.x - self.weapon.hit_range,
                                               self.y + self.height // 5,
                                          self.weapon.hit_range, self.height // 5 * 3)
        self.attack_surf = pygame.Surface((50, 50))
        self.attack_surf.set_colorkey(BLACK)
        self.collised_walls = dict.fromkeys(directions)
        self.speed_directions = dict.fromkeys(directions, 5)

        self.location = location
        self.attack_time = attack_time
        self.half_attack_time = half_attack_time
        self.backpack = backpack

        self.target = target
        self.size = size
        self.speed = speed

    def hit(self, entities: list):
        if self.attack_time <= 0:
            if self.direction == 'left':
                self.attack_rect = pygame.Rect(self.x - self.weapon.hit_range,
                                               self.y + self.height // 5,
                                          self.weapon.hit_range, self.height // 5 * 3)
            elif self.direction == 'right':
                self.attack_rect = pygame.Rect(self.phys_rect.right, self.y + self.height // 5,
                                          self.weapon.hit_range, self.height // 5 * 3)
            elif self.direction == 'up':
                self.attack_rect = pygame.Rect(self.x + self.width // 5, self.y - self.weapon.hit_range,
                                          self.width // 5 * 3, self.weapon.hit_range)
            elif self.direction == 'down':
                self.attack_rect = pygame.Rect(self.x + self.width // 5, self.y + self.height,
                                          self.width // 5 * 3, self.weapon.hit_range)
            for entity in entities:
                if entity.phys_rect.colliderect(self.attack_rect):
                    entity.health -= self.weapon.damage
                    dist_x, dist_y = get_rect_dist(entity.phys_rect, self.phys_rect)
                    entity.x += dist_x
                    entity.y += dist_y
                    entity.phys_rect.move_ip(dist_x, dist_y)
                    entity.active_zone.move_ip(dist_x, dist_y)

            self.attack_time = self.weapon.capability
            self.half_attack_time = self.weapon.capability // 2
        print(self.attack_time, 'ouch')

    def move(self):
        global c_a_s
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.x > -3:
            self.direction = 'left'
            l_speed = self.speed_directions['left']
            self.x -= l_speed
            self.active_zone.move_ip(-l_speed, 0)
            self.phys_rect.move_ip(-l_speed, 0)
            self.attack_rect.move_ip(-l_speed, 0)

        if keys[pygame.K_d] and self.x < display_width - self.width - 5:
            self.direction = 'right'
            r_speed = self.speed_directions['right']
            self.x += r_speed
            self.active_zone.move_ip(r_speed, 0)
            self.phys_rect.move_ip(r_speed, 0)
            self.attack_rect.move_ip(r_speed, 0)

        if keys[pygame.K_w] and self.y > -3:
            self.direction = 'up'
            u_speed = self.speed_directions['up']
            self.y -= u_speed
            self.active_zone.move_ip(0, -u_speed)
            self.phys_rect.move_ip(0, -u_speed)
            self.attack_rect.move_ip(0, -u_speed)

        if keys[pygame.K_s] and self.y < display_height - self.height - 5:
            self.direction = 'down'
            d_speed = self.speed_directions['down']
            self.y += d_speed
            self.active_zone.move_ip(0, d_speed)
            self.phys_rect.move_ip(0, d_speed)
            self.attack_rect.move_ip(0, d_speed)

        if self.phys_rect.colliderect(left_border):
            c_a_s.curr_room -= 1
            self.x = display_width - 100
            self.phys_rect.update(self.x, self.y, self.width, self.height)
            self.attack_rect.update(self.x - self.weapon.hit_range,
                                               self.y + self.height // 5,
                                          self.weapon.hit_range, self.height // 5 * 3)
            print(c_a_s.curr_room)
        elif self.phys_rect.colliderect(right_border):
            c_a_s.curr_room += 1
            self.x = 50
            self.phys_rect.update(self.x, self.y, self.width, self.height)
            self.attack_rect.update(self.phys_rect.right, self.y + self.height // 5,
                                          self.weapon.hit_range, self.height // 5 * 3)
            print(c_a_s.curr_room)
        elif self.phys_rect.colliderect(upper_border):
            c_a_s.curr_room -= dung_length
            self.y = display_height - 125
            self.phys_rect.update(self.x, self.y, self.width, self.height)
            self.attack_rect.update(self.x + self.width // 5, self.y - self.weapon.hit_range,
                                          self.width // 5 * 3, self.weapon.hit_range)
            print(c_a_s.curr_room)
        elif self.phys_rect.colliderect(lower_border):
            c_a_s.curr_room += dung_length
            self.y = 25
            self.phys_rect.update(self.x, self.y, self.width, self.height)
            self.attack_rect.update(self.x + self.width // 5, self.y + self.height,
                                          self.width // 5 * 3, self.weapon.hit_range)
            print(c_a_s.curr_room)


    def update(self):
        if self.attack_time:
            self.attack_time -= 1

    @staticmethod
    def tp(room):
        global c_a_s
        c_a_s.curr_room = room

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
        # if self.direction in self.weapon.sprite:
        #     if self.direction == 'left':
        #         display.blit(self.weapon, (self.phys_rect.left - 5, self.))
        if self.attack_rect:
            pygame.draw.rect(display, RED, self.attack_rect)
        self.visible_zone.blit(heretic_images[self.direction], (0, 0))

        display.blit(self.visible_zone, self.phys_rect)
        display.blit(self.attack_surf, self.attack_rect)
    #  pygame.draw.rect(self.visible_zone, (0, 0, 0), (self.x - 15, self.y - 30, 110, 25))
    #    pygame.draw.rect(self.visible_zone, RED, (self.x - 10, self.y - 28,
    #       int(100.0 * float(self.health) / 100.0), 21))
