from scripts.constants_and_sources import *
import scripts.constants_and_sources as c_a_s
from classes.loot import *


class Heretic:

    def __init__(self, x, y, width, height, health, direction,
                 speed=5, target=None, weapon=Fist(), location=None, size=1.):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.health = health
        self.actual_health = health
        self.regeneration_delay = -1

        self.dead = False
        self.direction = direction

        self.inventory = []
        self.max_capacity = 20

        self.light_zone = []
        self.visible_zone = pygame.Surface((self.width, self.height))
        self.phys_rect = pygame.Rect(x, y, self.width, int(self.height))
        self.active_zone = pygame.Rect(x - self.width // 10, y + self.height // 10,
                                       self.width * 1.2, int(self.height * .8))

        self.node = Node(self.phys_rect.centerx // grid_size,
                         self.phys_rect.centery // grid_size)

        self.weapon = weapon
        self.attack_rect = pygame.Rect(self.x - self.weapon.hit_range,
                                       self.y + self.height // 5,
                                       self.weapon.hit_range, self.height // 5 * 3)
        self.attack_surf = pygame.Surface((50, 50))
        self.attack_surf.set_colorkey(BLACK)
        self.collised_walls = dict.fromkeys(directions)
        self.speed_directions = dict.fromkeys(directions, 5)

        self.location = location
        self.attack_time = 0
        self.half_attack_time = 0

        self.target = target
        self.size = size
        self.speed = speed

        self.money = 0
        self.actual_money = 0

    def hit(self, entities: list = None, conts: list = None):
        if self.attack_time <= 0:
            for entity in entities:
                if entity.phys_rect.colliderect(self.attack_rect):
                    entity.actual_health = max(entity.actual_health -
                                               self.weapon.damage, 0)
                    entity.regeneration_delay = -1
                    dist_x, dist_y = map(round, get_rects_dir(self.phys_rect, entity.phys_rect) \
                                         * self.weapon.knockback)
                    entity.x += dist_x
                    entity.y += dist_y
                    entity.phys_rect.move_ip(dist_x, dist_y)
                    entity.active_zone.move_ip(dist_x, dist_y)
                    if entity.actual_health <= 0:
                        entity.die()
                    self.weapon.hit_sound.play()

            for obst in conts:
                if obst.phys_rect.colliderect(self.attack_rect):
                    obst.health -= self.weapon.damage
                    dist_x, dist_y = map(round, get_rects_dir(self.phys_rect, obst.phys_rect) \
                                         * self.weapon.knockback // 2)
                    obst.x += dist_x
                    obst.y += dist_y
                    obst.phys_rect.move_ip(dist_x, dist_y)
                    obst.active_zone.move_ip(dist_x, dist_y)
                    print(obst.health)
                    if obst.health <= 0:
                        obst.get_broken()

            self.attack_time = self.weapon.capability

    def get_center_coord(self, ind):
        return (self.phys_rect.centerx // grid_size, self.phys_rect.centery // grid_size) if ind \
            else (self.phys_rect.centerx, self.phys_rect.centery)

    def move(self):  # heretic's moving
        global c_a_s
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.x > -3:
            self.direction = 'left'
            l_speed = self.speed_directions['left']
            self.x -= l_speed
            self.phys_rect.move_ip(-l_speed, 0)
            self.attack_rect.move_ip(-l_speed, 0)

        if keys[pygame.K_d]:
            self.direction = 'right'
            r_speed = self.speed_directions['right']
            self.x += r_speed
            self.phys_rect.move_ip(r_speed, 0)
            self.attack_rect.move_ip(r_speed, 0)

        if keys[pygame.K_w]:
            self.direction = 'up'
            u_speed = self.speed_directions['up']
            self.y -= u_speed
            self.phys_rect.move_ip(0, -u_speed)
            self.attack_rect.move_ip(0, -u_speed)
            self.attack_rect.update(self.x + self.width // 5, self.y - self.weapon.hit_range,
                                    self.width // 5 * 3, self.weapon.hit_range)

        if keys[pygame.K_s]:
            self.direction = 'down'
            d_speed = self.speed_directions['down']
            self.y += d_speed
            self.phys_rect.move_ip(0, d_speed)
            self.attack_rect.move_ip(0, d_speed)
            self.attack_rect.update(self.x + self.width // 5, self.y + self.height,
                                    self.width // 5 * 3, self.weapon.hit_range)

        if self.phys_rect.colliderect(left_border):
            c_a_s.curr_room -= 1
            self.x = display_width - 100
            self.phys_rect.topleft = (self.x, self.y)

        elif self.phys_rect.colliderect(right_border):
            c_a_s.curr_room += 1
            self.x = 50
            self.phys_rect.topleft = (self.x, self.y)

        elif self.phys_rect.colliderect(upper_border):
            c_a_s.curr_room -= dung_length
            self.y = display_height - 125
            self.phys_rect.topleft = (self.x, self.y)

        elif self.phys_rect.colliderect(lower_border):
            c_a_s.curr_room += dung_length
            self.y = 25
            self.phys_rect.topleft = (self.x, self.y)

    def update(self, tick: int):
        self.active_zone.topleft = (self.phys_rect.left - self.width // 10,
                                    self.phys_rect.top + self.height // 10)
        if self.direction == 'left':
            self.attack_rect.update(self.x - self.weapon.hit_range,
                                    self.y + self.height // 5,
                                    self.weapon.hit_range, self.height // 5 * 3)
        elif self.direction == 'right':
            self.attack_rect.update(self.phys_rect.right, self.y + self.height // 5,
                                    self.weapon.hit_range, self.height // 5 * 3)

        if not tick % 10:
            self.regenerate()
        if self.health > self.actual_health:
            self.health -= .1
        if self.regeneration_delay > 0:
            self.regeneration_delay -= 1

        if self.attack_time > 0:
            self.attack_time -= 1

        if self.money != self.actual_money and not tick % 6:
            self.money = self.money + 1 if self.money < self.actual_money else self.money - 1

    def regenerate(self):
        if self.regeneration_delay == 0:
            self.actual_health = min(self.actual_health + 2, 100)

    @staticmethod
    def tp(room):
        global c_a_s
        c_a_s.curr_room = room

    def die(self):
        pass

    def draw_object(self, display: pygame.Surface, x=None, y=None):
        if x is None and y is None:
            x, y = self.phys_rect.topleft
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
        # if self.direction in self.weapon.sprite:
        #     if self.direction == 'left':
        #         display.blit(self.weapon, (self.phys_rect.left - 5, self.))
        # pygame.draw.rect(display, RED, self.attack_rect)
        self.visible_zone.blit(heretic_images[self.direction], (0, 0))
        display.blit(self.visible_zone, (x, y))
        if self.direction in self.weapon.sprite:
            if self.direction == 'left':
                self.weapon.draw_object(display, x=self.attack_rect.midtop[0], y=self.attack_rect.midleft[1], dir='left')
            elif self.direction == 'right':
                self.weapon.draw_object(display, x=self.attack_rect.left, y=self.attack_rect.midleft[1], dir='right')

        # display.blit(self.attack_surf, self.attack_rect)
        if self.attack_time > 0:

            pygame.draw.rect(display, (0, 0, 0),
                             (x + self.phys_rect.width // 2 - self.weapon.capability // 2,
                              y - 45, self.weapon.capability, 14), border_radius=8)
            pygame.draw.rect(display, BLUE,
                             (x + self.phys_rect.width // 2 - self.weapon.capability // 2 + 2,
                              y - 44, self.attack_time - 4, 12))
        pygame.draw.rect(display, (0, 0, 0), (x - 15, y - 30, 110, 25), border_radius=8)
        pygame.draw.rect(display, pygame.Color('Yellow'), (x - 10, y - 28,
                                                           int(100.0 * float(self.health) / 100.0), 21),
                         border_radius=8)
        pygame.draw.rect(display, RED, (x - 10, y - 28,
                                        int(100.0 * float(self.actual_health) / 100.0), 21), border_radius=8)

