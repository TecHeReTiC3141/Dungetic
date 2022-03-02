from classes.Heretic import *


class NPC(Heretic):
    stop = False
    delay = random.randint(250, 450)

    def __init__(self, x, y, width, height, health, direction, inventory, speed, behavior_type='passive',
                 target=None, weapon=None, location=None, attack_time=0, half_attack_time=0, backpack=None, size=1.):
        super().__init__(x, y, width, height, health, direction, inventory,
                         speed, target, weapon, location, attack_time, half_attack_time, backpack, size)
        self.collised_walls = []


    # def draw_object(self, display):
    #     self.visible_zone.fill((0, 0, 0))
    #     if self.weapon is not None and self.direction == 'right':
    #         self.weapon.draw_object(self.x + 65 - ((self.half_attack_time -
    #                                                 self.attack_time) // 2 if self.attack_time > self.half_attack_time else 0),
    #                                 self.y + 30)
    #     elif self.weapon is not None and self.direction == 'up':
    #         self.weapon.draw_object(self.x - 15, self.y + 30 + ((self.half_attack_time -
    #                                                              self.attack_time) // 2 if self.attack_time > self.half_attack_time else 0))
    #     pygame.draw.rect(display, (0, 0, 0), (self.x, self.y, 75, 100))
    #     eye_colour = (0, 0, 0)
    #     if self.direction == 'down':
    #         pygame.draw.rect(display, (255, 255, 255), (self.x + 10, self.y + 10, 20, 20))
    #         pygame.draw.rect(display, (255, 255, 255), (self.x + 40, self.y + 10, 20, 20))
    #         pygame.draw.rect(display, eye_colour, (self.x + 18, self.y + 17, 4, 4))
    #         pygame.draw.rect(display, eye_colour, (self.x + 48, self.y + 17, 4, 4))
    #         if self.backpack:
    #             self.backpack.draw_on_heretic(self.x + 40, self.y + 45)
    #         if self.weapon is not None:
    #             self.weapon.draw_object(self.x + 65, self.y + 30 - ((self.half_attack_time -
    #                                                                  self.attack_time) // 2 if self.attack_time > self.half_attack_time else 0))
    #
    #     elif self.direction == 'left':
    #         pygame.draw.rect(display, (255, 255, 255), (self.x + 8, self.y + 10, 20, 20))
    #         pygame.draw.rect(display, (255, 255, 255), (self.x + 38, self.y + 10, 20, 20))
    #         pygame.draw.rect(display, eye_colour, (self.x + 13, self.y + 17, 4, 4))
    #         pygame.draw.rect(display, eye_colour, (self.x + 43, self.y + 17, 4, 4))
    #         if self.backpack:
    #             self.backpack.draw_on_heretic(self.x + 20, self.y + 45)
    #         if self.weapon is not None:
    #             self.weapon.draw_object(self.x + 45 + ((self.half_attack_time -
    #                                                     self.attack_time) // 2 if self.attack_time > self.half_attack_time else 0),
    #                                     self.y + 30)
    #
    #     elif self.direction == 'right':
    #         pygame.draw.rect(display, (255, 255, 255), (self.x + 20, self.y + 10, 20, 20))
    #         pygame.draw.rect(display, (255, 255, 255), (self.x + 50, self.y + 10, 20, 20))
    #         pygame.draw.rect(display, eye_colour, (self.x + 31, self.y + 17, 4, 4))
    #         pygame.draw.rect(display, eye_colour, (self.x + 61, self.y + 17, 4, 4))
    #     pygame.draw.rect(display, (0, 0, 0), (self.x - 15, self.y - 30, 110, 25))
    #     pygame.draw.rect(display, RED, (self.x - 10, self.y - 28,
    #                                     int(100.0 * float(self.health) / 100.0), 21))

    def walk(self):
        if not self.stop:
            if self.direction == 'up' and not self.up_stop:
                self.direction = 'up'
                self.y = max(self.y - self.speed, 0)
                self.phys_rect.move_ip(0, -self.speed)
                self.active_zone.move_ip(0, -self.speed)

            elif self.direction == 'down' and not self.down_stop:
                self.direction = 'down'
                self.y = min(self.y + self.speed, display_height - self.height)
                self.phys_rect.move_ip(0, self.speed)
                self.active_zone.move_ip(0, self.speed)

            elif self.direction == 'left' and not self.left_stop:
                self.direction = 'left'
                self.x = max(self.x - self.speed, 0)
                self.phys_rect.move_ip(-self.speed, 0)
                self.active_zone.move_ip(-self.speed, 0)

            elif self.direction == 'right' and not self.right_stop:
                self.direction = 'right'
                self.x = min(self.x + self.speed, display_width - self.width)
                self.phys_rect.move_ip(self.speed, 0)
                self.active_zone.move_ip(self.speed, 0)

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


def produce_NPC(n):
    return [NPC(random.randint(300, 800), random.randint(200, 600), 75, 100, 5,
                random.choice(directions), [], speed=random.randint(3, 4)) for i in range(n)]
