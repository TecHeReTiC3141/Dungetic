from scripts.constants_and_sources import *

class Turret:

    def __init__(self, x, y, visble_zone, health=100):
        self.x = x
        self.y = y
        self.visible_zone = visble_zone
        self.health = health

    def draw_object(self, obj_x, obj_y, display):
        pygame.draw.rect(display, (10, 110, 10), (obj_x - 15, obj_y - 10, 40, 20))

    def shoot(self, target):
        bullets_list.append(
            Bullet(self.x, self.y, (target.x + 37 - self.x) // 35, (target.y + 50 - self.y) // 35, self))


class Bullet:

    def __init__(self, b_x, b_y, g_speed, v_speed, owner, mark_list=None):
        self.x = b_x
        self.y = b_y
        self.g_speed = g_speed
        self.v_speed = v_speed
        self.mark_list = mark_list
        self.owner = owner

    def draw_object(self, obj_x, obj_y, display):
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

    def draw_object(self, obj_x, obj_y, display):
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