from classes.Heretic import *


class NPC(Heretic):
    stop = False
    delay = random.randint(250, 450)

    def __init__(self, x, y, width, height, health, direction, inventory, speed, behavior_type='passive',
                 target=None, weapon=None, location=None, attack_time=0, half_attack_time=0, backpack=None, size=1.):
        super().__init__(x, y, width, height, health, direction, inventory,
                         speed, target, weapon, location, attack_time, half_attack_time, backpack, size)
        self.path = deque()
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
        self.visible_zone.blit(heretic_images[self.direction], (0, 0))
        pygame.draw.rect(display, (0, 0, 0), (self.x - 15, self.y - 30, 110, 25), border_radius=8)
        pygame.draw.rect(display, pygame.Color('Yellow'), (self.x - 10, self.y - 28,
                                                           int(100.0 * float(self.health) / 100.0), 21),
                         border_radius=8)
        pygame.draw.rect(display, RED, (self.x - 10, self.y - 28,
                                        int(100.0 * float(self.actual_health) / 100.0), 21), border_radius=8)
        display.blit(self.visible_zone, self.phys_rect)

    def walk(self):
        if self.direction == 'left' and self.collised_walls['left'] is None:
            self.direction = 'left'
            l_speed = self.speed_directions['left']
            self.x -= l_speed
            self.active_zone.move_ip(-l_speed, 0)
            self.phys_rect.move_ip(-l_speed, 0)
            self.attack_rect.move_ip(-l_speed, 0)

        if self.direction == 'right' and self.x < display_width - self.width - 5 and \
                self.collised_walls['right'] is None:
            self.direction = 'right'
            r_speed = self.speed_directions['right']
            self.x += r_speed
            self.active_zone.move_ip(r_speed, 0)
            self.phys_rect.move_ip(r_speed, 0)
            self.attack_rect.move_ip(r_speed, 0)

        if self.direction == 'up' and self.y > -3 \
                and self.collised_walls['up'] is None:
            self.direction = 'up'
            u_speed = self.speed_directions['up']
            self.y -= u_speed
            self.active_zone.move_ip(0, -u_speed)
            self.phys_rect.move_ip(0, -u_speed)
            self.attack_rect.move_ip(0, -u_speed)

        if self.direction == 'down' and self.y < display_height - self.height - 5 and \
                self.collised_walls['down'] is None:
            self.direction = 'down'
            d_speed = self.speed_directions['down']
            self.y += d_speed
            self.active_zone.move_ip(0, d_speed)
            self.phys_rect.move_ip(0, d_speed)
            self.attack_rect.move_ip(0, d_speed)

        self.node = Node(self.phys_rect.centerx // grid_size,
                         self.phys_rect.centery // grid_size)

    def passive_exist(self):

        self.walk()
        if not self.delay:
            next_direction = random.choice(directions + [None, None])
            if next_direction is not None:
                self.direction = next_direction
                self.stop = False
            else:
                self.stop = True
            self.delay = random.randint(250, 450)
        if (self.x <= 10 and self.direction == 'left') or (self.x >= 920 and self.direction == 'right') \
                or (self.y <= 0 and self.direction == 'up') or (self.y >= 685 and self.direction == 'down'):
            self.direction = opposites[self.direction]
        self.delay -= 1

    def update(self, tick: int):
        if self.health > self.actual_health:
            self.health -= .1

    def die(self):
        # drop loot or smth like that
        self.dead = True

    @staticmethod
    def produce_NPC(n):
        return [NPC(random.randint(300, 800), random.randint(200, 600), 75, 100, 100,
                    random.choice(directions), [], speed=random.randint(3, 4)) for i in range(n)]


class Hostile(NPC):

    def __init__(self, x, y, width, height, health, direction, inventory, speed, behavior_type='passive',
                 target=None, weapon=None, location=None, attack_time=0, half_attack_time=0, backpack=None, size=1.):
        super().__init__(x, y, width, height, health, direction, inventory,
                         speed, target, weapon, location, attack_time, half_attack_time, backpack, size)

        self.targetpoint = pygame.Rect(self.phys_rect.center, (5, 5))
        self.cur_point = pygame.math.Vector2(self.get_center_coord(False))
        self.dirs = pygame.math.Vector2([0, 0])

    def hostile_exist(self):
        if self.path:
            next_point = pygame.math.Vector2(self.targetpoint.center)
            self.cur_point = pygame.math.Vector2(self.get_center_coord(False))
            if (next_point - self.cur_point).length() != 0:
                self.dirs = (next_point - self.cur_point).normalize() * self.speed

            if self.dirs.x > 0:
                self.direction = 'right'
            elif self.dirs.x < 0:
                self.direction = 'left'
            if self.dirs.y < 0:
                self.direction = 'up'
            elif self.dirs.y > .2:
                self.direction = 'down'
            self.x += round(self.dirs.x)
            self.y += round(self.dirs.y)
            self.phys_rect.move_ip(round(self.dirs.x),
                                   round(self.dirs.y))
            if self.targetpoint.collidepoint(self.phys_rect.center):
                self.nextpoint()

    def nextpoint(self):
        self.path.popleft()
        if not self.path:
            self.targetpoint = pygame.Rect(self.phys_rect.center, (6, 6))
        else:
            self.targetpoint = pygame.Rect((self.path[0][0] + 3, self.path[0][1] + 3), (6, 6))

    @staticmethod
    def produce_Hostiles(n):
        return [Hostile(random.randint(300, 800), random.randint(200, 600), 75, 100, 100,
                    random.choice(directions), [], speed=random.randint(3, 4)) for i in range(n)]


