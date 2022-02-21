import pygame
import random

# from My_classes.dungetic_classes import Drop, Log, Stone, Coal, Weapon, DroppedBerry, Meat, Stick, Juice, inventory_font, active_font, title_font
from classes.Heretic import Heretic

pygame.init()
dung_length, dung_width = map(int, input('Введите длину и ширину подземелья: ').split())
display_width, display_height = 1440, 750
print(*[''.join([str(i).rjust(3) for i in list(range(1 + dung_length * i, dung_length * (i + 1) + 1))]) for i in
        range(dung_width)], sep='\n')
pygame.mouse.set_visible(False)
'''
TODO:
Изменить систему столкновений со стенами. 550 - 600

'''
display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Dungetic')
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 200)
clock = pygame.time.Clock()
bullets_list = []
tick = 0
bloor = pygame.Surface((display_width, display_height))
bloor.set_alpha(15)
map_image = pygame.image.load('./images/old_map2.jpg').convert_alpha()
cursor_for_battle = pygame.image.load('./images/sword.png')
stone_floor = pygame.image.load('./images/stone_floor.jpg')
cursor_for_battle = pygame.transform.scale(cursor_for_battle,
                                           (cursor_for_battle.get_width() // 5, cursor_for_battle.get_height() // 5))
map_image = pygame.transform.scale(map_image, (
    int(map_image.get_width() / 1.5), int(map_image.get_height() * 0.6))).convert_alpha()
stone_floor = pygame.transform.scale(stone_floor, (display_width, display_height))
text_font = pygame.font.Font(None, 40)
active_font = pygame.font.Font(None, 50)
inventory_font = pygame.font.SysFont('Cambria', 75)

directions = ['up', 'down', 'left', 'right']
opposites = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}




class NPC(Heretic):
    left_stop = False
    right_stop = False
    up_stop = False
    down_stop = False
    stop = False
    delay = random.randint(250, 450)

    def __init__(self, h_x, h_y, health, direction, inventory, light_zone, speed, behavior_type, collised_walls,
                 target=None, weapon=None, location=None, attack_time=0, half_attack_time=0, backpack=None, size=1.):
        self.x = h_x
        self.y = h_y
        self.health = health
        self.direction = direction
        self.inventory = inventory
        self.light_zone = light_zone
        self.active_zone = [list(range(self.x - 100, self.x + 126)), list(range(self.y - 50, self.y + 121))]
        self.visible_zone = [list(range(self.x, self.x + 76)), list(range(self.y, self.y + 101))]
        self.speed = speed
        self.behavior_type = behavior_type
        self.location = location
        self.collised_walls = collised_walls
        self.attack_time = attack_time
        self.half_attack_time = half_attack_time
        self.backpack = backpack
        self.weapon = weapon
        self.target = target
        self.size = size

        self.npc_points = [(self.x, self.y), (self.x + 37, self.y), (self.x + 75, self.y),
                           (self.x + 75, self.y + 50),
                           (self.x + 75, self.y + 100), (self.x + 37, self.y + 100),
                           (self.x, self.y + 100), (self.x, self.y + 50)]

    def draw_object(self, size=1):
        if self.backpack and self.direction == 'right':
            self.backpack.draw_on_heretic(self.x + 25, self.y + 45)
        elif self.backpack and self.direction == 'up':
            self.backpack.draw_on_heretic(heretic.x - 5, heretic.y + 45)
        if self.weapon is not None and self.direction == 'right':
            self.weapon.draw_object(self.x + 65 - ((self.half_attack_time -
                                                    self.attack_time) // 2 if self.attack_time > self.half_attack_time else 0),
                                    self.y + 30)
        elif self.weapon is not None and self.direction == 'up':
            self.weapon.draw_object(self.x - 15, self.y + 30 + ((self.half_attack_time -
                                                                 self.attack_time) // 2 if self.attack_time > self.half_attack_time else 0))
        pygame.draw.rect(display, (0, 0, 0), (self.x, self.y, 75, 100))
        eye_colour = (0, 0, 0)
        if self.direction == 'down':
            pygame.draw.rect(display, (255, 255, 255), (self.x + 10, self.y + 10, 20, 20))
            pygame.draw.rect(display, (255, 255, 255), (self.x + 40, self.y + 10, 20, 20))
            pygame.draw.rect(display, eye_colour, (self.x + 18, self.y + 17, 4, 4))
            pygame.draw.rect(display, eye_colour, (self.x + 48, self.y + 17, 4, 4))
            if self.backpack:
                self.backpack.draw_on_heretic(self.x + 40, self.y + 45)
            if self.weapon is not None:
                self.weapon.draw_object(self.x + 65, self.y + 30 - ((self.half_attack_time -
                                                                     self.attack_time) // 2 if self.attack_time > self.half_attack_time else 0))

        elif self.direction == 'left':
            pygame.draw.rect(display, (255, 255, 255), (self.x + 8, self.y + 10, 20, 20))
            pygame.draw.rect(display, (255, 255, 255), (self.x + 38, self.y + 10, 20, 20))
            pygame.draw.rect(display, eye_colour, (self.x + 13, self.y + 17, 4, 4))
            pygame.draw.rect(display, eye_colour, (self.x + 43, self.y + 17, 4, 4))
            if self.backpack:
                self.backpack.draw_on_heretic(self.x + 20, self.y + 45)
            if self.weapon is not None:
                self.weapon.draw_object(self.x + 45 + ((self.half_attack_time -
                                                        self.attack_time) // 2 if self.attack_time > self.half_attack_time else 0),
                                        self.y + 30)

        elif self.direction == 'right':
            pygame.draw.rect(display, (255, 255, 255), (self.x + 20, self.y + 10, 20, 20))
            pygame.draw.rect(display, (255, 255, 255), (self.x + 50, self.y + 10, 20, 20))
            pygame.draw.rect(display, eye_colour, (self.x + 31, self.y + 17, 4, 4))
            pygame.draw.rect(display, eye_colour, (self.x + 61, self.y + 17, 4, 4))
        pygame.draw.rect(display, (0, 0, 0), (self.x - 15, self.y - 30, 110, 25))
        pygame.draw.rect(display, RED, (self.x - 10, self.y - 28,
                                        int(100.0 * float(self.health) / 100.0), 21))

    def walk_left(self):
        self.direction = 'left'
        self.x -= self.speed
        self.visible_zone = [[j for j in range(self.x, self.x + 90)], [k for k in range(self.y, self.y + 60)]]
        self.active_zone = [[j for j in range(self.x - 100, self.x + 150)],
                            [k for k in range(self.y - 100, self.y + 100)]]
        if self.x <= 0:
            self.x = 0

    def walk_right(self):
        self.direction = 'right'
        self.x += self.speed
        self.visible_zone = [[j for j in range(self.x, self.x + 90)], [k for k in range(self.y, self.y + 60)]]
        self.active_zone = [[j for j in range(self.x - 100, self.x + 150)],
                            [k for k in range(self.y - 100, self.y + 100)]]
        if self.x >= 920:
            self.x = 920

    def walk_up(self):
        self.direction = 'up'
        self.y -= self.speed
        self.visible_zone = [[j for j in range(self.x, self.x + 60)], [k for k in range(self.y, self.y + 90)]]
        self.active_zone = [[j for j in range(self.x - 100, self.x + 150)],
                            [k for k in range(self.y - 100, self.y + 100)]]
        if self.y <= 0:
            self.y = 0

    def walk_down(self):
        self.direction = 'down'
        self.y += self.speed
        self.visible_zone = [[j for j in range(self.x, self.x + 60)], [k for k in range(self.y, self.y + 90)]]
        self.active_zone = [[j for j in range(self.x - 100, self.x + 150)],
                            [k for k in range(self.y - 100, self.y + 100)]]
        if self.y >= 700:
            self.y = 700

    def passive_exist(self):
        if self.direction == 'up' and not self.up_stop:
            self.walk_up()
        elif self.direction == 'down' and not self.down_stop:
            self.walk_down()
        elif self.direction == 'left' and not self.left_stop:
            self.walk_left()
        elif self.direction == 'right' and not self.right_stop:
            self.walk_right()

        if not self.delay:
            next_direction = random.choice(directions + ['none', 'none'])
            self.direction = next_direction
            self.stop = False
            if next_direction == 'none':
                self.stop = True
            self.delay = random.randint(250, 450)
        if (self.x <= 10 and self.direction == 'left') or (self.x >= 920 and self.direction == 'right') \
                or (self.y <= 0 and self.direction == 'up') or (self.y >= 685 and self.direction == 'down'):
            self.direction = opposites[self.direction]
        self.delay -= 1


def produce_NPC(n):
    return [NPC(random.randint(300, 800), random.randint(200, 600), random.randint(50, 70),
                random.choice(directions), [], [], random.randint(3, 4), 'passive', {}) for i in range(n)]


class Turret:

    def __init__(self, t_x, t_y, visble_zone, health=100):
        self.x = t_x
        self.y = t_y
        self.visible_zone = visble_zone
        self.health = health

    def draw_object(self, obj_x, obj_y):
        pygame.draw.rect(display, (10, 110, 10), (obj_x - 15, obj_y - 10, 40, 20))

    def shoot(self):
        bullets_list.append(
            Bullet(self.x, self.y, (heretic.x + 37 - self.x) // 35, (heretic.y + 50 - self.y) // 35, self))


class Wall:

    def __init__(self, w_x, w_y, width, height, collised=False, movable=False, health=120):
        self.x = w_x
        self.y = w_y
        self.width = width
        self.height = height
        self.health = height
        self.active_zone = [list(range(self.x - 100, self.x + self.width + 51)),
                            list(range(self.y, self.y + self.height + 1))]
        self.visible_zone = [list(range(self.x, self.x + self.width + 1)),
                             list(range(self.y, self.y + self.height + 1))]
        self.collised = collised
        self.health = health
        self.movable = movable

    def draw_object(self, obj_x, obj_y):
        pygame.draw.rect(display, (50, 50, 50), (obj_x, obj_y, self.width, self.height))


class Vase(Wall):

    def draw_object(self, obj_x, obj_y):
        pygame.draw.polygon(display, (184, 133, 71),
                            ((obj_x, obj_y), (obj_x + 40, obj_y), (obj_x + 30, obj_y + 20), (obj_x + 10, obj_y + 20)))
        pygame.draw.polygon(display, (184, 133, 71), (
            (obj_x + 5, obj_y + 20), (obj_x + 35, obj_y + 20), (obj_x + 30, obj_y + 45), (obj_x + 10, obj_y + 45)))
        pygame.draw.polygon(display, (0, 0, 0), (
            (obj_x + 7, obj_y + 27), (obj_x + 33, obj_y + 27), (obj_x + 31, obj_y + 42), (obj_x + 9, obj_y + 42)))


class Bullet:

    def __init__(self, b_x, b_y, g_speed, v_speed, owner, mark_list=None):
        self.x = b_x
        self.y = b_y
        self.g_speed = g_speed
        self.v_speed = v_speed
        self.mark_list = mark_list
        self.owner = owner

    def draw_object(self, obj_x, obj_y):
        pygame.draw.circle(display, (200, 10, 10), (obj_x, obj_y), 5)
        pygame.draw.circle(display, (10, 10, 10), (obj_x, obj_y), 6, 1)

    def move(self):
        self.x += self.g_speed
        self.y += self.v_speed

        '''
        if self.v_speed < 3:
            self.v_speed = 3 if self.v_speed > 0 else - 3
        if self.g_speed < 3:
            self.g_speed = 3 if self.g_speed > 0 else - 3
        '''


class Mark:

    def __init__(self, m_x, m_y, life_time):
        self.x = m_x
        self.y = m_y
        self.life_time = life_time

    def draw_object(self, obj_x, obj_y):
        pygame.draw.rect(display, (200, 0, 0), (obj_x - 5, obj_y - 5, 10, 10))
        self.life_time -= 1


class Item:

    def __init__(self, d_x, d_y, active_zone, visible_zone, type, description, location, strength=0, energy_value=0):
        self.x = d_x
        self.y = d_y
        self.active_zone = active_zone
        self.visible_zone = visible_zone
        self.type = type
        self.description = description
        self.location = location
        self.energy_value = energy_value
        self.strength = strength

    def up_down(self):
        if tick % 60 == 1:
            self.y += 17
        elif tick % 60 == 29:
            self.y -= 17


class Bow:

    def __init__(self, reload):
        self.reload = reload

    def draw_object(self, x, y):
        pygame.draw.lines(display, (168, 167, 159), False, (
            (x, y + self.reload // 20), (x - 15 - self.reload // 10, y + 20), (x, y + 40 - self.reload // 20)), 3)
        pygame.draw.lines(display, (150, 89, 35), False,
                          ((x, y + self.reload // 20), (x + 15, y + 10), (x + 20, y + 20),
                           (x + 15, y + 30), (x, y + 40 - self.reload // 20)), 5)

    @staticmethod
    def shoot(self, target):
        bullets_list.append(Bullet(heretic.x + 37, heretic.y + 50, (-heretic.x - 37 + target.x) // 38,
                                   (-heretic.y - 50 + target.y) // 38, heretic))


class Room:
    visited = False

    def __init__(self, walls_list, entities_list, entrances, floor):
        self.walls_list = walls_list
        self.entities_list = entities_list
        self.entrances = entrances
        self.floor = floor


def draw_heretic(obj_x, obj_y, direction, size=1.):
    if heretic.backpack and direction == 'right':
        heretic.backpack.draw_on_heretic(obj_x + 25, obj_y + 45)
    elif heretic.backpack and direction == 'up':
        heretic.backpack.draw_on_heretic(obj_x - 5, obj_y + 45)
    if heretic.weapon != 'none' and direction == 'right':
        heretic.weapon.draw_object(obj_x + 65 - ((heretic.half_attack_time -
                                                  heretic.attack_time) // 2 if heretic.attack_time > heretic.half_attack_time else 0),
                                   obj_y + 30)
    elif heretic.weapon != 'none' and direction == 'up':
        heretic.weapon.draw_object(obj_x - 15, obj_y + 30 + ((heretic.half_attack_time -
                                                              heretic.attack_time) // 2 if heretic.attack_time > heretic.half_attack_time else 0))
    pygame.draw.rect(display, (0, 0, 0), (obj_x, obj_y, int(75 * size), int(100 * size)))
    eye_colour = (0, 0, 0)
    if direction == 'down':
        pygame.draw.rect(display, (255, 255, 255),
                         tuple(map(int, ((obj_x + 10 * size), obj_y + 10 * size, 20 * size, 20 * size))))
        pygame.draw.rect(display, (255, 255, 255),
                         tuple(map(int, (obj_x + 40 * size, obj_y + 10 * size, 20 * size, 20 * size))))
        pygame.draw.rect(display, eye_colour,
                         tuple(map(int, (obj_x + 18 * size, obj_y + 17 * size, 4 * size, 4 * size))))
        pygame.draw.rect(display, eye_colour,
                         tuple(map(int, (obj_x + 48 * size, obj_y + 17 * size, 4 * size, 4 * size))))
        if heretic.backpack:
            heretic.backpack.draw_on_heretic(int(obj_x + 40 * size), int(obj_y + 45 * size * 2))
        if heretic.weapon != 'none':
            heretic.weapon.draw_object(int(obj_x + 65 * size), int(obj_y + 30 * size - ((heretic.half_attack_time -
                                                                                         heretic.attack_time) // 2 if heretic.attack_time > heretic.half_attack_time else 0)))

    elif direction == 'left':
        pygame.draw.rect(display, (255, 255, 255),
                         tuple(map(int, (obj_x + 8 * size, obj_y + 10 * size, 20 * size, 20 * size))))
        pygame.draw.rect(display, (255, 255, 255),
                         tuple(map(int, (obj_x + 38 * size, obj_y + 10 * size, 20 * size, 20 * size))))
        pygame.draw.rect(display, eye_colour,
                         tuple(map(int, (obj_x + 13 * size, obj_y + 17 * size, 4 * size, 4 * size))))
        pygame.draw.rect(display, eye_colour,
                         tuple(map(int, (obj_x + 43 * size, obj_y + 17 * size, 4 * size, 4 * size))))
        if heretic.backpack:
            heretic.backpack.draw_on_heretic(int(obj_x + 20 * size), int(obj_y + 45 * size))
        if heretic.weapon != 'none':
            heretic.weapon.draw_object(int(obj_x + 45 * size + ((heretic.half_attack_time -
                                                                 heretic.attack_time) // 2 if heretic.attack_time > heretic.half_attack_time else 0)),
                                       int(obj_y + 30 * size))

    elif direction == 'right':
        pygame.draw.rect(display, (255, 255, 255),
                         tuple(map(int, (obj_x + 20 * size, obj_y + 10 * size, 20 * size, 20 * size))))
        pygame.draw.rect(display, (255, 255, 255),
                         tuple(map(int, (obj_x + 50 * size, obj_y + 10 * size, 20 * size, 20 * size))))
        pygame.draw.rect(display, eye_colour,
                         tuple(map(int, (obj_x + 31 * size, obj_y + 17 * size, 4 * size, 4 * size))))
        pygame.draw.rect(display, eye_colour,
                         tuple(map(int, (obj_x + 61 * size, obj_y + 17 * size, 4 * size, 4 * size))))


heretic = Heretic(100, 100, 75, 100, 100, 'left', [], location=random.randint(1, dung_width * dung_length))

heretic_points = [(heretic.x, heretic.y), (heretic.x + 37, heretic.y), (heretic.x + 75, heretic.y),
                  (heretic.x + 75, heretic.y + 50),
                  (heretic.x + 75, heretic.y + 100), (heretic.x + 37, heretic.y + 100), (heretic.x, heretic.y + 100),
                  (heretic.x, heretic.y + 50)]

stop = []
left_stop, right_stop, up_stop, down_stop = False, False, False, False

rooms = {}
'''
Генерация стен
'''
for i in range(1, dung_width * dung_length + 1):
    ways = random.sample(['down', 'right'], random.randint(1, 2))
    enters = []
    walls = []
    if i > dung_length and 'down' in rooms[i - dung_length].entrances:
        walls.append(Wall(0, 0, width=random.randint(display_width // 2 - 250, display_width // 2 - 100),
                          height=random.randint(50, 100)))
        walls.append(Wall(x := random.randint(display_width // 2 + 150, display_width // 2 + 220), y := 0,
                          width := display_width - x, height := random.randint(50, 100)))
        enters.append('up')
    else:
        walls.append(Wall(0, 0, width := display_width, height := random.randint(50, 100)))

    if i % dung_length != 1 and 'right' in rooms[i - 1].entrances:
        walls.append(Wall(0, 0, width=random.randint(50, 100), height=random.randint(display_height // 2 - 250, display_height // 2 - 100)))
        walls.append(Wall(0, y := random.randint(display_height // 2 + 150, display_height // 2 + 220), width := random.randint(50, 100), height := display_height - y))
        enters.append('left')
    else:
        walls.append(Wall(0, 0, width=random.randint(50, 100), height=1000))

    if 'down' in ways and i < (dung_width - 1) * dung_length:
        walls.append(Wall(0, y := random.randint(display_height - 100, display_height - 50),
                          width := random.randint(display_width // 2 - 250, display_width // 2 - 100),
                          height := display_height - y))
        walls.append(
            Wall(x := random.randint(display_width // 2 + 150, display_width // 2 + 220), y := random.randint(display_height - 100, display_height - 50),
                 width=display_width - x, height=display_height - y))
        enters.append('down')
    else:
        walls.append(Wall(0, y := random.randint(display_height - 100, display_height - 50), width := display_width, height := display_height - y))

    if 'right' in ways and i % dung_length:
        walls.append(Wall(x := random.randint(display_width - 100, display_width - 50), 0, width=display_width - x,
                          height=random.randint(display_height // 2 - 250, display_height // 2 - 100)))
        walls.append(Wall(x := random.randint(display_width - 100, display_width - 50),
                          y := random.randint(display_height // 2 + 150, display_height // 2 + 220), width=display_width - x, height=display_height - y))
        enters.append('right')
    else:
        walls.append(Wall(x := random.randint(display_width - 100, display_width - 50), y := 0, width := display_width - x, height := display_height))

    walls += [Wall(random.randrange(100, 905, 5), random.randrange(100, 705, 5),
                   width=random.randrange(50, 120, 5),
                   height=random.randrange(50, 120, 5), movable=True) for
              j in range(random.randint(5, 10))]
    walls += [Vase(random.randrange(100, 905, 5), random.randrange(100, 705, 5),
                   width=40, height=45, movable=True) for j in range(random.randint(3, 5))]
    if not enters:
        enters = [i for i in directions if i not in ways]
    entities_list = produce_NPC(random.randint(1, 3))
    rooms[i] = Room(walls, entities_list, enters, random.choice(['stone', 'wooden']))

# Кажется, после генерации следует проверить все стены на смежные переходы вложенным циклом !

curr_room = random.randint(1, dung_width * dung_length)
collised_walls = {wall: [] for wall in rooms[curr_room].walls_list}
current_interface = None

while True:
    console_req = False
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # wall_height, wall_width = (random.randint(90, 150), random.randint(40, 80)) if event.button == 1 else (
            # random.randint(40, 80), random.randint(90, 150))
            # rooms[curr_room].walls_list.append(Wall(x := event.pos[0], y := event.pos[1], wall_width, wall_height, movable=True))
            if event.button == 1:
                for wall in rooms[curr_room].walls_list:
                    if event.pos[0] in wall.visible_zone[0] and event.pos[1] in wall.visible_zone[1] \
                            and heretic.x in wall.active_zone[0] and heretic.y in wall.active_zone[1] and heretic.attack_time <= 0:
                        heretic.hit(wall)
                        break

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                if not current_interface:
                    current_interface = 'Map'
                    bloor.set_alpha(200)
                else:
                    current_interface = None
                    bloor.set_alpha(15)
            elif event.key == pygame.K_i:
                current_interface = "Inventory" if current_interface != 'Inventory' else None
            elif event.key == pygame.K_SLASH:
                console_req = True
                com = input('Введите команду: ').split()
                com_name, args = com[0], com[1:]
                if com_name == 'tp':
                    room = int(args[0])
                    heretic.tp(room)

    if console_req:
        continue
    keys = pygame.key.get_pressed()
    for wall in rooms[curr_room].walls_list:
        if not collised_walls.get(wall, 0):
            continue
        if any([1 in collised_walls[wall], 7 in collised_walls[wall], 8 in collised_walls[wall]]) and wall.x + len(
                wall.visible_zone[0]) - 15 < heretic.x:
            if wall.movable:
                wall.x -= 1
                wall.active_zone = [list(range(wall.x - 100, wall.x + wall.width + 25)),
                                    list(range(wall.y - 100, wall.y + wall.height + 25))]
                wall.visible_zone = [list(range(wall.x, wall.x + wall.width)),
                                     list(range(wall.y, wall.y + wall.height))]
            left_stop = True

        if any([3 in collised_walls[wall], 4 in collised_walls[wall],
                5 in collised_walls[wall]]) and wall.x > heretic.x + 60:
            if wall.movable:
                wall.x += 1
                wall.active_zone = [list(range(wall.x - 100, wall.x + wall.width + 25)),
                                    list(range(wall.y - 100, wall.y + wall.height + 25))]
                wall.visible_zone = [list(range(wall.x, wall.x + wall.width)),
                                     list(range(wall.y, wall.y + wall.height))]
            right_stop = True
        if any([1 in collised_walls[wall], 2 in collised_walls[wall], 3 in collised_walls[wall]]) and wall.y + len(
                wall.visible_zone[1]) - 15 < heretic.y:
            if wall.movable:
                wall.y -= 1
                wall.active_zone = [list(range(wall.x - 100, wall.x + wall.width + 25)),
                                    list(range(wall.y - 100, wall.y + wall.height + 25))]
                wall.visible_zone = [list(range(wall.x, wall.x + wall.width)),
                                     list(range(wall.y, wall.y + wall.height))]
            up_stop = True
        if any([5 in collised_walls[wall], 6 in collised_walls[wall],
                7 in collised_walls[wall]]) and wall.y > heretic.y + 85:
            if wall.movable:
                wall.y += 1
                wall.active_zone = [list(range(wall.x - 100, wall.x + wall.width + 25)),
                                    list(range(wall.y - 100, wall.y + wall.height + 25))]
                wall.visible_zone = [list(range(wall.x, wall.x + wall.width)),
                                     list(range(wall.y, wall.y + wall.height))]
            down_stop = True

    if not current_interface:
        if keys[pygame.K_a] and heretic.x > -3 and not left_stop:
            heretic.x -= 5
            heretic.direction = 'left'

        elif keys[pygame.K_d] and heretic.x < display_width - 75 and not right_stop:
            heretic.direction = 'right'
            heretic.x += 5

        if keys[pygame.K_w] and heretic.y > 0 and not up_stop:

            heretic.y -= 4
            heretic.direction = 'up'

        elif keys[pygame.K_s] and heretic.y < display_height - 100 and not down_stop:
            heretic.direction = 'down'
            heretic.y += 4
    if current_interface == 'Inventory':
        display.fill((184, 173, 118))
        display.blit(inventory_font.render('Инвентарь', True, (0, 0, 0)), (120, 10))
        display.blit(inventory_font.render('Часы: день/ночь', True, (0, 0, 0)), (800, 10))
        pygame.draw.rect(display, (0, 0, 0), (800, 150, 600, 60))
        pygame.draw.rect(display, (184, 173, 118), (1260, 155, 130, 50))
        pygame.draw.rect(display, (200, 0, 0), (810, 155, int(445 * heretic.health // 100), 50))
        pygame.draw.rect(display, (0, 0, 200), (810, 230, 130, 130))
        pygame.draw.rect(display, (190, 190, 190), (825, 245, 100, 100))
        pygame.draw.rect(display, (0, 0, 200), (970, 230, 130, 130))
        pygame.draw.rect(display, (190, 190, 190), (985, 245, 100, 100))
        if heretic.weapon != 'none':
            heretic.weapon.draw_object(865, 260)
            display.blit(active_font.render(heretic.weapon.type, True, (0, 0, 0)), (825, 365))
        else:
            pygame.draw.rect(display, (184, 173, 118), (860, 260, 20, 45))
            pygame.draw.polygon(display, (184, 173, 118), ((860, 260), (870, 252), (880, 260)))
            pygame.draw.rect(display, (184, 173, 118), (850, 300, 40, 6))
            pygame.draw.rect(display, (184, 173, 118), (864, 306, 12, 20))

        if heretic.backpack:
            heretic.backpack.draw_object(1000, 260)
            display.blit(active_font.render(heretic.backpack.type, True, (0, 0, 0)), (960, 365))
        else:
            pygame.draw.rect(display, (184, 173, 118), (1000, 260, 50, 70))
            pygame.draw.lines(display, (184, 173, 118), True, ((1000, 260), (1040, 245), (1060, 270)), 8)
            pygame.draw.polygon(display, (184, 173, 118),
                                ((998, 260), (998, 285), (1025, 295), (1052, 285), (1052, 260)))

            pygame.draw.circle(display, (184, 173, 118), (1035, 289), 3)

        pygame.draw.line(display, (161, 96, 54), (700, 0), (700, 900), 100)

        pygame.draw.rect(display, (240, 240, 240), (870, 450, 500, 450))

        for i in range(510, 871, 60):
            pygame.draw.line(display, (0, 0, 0), (880, i), (1350, i), 5)

        for i in range(50, 601, 150):
            for j in range(100, 801, 150):
                pygame.draw.rect(display, (0, 0, 200), (i, j, 130, 130))
                pygame.draw.rect(display, (190, 190, 190), (i + 15, j + 15, 100, 100))

        for i in range(len(heretic.inventory)):
            # if isinstance(heretic.inventory[i], Berry) or isinstance(heretic.inventory[i], DroppedBerry):
            #     heretic.inventory[i].draw_object(100 + 150 * (i % 4), 160 + 150 * (i // 4))
            #
            # elif isinstance(heretic.inventory[i], Log):
            #     heretic.inventory[i].draw_object(75 + 150 * (i % 4), 150 + 150 * (i // 4))
            #
            # elif isinstance(heretic.inventory[i], Pine):
            #     heretic.inventory[i].draw_object(80 + 150 * (i % 4), 150 + 150 * (i // 4))
            #
            # elif isinstance(heretic.inventory[i], Juice):
            #     heretic.inventory[i].draw_object(90 + 150 * (i % 4), 160 + 150 * (i // 4))
            #
            # elif isinstance(heretic.inventory[i], RawMeat):
            #     heretic.inventory[i].draw_object(80 + 150 * (i % 4), 170 + 150 * (i // 4))
            #
            # elif isinstance(heretic.inventory[i], Meat):
            #     heretic.inventory[i].draw_object(80 + 150 * (i % 4), 170 + 150 * (i // 4))
            #
            # elif isinstance(heretic.inventory[i], Stick):
            #     heretic.inventory[i].draw_object(110 + 150 * (i % 4), 150 + 150 * (i // 4))
            #
            # elif any([isinstance(heretic.inventory[i], Stone), isinstance(heretic.inventory[i], IronOre),
            #           isinstance(heretic.inventory[i], Coal)]):
            #     heretic.inventory[i].draw_object(90 + 150 * (i % 4), 150 + 150 * (i // 4))
            #
            # elif isinstance(heretic.inventory[i], SharpenedStone):
            #     heretic.inventory[i].draw_object(90 + 150 * (i % 4), 150 + 150 * (i // 4))
            #
            # elif isinstance(heretic.inventory[i], PickAxe) or isinstance(heretic.inventory[i], Shovel):
            #     heretic.inventory[i].draw_object(90 + 150 * (i % 4), 140 + 150 * (i // 4))
            '''            if isinstance(heretic.inventory[i], Drop):
                heretic.inventory[i].draw_object(90 + 150 * (i % 4), 140 + 150 * (i // 4))
            '''


            # if 100 < pos[0] < 650 and pos[1] > 100:
            #     pos_index = (pos[0] - 50) // 150 + (pos[1] - 100) // 150 * 4
            #     if pos_index < len(heretic.inventory):
            #         display.blit(inventory_font.render(heretic.inventory[pos_index].type, True,
            #                                            (0, 0, 0)), (pos[0] - 100, pos[1] - 75))
            # if isinstance(chosen_item, Drop) or isinstance(chosen_item, Berry) or isinstance(chosen_item, Weapon):
            #     for i in range(len(chosen_item.description)):
            #         display.blit(active_font.render(chosen_item.description[i], True, (0, 0, 0)), (880, 465 + i * 60))
    else:
        display.fill((252, 240, 188))
        if rooms[curr_room].floor == 'stone':
            display.blit(stone_floor, (0, 0))
        for bullet in bullets_list:
            bullet.draw_object(bullet.x, bullet.y)
            if not tick % 3:
                bullet.move()
            for mark in bullet.mark_list:
                mark.draw_object(mark.x, mark.y)

        for wall in rooms[curr_room].walls_list:
            wall.draw_object(wall.x, wall.y)

        for npc in rooms[curr_room].entities_list:
            npc.draw_object()
            npc.passive_exist()

        heretic.draw_object(heretic.visible_zone)
        for i in stop:
            pygame.draw.rect(display, (200, 0, 0), (*heretic_points[i - 1], 5, 5))
        # heretic2.draw_object()
        '''
    Отрисовка карты
        '''

        if current_interface == 'Map':
            display.blit(bloor, (0, 0))
            display.blit(map_image, (40, 50))
            for j in range(90, 90 + dung_width * 80, 80):
                for i in range(90, 90 + dung_length * 80, 80):
                    r_ind = (i - 90) // 80 + (j - 90) // 80 * dung_length + 1
                    if rooms[r_ind].visited:
                        pygame.draw.rect(display, (240, 240, 240), (i, j, 45, 35))
                        if 'up' in rooms[r_ind].entrances:
                            pygame.draw.rect(display, (200, 200, 200), (i + 12, j - 25, 20, 25))
                        if 'down' in rooms[r_ind].entrances:
                            pygame.draw.rect(display, (200, 200, 200), (i + 12, j + 35, 20, 20))
                        if 'right' in rooms[r_ind].entrances:
                            pygame.draw.rect(display, (200, 200, 200), (i + 45, j + 7, 20, 20))
                        if 'left' in rooms[r_ind].entrances:
                            pygame.draw.rect(display, (200, 200, 200), (i - 15, j + 7, 15, 20))
                        if r_ind == curr_room:
                            draw_heretic(i + 10, j + 5, heretic.direction, 0.3)
                    else:
                        pygame.draw.rect(display, (10, 10, 10), (i, j, 45, 35))
                # print(i, j, (i - 90) // 80, (j - 90) // 80 * dung_length)

    display.blit(text_font.render(str(curr_room), True, (255, 255, 255)), (950, 20))
    display.blit(cursor_for_battle, cursor_for_battle.get_rect(center=(mouse_pos[0], mouse_pos[1])))

    # for j in range(dung_length):

    # pygame.draw.rect(display, (215, 185, 147), (100, 50, 600, 600))
    pygame.display.update()
    clock.tick(60)

    heretic.visible_zone = [list(range(heretic.x, heretic.x + int(76 * heretic.size))),
                            list(range(heretic.y, int(heretic.y + 101 * heretic.size)))]
    heretic.active_zone = [list(range(heretic.x - int(50 * heretic.size), heretic.x + int(151 * heretic.size))),
                           list(range(heretic.y - int(50 * heretic.size), heretic.y + int(151 * heretic.size)))]
    tick += 1
    # if not tick % (60 - (tick % 29500 // 500)):
    # turret.shoot()

    for i in bullets_list:
        if any([i.x < 0, i.x > 1000, i.y < 0, i.y > 800]):
            bullets_list.remove(i)
        i.mark_list = list(filter(lambda j: j.life_time > 0, i.mark_list))
        i.mark_list.append(Mark(i.x, i.y, 10))
        for entity in entities_list:
            if i.owner != entity and i.x in entity.visible_zone[0] and i.y in entity.visible_zone[1]:
                bullets_list.remove(i)
                if entity.health >= 5:
                    entity.health -= 5

    stop = []
    left_stop, right_stop, up_stop, down_stop = False, False, False, False
    collised_walls = {wall: [] for wall in rooms[curr_room].walls_list}
    '''
Расчет столкновений еретика со стеной
    '''
    for point in range(len(heretic_points)):

        for wall in rooms[curr_room].walls_list:
            if heretic_points[point][0] in wall.visible_zone[0] and heretic_points[point][1] in wall.visible_zone[1]:
                stop.append(point + 1)
                collised_walls[wall].append(point + 1)

                '''
                if point in [1, 2, 3]:
                    heretic.y += 5
                if point in [3, 4, 5]:
                    heretic.x -= 5
                if point in [1, 7, 8]:
                    heretic.x += 7
                if point in [5, 6, 7]:
                    heretic.y -= 5'''

    heretic_points = [(heretic.x, heretic.y), (heretic.x + 37, heretic.y), (heretic.x + 75, heretic.y),
                      (heretic.x + 75, heretic.y + 50),
                      (heretic.x + 75, heretic.y + 100), (heretic.x + 37, heretic.y + 100),
                      (heretic.x, heretic.y + 100), (heretic.x, heretic.y + 50)]
    '''
    Расчет столкновений существ со стеной
        '''
    for entity in rooms[curr_room].entities_list:
        entity.left_stop, entity.right_stop, entity.up_stop, entity.down_stop = False, False, False, False
        entity.collised_walls = {wall: [] for wall in rooms[curr_room].walls_list}
        entity.npc_points = [(entity.x, entity.y), (entity.x + 37, entity.y), (entity.x + 75, entity.y),
                             (entity.x + 75, entity.y + 50),
                             (entity.x + 75, entity.y + 100), (entity.x + 37, entity.y + 100),
                             (entity.x, entity.y + 100), (entity.x, entity.y + 50)]

    for entity in rooms[curr_room].entities_list:
        for point in range(len(entity.npc_points)):
            for wall in rooms[curr_room].walls_list:
                if entity.npc_points[point][0] in wall.visible_zone[0] and entity.npc_points[point][1] in \
                        wall.visible_zone[1]:
                    entity.collised_walls[wall].append(point + 1)

    for entity in rooms[curr_room].entities_list:
        for wall in entity.collised_walls.keys():
            if not entity.collised_walls.get(wall, 0):
                continue
            if any([1 in entity.collised_walls[wall], 7 in entity.collised_walls[wall],
                    8 in entity.collised_walls[wall]]) and wall.x + len(
                wall.visible_zone[0]) - 15 < entity.x:
                if wall.movable:
                    wall.x -= 1
                    wall.active_zone = [list(range(wall.x - 100, wall.x + wall.width + 25)),
                                        list(range(wall.y - 100, wall.y + wall.height + 25))]
                    wall.visible_zone = [list(range(wall.x, wall.x + wall.width)),
                                         list(range(wall.y, wall.y + wall.height))]
                entity.left_stop = True

            if any([3 in entity.collised_walls[wall], 4 in entity.collised_walls[wall],
                    5 in entity.collised_walls[wall]]) and wall.x > entity.x + 60:
                if wall.movable:
                    wall.x += 1
                    wall.active_zone = [list(range(wall.x - 100, wall.x + wall.width + 25)),
                                        list(range(wall.y - 100, wall.y + wall.height + 25))]
                    wall.visible_zone = [list(range(wall.x, wall.x + wall.width)),
                                         list(range(wall.y, wall.y + wall.height))]
                entity.right_stop = True

            if any([1 in entity.collised_walls[wall], 2 in entity.collised_walls[wall],
                    3 in entity.collised_walls[wall]]) and wall.y + len(
                wall.visible_zone[1]) - 15 < entity.y:
                if wall.movable:
                    wall.y -= 1
                    wall.active_zone = [list(range(wall.x - 100, wall.x + wall.width + 25)),
                                        list(range(wall.y - 100, wall.y + wall.height + 25))]
                    wall.visible_zone = [list(range(wall.x, wall.x + wall.width)),
                                         list(range(wall.y, wall.y + wall.height))]
                entity.up_stop = True

            if any([5 in entity.collised_walls[wall], 6 in entity.collised_walls[wall],
                    7 in entity.collised_walls[wall]]) and wall.y > entity.y + 85:
                if wall.movable:
                    wall.y += 1
                    wall.active_zone = [list(range(wall.x - 100, wall.x + wall.width + 25)),
                                        list(range(wall.y - 100, wall.y + wall.height + 25))]
                    wall.visible_zone = [list(range(wall.x, wall.x + wall.width)),
                                         list(range(wall.y, wall.y + wall.height))]
                entity.down_stop = True

    if heretic.y < 20 and curr_room > dung_length:
        curr_room -= dung_length
        heretic.y = display_height - 150
    elif heretic.y > display_height - 110 and curr_room < dung_width * (dung_length - 1):
        curr_room += dung_length
        heretic.y = 30
    elif heretic.x < 15 and curr_room % dung_length != 1:
        curr_room -= 1
        heretic.x = display_width - 100
    elif heretic.x > display_width - 85 and curr_room % dung_length:
        curr_room += 1
        heretic.x = 20

    if heretic.location != curr_room:
        heretic.location = curr_room
        rooms[curr_room].visited = True

    if heretic.attack_time:
        heretic.attack_time -= 1

    if not tick % 300:
        print(f'{curr_room} - {rooms[curr_room].entrances}')
