from classes.Heretic import *


class NPC(Heretic):
    stop = False
    delay = randint(250, 450)

    def __init__(self, x, y, width, height, health, direction, speed,
                 target=None, weapon=Fist(), loot=None, location=None, size=1.):
        super().__init__(x, y, width, height, health, direction, None,
                         speed, target, weapon, location, size)
        self.path = deque()
        self.loot = [] if loot is None else loot

    def draw_object(self, display: pygame.Surface, x=None, y=None):
        super().draw_object(display)

    def walk(self):
        if self.direction == 'left' and self.collised_walls['left'] is None:
            self.direction = 'left'
            l_speed = self.speed_directions['left']
            self.active_zone.move_ip(-l_speed, 0)
            self.cur_rect.move_ip(-l_speed, 0)
            self.attack_rect.move_ip(-l_speed, 0)

        if self.direction == 'right' and self.cur_rect.left < display_width - self.width - 5 and \
                self.collised_walls['right'] is None:
            self.direction = 'right'
            r_speed = self.speed_directions['right']
            self.active_zone.move_ip(r_speed, 0)
            self.cur_rect.move_ip(r_speed, 0)
            self.attack_rect.move_ip(r_speed, 0)

        if self.direction == 'up' and self.cur_rect.top > -3 \
                and self.collised_walls['up'] is None:
            self.direction = 'up'
            u_speed = self.speed_directions['up']
            self.active_zone.move_ip(0, -u_speed)
            self.cur_rect.move_ip(0, -u_speed)
            self.attack_rect.move_ip(0, -u_speed)

        if self.direction == 'down' and self.cur_rect.top < display_height - self.height - 5 and \
                self.collised_walls['down'] is None:
            self.direction = 'down'
            d_speed = self.speed_directions['down']
            self.active_zone.move_ip(0, d_speed)
            self.cur_rect.move_ip(0, d_speed)
            self.attack_rect.move_ip(0, d_speed)

        self.node = Node(self.cur_rect.centerx // grid_size,
                         self.cur_rect.centery // grid_size)

    def passive_exist(self):

        self.walk()
        if not self.delay:
            next_direction = choice(directions + [None, None])
            if next_direction is not None:
                self.direction = next_direction
                self.stop = False
            else:
                self.stop = True
            self.delay = randint(150, 300)
        if (self.cur_rect.left <= 10 and self.direction == 'left') or (
                self.cur_rect.left >= 920 and self.direction == 'right') \
                or (self.cur_rect.top <= 0 and self.direction == 'up') or (
                self.cur_rect.top >= 685 and self.direction == 'down'):
            self.direction = opposites[self.direction]
        self.delay -= 1

    def die(self) -> list:
        # drop loot or smth like that
        self.dead = True
        for loot in self.loot:
            loot.rect.topleft = self.cur_rect.topleft
            loot.picked = False

        return self.loot

    def exist(self):
        self.passive_exist()

    @staticmethod
    def produce_NPC(n, nodes: list[list], room_width, room_height, loot: list=None,) -> list[Heretic]:
        entities = []
        for _ in range(n):
            while True:
                x, y = randint(200, room_width - 200), randint(200, room_height - 200)
                x_n, y_n = (x + 38 // 2) // grid_size, (y + 50) // grid_size
                if nodes[y_n][x_n].status:
                    entities.append(NPC(x, y, 75, 100, 100,
                    choice(directions), speed=randint(3, 4), loot=loot))
                    break
        return entities



class Hostile(NPC):
    sprites = {i: pygame.image.load(f'../images/entities/goblins/goblin_sprite_{i}.png')
               for i in directions}

    def __init__(self, x, y, width, height, health, direction, speed,
                 target=None, weapon=Fist(), location=None, loot=None, size=1.):
        super().__init__(x, y, width, height, health, direction,
                         speed, target, weapon, loot, location, size)
        self.state = 'neutral'
        self.target = []
        self.targetpoint = pygame.Rect(self.cur_rect.center, (5, 5))
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

            self.cur_rect.move_ip(round(self.dirs.x),
                                  round(self.dirs.y))
            self.active_zone.move_ip(round(self.dirs.x),
                                     round(self.dirs.y))
            self.attack_rect.move_ip(round(self.dirs.x),
                                     round(self.dirs.y))
            if self.targetpoint.collidepoint(self.cur_rect.center):
                self.nextpoint()
            blood_list = self.hit(entities=self.target)
            return blood_list

    def exist(self):
        if self.state == 'neutral':
            self.passive_exist()
        else:
            self.hostile_exist()

        if len(self.path) > randint(15, 20):
            self.state = 'neutral'
        else:
            self.state = 'hostile'

    def nextpoint(self):
        self.path.popleft()
        if not self.path:
            self.targetpoint = pygame.Rect(self.cur_rect.center, (6, 6))
        else:
            self.targetpoint = pygame.Rect((self.path[0][0] + 3, self.path[0][1] + 3), (6, 6))

    def hit(self, entities: list[Heretic] = None, conts: list = None) -> list:
        blood_list = []
        if self.attack_time <= 0:
            for target in entities:
                if self.active_zone.colliderect(target.active_zone):
                    self.attack_time = self.weapon.capability * 2

                    damage = randint(self.weapon.damage - 2, self.weapon.damage + 2)
                    if isinstance(target.head_armor, Helmet):
                        damage *= 1 - target.head_armor.persist - target.skills['resist'][1]

                    if target.manager.show_damage:
                        blood_list.append(DamageInd(randint(target.cur_rect.left, target.cur_rect.right),
                                                    randint(target.cur_rect.top, target.cur_rect.midleft[1]),
                                                    damage, randint(50, 70), text_font))

                    if target.manager.blood:
                        blood_list.extend([Blood(randint(target.cur_rect.left, target.cur_rect.right),
                                             randint(target.cur_rect.top, target.cur_rect.midleft[1]),
                                             randint(10, 15), randint(10, 15), randint(50, 70),
                                             type=choice(['down', 'up']), speed=5) for i in
                                       range(self.weapon.damage // 4)])

                    target.actual_health = max(target.actual_health - round(damage), 0)
                    target.regeneration_delay = self.weapon.damage * 20
                    dist_x, dist_y = map(round, get_rects_dir(self.cur_rect, target.cur_rect)
                                         * self.weapon.damage * 10)
                    target.cur_rect.move_ip(dist_x, dist_y)
                    target.active_zone.move_ip(dist_x, dist_y)

                    if isinstance(target.head_armor, Helmet):
                        target.head_armor.durab -= self.weapon.damage

                    if target.actual_health <= 0:
                        target.die()

                    self.weapon.hit_sound.play()
                    self.weapon.durab -= 1
                    if self.weapon.durab <= 0:
                        self.weapon = Fist()

        return blood_list

    def draw_object(self, display: pygame.Surface, x=0, y=0):
        super().draw_object(display)

    @staticmethod
    def produce_Hostiles(n, nodes: list[list], room_width, room_height, loot: list = None,):
        entities = []
        for _ in range(n):
            while True:
                x, y = randint(200, room_width - 200), randint(200, room_height - 200)
                x_n, y_n = (x + 38 // 2) // grid_size, (y + 50) // grid_size
                if nodes[y_n][x_n].status:
                    entities.append(Hostile(x, y, 75, 100, 100,
                                        choice(directions), speed=randint(3, 4), loot=loot))
                    break
        return entities
