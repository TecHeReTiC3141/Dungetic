from classes.loot import *
from classes.decors import *
from scripts.game_manager import GameManager


class Heretic:
    sprites = {i: pygame.image.load(f'../images/entities/heretic/heretic_sprite_{i}.png')
               for i in directions}

    def __init__(self, x, y, width, height, health, direction, manager: GameManager=None,
                 speed=6, target=None, weapon=Fist(), location=None, size=1.):
        self.x, self.y = x, y
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
        self.cur_rect = pygame.Rect(x, y + height // 4, width, int(height * .75))
        self.prev_rect = self.cur_rect.copy()
        self.active_zone = pygame.Rect(x - self.width // 10, y + self.height // 10,
                                       self.width * 1.2, int(self.height * .8))

        self.node = Node(self.cur_rect.centerx // grid_size,
                         self.cur_rect.centery // grid_size)

        self.weapon = weapon
        self.attack_rect = pygame.Rect(self.cur_rect.left - self.weapon.hit_range,
                                       self.cur_rect.top,
                                       self.weapon.hit_range, self.height // 5 * 3)
        self.attack_surf = pygame.Surface((50, 50))
        self.attack_surf.set_colorkey(BLACK)

        self.body_armor = None
        self.head_armor = None
        self.defense = 0.

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

        self.experience = 0
        self.level = 0
        self.exp_points = 0
        self.skills = {
            'speed': [0, 4],
            'damage': [0, 1],
            'resist': [0, 0.],
        }

        self.manager = manager

    def hit(self, entities: list['Heretic'] = None, conts: list = None) -> list:
        blood_list = []
        if self.attack_time <= 0:
            for entity in entities:
                if entity.friendly:
                    continue
                if entity.cur_rect.colliderect(self.attack_rect):
                    damage = randint(self.weapon.damage - 2, self.weapon.damage + 2) * \
                             self.skills['damage'][1]
                    entity.actual_health = max(entity.actual_health -
                                               damage, 0)
                    entity.regeneration_delay = -1
                    dist_x, dist_y = map(round, get_rects_dir(self.cur_rect, entity.cur_rect)
                                         * self.weapon.knockback)
                    if self.manager.blood:
                        blood_list.extend([Blood(randint(entity.cur_rect.left, entity.cur_rect.right),
                                                 randint(entity.cur_rect.top, entity.cur_rect.midleft[1]),
                                                 randint(10, 15), randint(10, 15), randint(50, 70),
                                                 type=choice(['down', 'up']), speed=5) for _ in
                                           range(self.weapon.damage // 4)])
                    if self.manager.show_damage:
                        blood_list.append(DamageInd(randint(entity.cur_rect.left, entity.cur_rect.right),
                                                    randint(entity.cur_rect.top, entity.cur_rect.midleft[1]),
                                                    damage, randint(50, 70), text_font))

                    entity.cur_rect.move_ip(dist_x, dist_y)
                    entity.active_zone.move_ip(dist_x, dist_y)
                    entity.attack_rect.move_ip(dist_x, dist_y)
                    if entity.actual_health <= 0:
                        entity.die()

                    self.weapon.hit_sound.play()
                    self.weapon.durab -= 1

            for obst in conts:
                if obst.cur_rect.colliderect(self.attack_rect):
                    obst.health -= self.weapon.damage
                    dist_x, dist_y = map(round, get_rects_dir(self.cur_rect, obst.cur_rect)
                                         * self.weapon.knockback // 2)

                    obst.cur_rect.move_ip(dist_x, dist_y)
                    obst.active_zone.move_ip(dist_x, dist_y)

                    if obst.health <= 0:
                        obst.get_broken()

            self.attack_time = self.weapon.capability
        return blood_list

    def shoot(self) -> Projectile:
        if isinstance(self.weapon, LongRange) and self.attack_time <= 0:
            if self.direction == 'left':
                vector = pygame.math.Vector2(-1, uniform(-.3, .3))
            elif self.direction == 'right':
                vector = pygame.math.Vector2(1, + uniform(-.3, .3))
            elif self.direction == 'up':
                vector = pygame.math.Vector2(uniform(-.3, .3), -1)
            else:
                vector = pygame.math.Vector2(uniform(-.3, .3), 1)

            self.attack_time = self.weapon.capability

            return self.weapon.shoot(*self.get_center_coord(False), vector)

    def get_center_coord(self, ind):
        return (self.cur_rect.centerx // grid_size, self.cur_rect.centery // grid_size) if ind \
            else (self.cur_rect.centerx, self.cur_rect.centery)

    def move(self):  # heretic's moving
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

    def update(self, tick: int, is_safe: bool = None):

        self.prev_rect = self.cur_rect.copy()
        if self.vector.length():
            norm_dir = self.vector.normalize() * self.skills['speed'][1]
            self.cur_rect.move_ip(round(norm_dir.x), round(norm_dir.y))
            self.attack_rect.move_ip(round(norm_dir.x), round(norm_dir.y))
        self.vector.x, self.vector.y = 0, 0
        self.active_zone.topleft = (self.cur_rect.left - self.width // 10,
                                    self.cur_rect.top + self.height // 10)
        if isinstance(self.weapon, Melee):
            if self.direction == 'left':
                self.attack_rect.update(self.cur_rect.left - self.weapon.hit_range - max(self.attack_time // 4, 0),
                                        self.cur_rect.top,
                                        self.weapon.hit_range, self.height // 5 * 3)

            elif self.direction == 'right':
                self.attack_rect.update(self.cur_rect.right + max(self.attack_time // 4, 0),
                                        self.cur_rect.top,
                                        self.weapon.hit_range, self.height // 5 * 3)
            elif self.direction == 'up':
                self.attack_rect.update(self.cur_rect.left + self.width // 5,
                                        self.cur_rect.top - self.weapon.hit_range,
                                        self.width // 5 * 3, self.weapon.hit_range)
            elif self.direction == 'down':
                self.attack_rect.update(self.cur_rect.left + self.width // 5,
                                        self.cur_rect.top + self.height,
                                        self.width // 5 * 3, self.weapon.hit_range)
        elif isinstance(self.weapon, LongRange):
            if self.direction == 'left':
                self.attack_rect.update(
                    self.cur_rect.left - self.weapon.sprite[self.direction].get_width() - max(self.attack_time // 4, 0),
                    self.cur_rect.top + self.height // 5,
                    self.weapon.sprite[self.direction].get_width(), self.height // 5 * 3)

            elif self.direction == 'right':
                self.attack_rect.update(self.cur_rect.right + max(self.attack_time // 4, 0),
                                        self.cur_rect.top + self.height // 5,
                                        self.weapon.sprite[self.direction].get_width(), self.height // 5 * 3)

        if self.weapon.durab <= 0:
            self.weapon = Fist()

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

        if isinstance(self.head_armor, Helmet) and self.head_armor.durab <= 0:
            self.head_armor = None

        if self.actual_health <= 0:
            self.die()

        if self.experience >= 20 * (self.level + 1):
            self.level += 1
            self.experience = 0
            self.exp_points += max(self.level // 2, 1)

    def regenerate(self):
        if self.regeneration_delay == 0:
            self.actual_health = min(self.actual_health + 2, 100)

    def die(self):
        pass

    def draw_object(self, display: pygame.Surface, x=None, y=None, in_game=True):
        if x is None and y is None:
            x, y = self.cur_rect.left, self.cur_rect.top - self.height // 4
        self.visible_zone.fill('yellow')

        self.visible_zone.blit(self.sprites[self.direction], (0, 0))
        display.blit(self.visible_zone, (x, y))
        if self.direction in self.weapon.sprite:
            if in_game:
                if self.direction == 'left':
                    self.weapon.draw_object(display, x=self.attack_rect.midtop[0],
                                            y=self.attack_rect.midleft[1],
                                            direct='left')
                elif self.direction == 'right':
                    self.weapon.draw_object(display, x=self.attack_rect.left,
                                            y=self.attack_rect.midleft[1], direct='right')
        # display.blit(self.attack_surf, self.attack_rect)
        if self.attack_time > 0:
            pygame.draw.rect(display, (0, 0, 0),
                             (x + self.cur_rect.width // 2 - self.weapon.capability // 2,
                              y - 45, self.weapon.capability, 14), border_radius=8)
            pygame.draw.rect(display, BLUE,
                             (x + self.cur_rect.width // 2 - self.weapon.capability // 2 + 2,
                              y - 44, self.attack_time - 4, 12))
        pygame.draw.rect(display, (0, 0, 0), (x - 15, y - 30, 110, 25), border_radius=8)

        if isinstance(self.head_armor, Helmet):
            self.head_armor.draw_object(display, self.cur_rect.left,
                                        self.cur_rect.top, self.direction)

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

    def set_player(self, player):
        self.inventory = player.inventory
        self.weapon = player.weapon
        self.body_armor = player.body_armor
        self.head_armor = player.head_armor
        self.actual_money = player.actual_money
        self.experience = player.experience
        self.level = player.level
        self.exp_points = player.exp_points
        self.skills = player.skills

    def __getstate__(self):
        state = self.__dict__.copy()

        state.pop('attack_surf')
        state.pop('visible_zone')
        state.pop('manager')
        pprint(state)
        return state

    def __setstate__(self, state):
        state['attack_surf'] = pygame.Surface((50, 50))
        state['visible_zone'] = pygame.Surface((state['width'], state['height']))
        self.__dict__.update(state)


class PlayerManager(GameManager):

    def __init__(self, player: Heretic):
        self.player = player
