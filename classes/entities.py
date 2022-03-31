from classes.Heretic import *


class NPC(Heretic):
    stop = False
    delay = random.randint(250, 450)

    def __init__(self, x, y, width, height, health, direction, speed,
                 target=None, weapon=Fist(), loot=None, location=None, size=1.):
        super().__init__(x, y, width, height, health, direction,
                         speed, target, weapon, location, size)
        self.path = deque()
        self.loot = [] if loot is None else loot

    def draw_object(self, display: pygame.Surface, x=None, y=None):
        super().draw_object(display)

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

    def die(self) -> list:
        # drop loot or smth like that
        self.dead = True
        for loot in self.loot:
            loot.rect.topleft = self.phys_rect.topleft
            loot.picked = False
        print([i.picked for i in self.loot])
        return self.loot

    @staticmethod
    def produce_NPC(n, loot: list=None):
        return [NPC(random.randint(300, 800), random.randint(200, 600), 75, 100, 100,
                    random.choice(directions), speed=random.randint(3, 4), loot=loot) for i in range(n)]


class Hostile(NPC):

    def __init__(self, x, y, width, height, health, direction, speed,
                 target=None, weapon=Fist(), location=None, loot=None, size=1.):
        super().__init__(x, y, width, height, health, direction,
                         speed, target, weapon, loot, location, size)
        self.target = []
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
            self.active_zone.move_ip(round(self.dirs.x),
                                     round(self.dirs.y))
            if self.targetpoint.collidepoint(self.phys_rect.center):
                self.nextpoint()
            self.hit(entities=self.target)

    def nextpoint(self):
        self.path.popleft()
        if not self.path:
            self.targetpoint = pygame.Rect(self.phys_rect.center, (6, 6))
        else:
            self.targetpoint = pygame.Rect((self.path[0][0] + 3, self.path[0][1] + 3), (6, 6))

    def hit(self, entities: list[Heretic] = None, conts: list = None):
        if self.attack_time <= 0:
            for target in entities:
                if self.active_zone.colliderect(target.active_zone):
                    self.attack_time = self.weapon.capability * 2
                    target.actual_health = max(target.actual_health - self.weapon.damage, 0)
                    target.regeneration_delay = self.weapon.damage * 20
                    dist_x, dist_y = map(round, get_rects_dir(self.phys_rect, target.phys_rect) \
                                         * self.weapon.damage * 10)
                    target.x += dist_x
                    target.y += dist_y
                    target.phys_rect.move_ip(dist_x, dist_y)
                    target.active_zone.move_ip(dist_x, dist_y)
                    if target.actual_health <= 0:
                        target.die()

    def draw_object(self, display: pygame.Surface):
        super().draw_object(display)

    @staticmethod
    def produce_Hostiles(n, loot: list=None):
        return [Hostile(random.randint(300, 800), random.randint(200, 600), 75, 100, 15,
                        random.choice(directions), speed=random.randint(3, 4), loot=loot) for i in range(n)]
