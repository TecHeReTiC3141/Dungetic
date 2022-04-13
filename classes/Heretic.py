from scripts.constants_and_sources import *
import scripts.constants_and_sources as c_a_s
from classes.loot import *
from classes.decors import *



class Heretic:
    # TODO try to transform entities into pygame.sprites
    def __init__(self, x, y, width, height, health, direction,
                 speed=6, target=None, weapon=Fist(), location=None, size=1.):
        self.width = width
        self.height = height

        self.health = health
        self.actual_health = health
        self.regeneration_delay = -1

        self.dead = False
        self.direction = direction
        self.vector = pygame.math.Vector2([0, 0])

        self.inventory = []
        self.max_capacity = 20

        self.light_zone = []
        self.visible_zone = pygame.Surface((self.width, self.height))
        self.cur_rect = pygame.Rect(x, y, self.width, int(self.height))
        self.prev_rect = self.cur_rect.copy()
        self.active_zone = pygame.Rect(x - self.width // 10, y + self.height // 10,
                                       self.width * 1.2, int(self.height * .8))

        self.node = Node(self.cur_rect.centerx // grid_size,
                         self.cur_rect.centery // grid_size)

        self.weapon = weapon
        self.attack_rect = pygame.Rect(self.cur_rect.left - self.weapon.hit_range,
                                       self.cur_rect.top + self.height // 5,
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

    def hit(self, entities: list = None, conts: list = None) -> list:
        blood_list = []
        if self.attack_time <= 0:
            for entity in entities:
                if entity.cur_rect.colliderect(self.attack_rect):
                    entity.actual_health = max(entity.actual_health -
                                               self.weapon.damage, 0)
                    entity.regeneration_delay = -1
                    dist_x, dist_y = map(round, get_rects_dir(self.cur_rect, entity.cur_rect)
                                         * self.weapon.knockback)
                    blood_list.extend([Blood(random.randint(entity.cur_rect.left,entity.cur_rect.right),
                                             random.randint(entity.cur_rect.top,entity.cur_rect.midleft[1]),
                                             random.randint(10, 15), random.randint(10, 15), random.randint(70, 90),
                                             type=random.choice(['down', 'up']), speed=5) for i in range(self.weapon.damage // 4)])

                    entity.cur_rect.move_ip(dist_x, dist_y)
                    entity.active_zone.move_ip(dist_x, dist_y)
                    entity.attack_rect.move_ip(dist_x, dist_y)
                    if entity.actual_health <= 0:
                        entity.die()
                    self.weapon.hit_sound.play()

            for obst in conts:
                if obst.phys_rect.colliderect(self.attack_rect):
                    obst.health -= self.weapon.damage
                    dist_x, dist_y = map(round, get_rects_dir(self.cur_rect, obst.phys_rect)
                                         * self.weapon.knockback // 2)

                    obst.phys_rect.move_ip(dist_x, dist_y)
                    obst.active_zone.move_ip(dist_x, dist_y)
                    print(obst.health)
                    if obst.health <= 0:
                        obst.get_broken()

            self.attack_time = self.weapon.capability
        return blood_list

    def get_center_coord(self, ind):
        return (self.cur_rect.centerx // grid_size, self.cur_rect.centery // grid_size) if ind \
            else (self.cur_rect.centerx, self.cur_rect.centery)

    def move(self):  # heretic's moving
        global c_a_s
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.direction = 'left'
            self.vector.x = -1

        if keys[pygame.K_d]:
            self.direction = 'right'
            self.vector.x = 1

        if keys[pygame.K_w]:
            self.direction = 'up'
            self.vector.y = -1

        if keys[pygame.K_s]:
            self.direction = 'down'
            self.vector.y = 1

        if self.cur_rect.colliderect(left_border):
            c_a_s.curr_room -= 1
            self.cur_rect.left = display_width - 100
            self.cur_rect.topleft = (self.cur_rect.left, self.cur_rect.top)

        elif self.cur_rect.colliderect(right_border):
            c_a_s.curr_room += 1
            self.cur_rect.left = 50
            self.cur_rect.topleft = (self.cur_rect.left, self.cur_rect.top)

        elif self.cur_rect.colliderect(upper_border):
            c_a_s.curr_room -= dung_length
            self.cur_rect.top = display_height - 125
            self.cur_rect.topleft = (self.cur_rect.left, self.cur_rect.top)

        elif self.cur_rect.colliderect(lower_border):
            c_a_s.curr_room += dung_length
            self.cur_rect.top = 25
            self.cur_rect.topleft = (self.cur_rect.left, self.cur_rect.top)

    def update(self, tick: int, is_safe: bool = None):

        self.prev_rect = self.cur_rect.copy()
        if self.vector.length():
            norm_dir = self.vector.normalize() * self.speed
            self.cur_rect.move_ip(round(norm_dir.x), round(norm_dir.y))
            self.attack_rect.move_ip(round(norm_dir.x), round(norm_dir.y))
        self.vector.x, self.vector.y = 0, 0
        self.active_zone.topleft = (self.cur_rect.left - self.width // 10,
                                    self.cur_rect.top + self.height // 10)
        if self.direction == 'left':
            self.attack_rect.update(self.cur_rect.left - self.weapon.hit_range,
                                    self.cur_rect.top + self.height // 5,
                                    self.weapon.hit_range, self.height // 5 * 3)

        elif self.direction == 'right':
            self.attack_rect.update(self.cur_rect.right,
                                    self.cur_rect.top + self.height // 5,
                                    self.weapon.hit_range, self.height // 5 * 3)
        elif self.direction == 'up':
            self.attack_rect.update(self.cur_rect.left + self.width // 5,
                                    self.cur_rect.top - self.weapon.hit_range,
                                    self.width // 5 * 3, self.weapon.hit_range)
        elif self.direction == 'down':
            self.attack_rect.update(self.cur_rect.left + self.width // 5,
                                    self.cur_rect.top + self.height,
                                    self.width // 5 * 3, self.weapon.hit_range)

        if not tick % 10 and is_safe:
            self.regenerate()

        if self.health > self.actual_health:
            self.health -= .2

        elif self.health < self.actual_health:
            self.health += .2

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
            x, y = self.cur_rect.topleft
        self.visible_zone.fill((0, 0, 0))
        # if self.backpack and self.directions == 'right':
        #     self.backpack.draw_on_self(self.cur_rect.left + 25, self.cur_rect.top + 45)
        # elif self.backpack and self.directions == 'up':
        #     self.backpack.draw_on_self(self.cur_rect.left - 5, self.cur_rect.top + 45)
        # if self.weapon != 'none' and self.directions == 'right':
        #     self.weapon.draw_object(self.cur_rect.left + 65 - ((self.half_attack_time -
        #                                                   self.attack_time) // 2 if self.attack_time > self.half_attack_time else 0),
        #                                self.cur_rect.top + 30)
        # elif self.weapon != 'none' and self.directions == 'up':
        #     self.weapon.draw_object(self.cur_rect.left - 15, self.cur_rect.top + 30 + ((self.half_attack_time -
        #                                                                   self.attack_time) // 2 if self.attack_time > self.half_attack_time else 0))
        # if self.direction in self.weapon.sprite:
        #     if self.direction == 'left':
        #         display.blit(self.weapon, (self.cur_rect.left - 5, self.))
        # pygame.draw.rect(display, RED, self.attack_rect)
        self.visible_zone.blit(heretic_images[self.direction], (0, 0))
        display.blit(self.visible_zone, (x, y))
        if self.direction in self.weapon.sprite:
            if self.direction == 'left':
                self.weapon.draw_object(display, x=self.attack_rect.midtop[0], y=self.attack_rect.midleft[1],
                                        direct='left')
            elif self.direction == 'right':
                self.weapon.draw_object(display, x=self.attack_rect.left, y=self.attack_rect.midleft[1], direct='right')

        # display.blit(self.attack_surf, self.attack_rect)
        if self.attack_time > 0:
            pygame.draw.rect(display, (0, 0, 0),
                             (x + self.cur_rect.width // 2 - self.weapon.capability // 2,
                              y - 45, self.weapon.capability, 14), border_radius=8)
            pygame.draw.rect(display, BLUE,
                             (x + self.cur_rect.width // 2 - self.weapon.capability // 2 + 2,
                              y - 44, self.attack_time - 4, 12))
        pygame.draw.rect(display, (0, 0, 0), (x - 15, y - 30, 110, 25), border_radius=8)
        if self.health >= self.actual_health:
            pygame.draw.rect(display, pygame.Color('Yellow'), (x - 10, y - 28,
                                                               int(100.0 * float(self.health) / 100.0), 21),
                             border_radius=8)
            pygame.draw.rect(display, RED, (x - 10, y - 28,
                                            int(100.0 * float(self.actual_health) / 100.0), 21), border_radius=8)
        else:
            pygame.draw.rect(display, pygame.Color('Green'), (x - 10, y - 28,
                                                               int(100.0 * float(self.actual_health) / 100.0), 21),
                             border_radius=8)
            pygame.draw.rect(display, RED, (x - 10, y - 28,
                                            int(100.0 * float(self.health) / 100.0), 21), border_radius=8)
