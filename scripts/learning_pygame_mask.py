import pygame
from random import *

display_width, display_height = 1280, 720
display = pygame.display.set_mode((display_width, display_height))


class Wall:

    def __init__(self, x, y, width, height, collised=False, movable=False, *args):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = height
        self.weight = width * height // 2500
        self.active_zone = pygame.Rect(x - 100, y, width + 51, height + 1)
        self.cur_rect = pygame.Rect(x, y, width, height)
        self.prev_rect = self.cur_rect.copy()
        self.inner_phys_rect = pygame.Rect(x + 5, y + 5,
                                           max(width - 10, 10), max(height - 10, 10))
        self.outer_phys_rect = pygame.Rect(x - 10, y - 10, width + 20, height + 20)
        self.visible_zone = pygame.Surface((width, height))
        self.sprite = pygame.Surface((width, height))

        self.visible_zone.set_colorkey('Black')
        self.sprite.set_colorkey('Black')
        self.mask = pygame.mask.from_surface(self.sprite)
        self.collised = collised
        self.movable = movable
        super().__init__(*args)

    def draw_object(self, display: pygame.Surface):
        # pygame.draw.rect(display, ('#CCCCCC'), self.outer_phys_rect)
        pygame.draw.rect(self.sprite, (70, 70, 70), (0, 0, self.width, self.height), border_radius=8)

        self.visible_zone.blit(self.sprite, (0, 0))
        display.blit(self.visible_zone, self.cur_rect)
        # pygame.draw.rect(display, ('#AAAAAA'), self.inner_phys_rect)


class Vase(Wall):

    def __init__(self, x, y, width, height, collised=False, movable=False):
        super().__init__(x, y, width, height, collised, movable)
        self.sprite = pygame.image.load('../images/surroundings/Vase1.png').convert_alpha()
        self.cur_rect.update(*self.cur_rect.topleft, *self.sprite.get_size())
        self.sprite.set_colorkey('#FFFFFF')
        self.visible_zone.set_colorkey('White')

    def draw_object(self, display: pygame.Surface):
        self.visible_zone.fill('#FFFFFF')
        self.visible_zone.blit(self.sprite, (0, 0))
        display.blit(self.visible_zone, self.cur_rect)

        return self.visible_zone


class Point:

    def __init__(self, x, y):
        self.surf = pygame.Surface((40, 40))

        self.rect = self.surf.get_rect(topleft=(x, y))
        self.surf.set_colorkey('black')
        pygame.draw.circle(self.surf, 'blue', (self.surf.get_width() // 2,
                                               self.surf.get_height() // 2), self.surf.get_height() // 2)

        self.mask = pygame.mask.from_surface(self.surf)

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

    def draw(self, display: pygame.Surface):
        display.blit(self.surf, self.rect)

    def collide(self, obsts: list[Vase]):
        pygame.draw.circle(self.surf, 'blue', (self.surf.get_width() // 2,
                                               self.surf.get_height() // 2), self.surf.get_height() // 2)

        for obst in obsts:
            if obst.cur_rect.colliderect(self.rect):
                pygame.draw.circle(self.surf, 'red', (self.surf.get_width() // 2,
                                                      self.surf.get_height() // 2), self.surf.get_height() // 2)

                mask = pygame.mask.from_surface(obst.visible_zone)
                off_x = obst.x - self.rect.x
                off_y = obst.y - self.rect.y
                if self.mask.overlap(mask, (off_x, off_y)):
                    pygame.draw.circle(self.surf, 'green', (self.surf.get_width() // 2,
                                                            self.surf.get_height() // 2), self.surf.get_height() // 2)
                    break


class Projectile(Point):

    def __init__(self, x, y, dir, speed=7):
        super().__init__(x, y)

        if dir == 'left':
            self.vector = pygame.math.Vector2(-1, uniform(-.3, .3))
        elif dir == 'right':
            self.vector = pygame.math.Vector2(1, uniform(-.3, .3))
        elif dir == 'up':
            self.vector = pygame.math.Vector2(uniform(-.3, .3), -1)
        else:
            self.vector = pygame.math.Vector2(uniform(-.3, .3), 1)
        self.speed = speed

    def update(self):
        if self.vector.length():
            norm = self.vector.normalize()
            self.rect.move_ip(norm * self.speed)


class Shooter:

    def __init__(self, x, y):
        self.surf = pygame.Surface((50, 50))
        self.rect = self.surf.get_rect(topleft=(x, y))
        self.dir = 'left'

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.dir = 'left'
            self.rect.move_ip(-5, 0)
        if keys[pygame.K_d]:
            self.dir = 'right'
            self.rect.move_ip(5, 0)

        if keys[pygame.K_w]:
            self.dir = 'up'
            self.rect.move_ip(0, -5)

        if keys[pygame.K_s]:
            self.dir = 'down'
            self.rect.move_ip(0, 5)

    def draw(self, display: pygame.Surface):
        pygame.draw.rect(self.surf, 'black', self.rect)
        # if self.dir == 'up':
        #     pygame.draw.rect()
        display.blit(self.surf, self.rect)

    def shoot(self) -> Projectile:
        print('shot')
        return Projectile(*self.rect.center, self.dir)


walls = [Wall(randrange(100, 905, 5), randrange(100, 705, 5),
              width=randrange(50, 120, 5),
              height=randrange(50, 120, 5), movable=False) for
         j in range(randint(6, 10))] + [Vase(x := randrange(100, 905, 5), y := randrange(100, 705, 5),
                                             width=40, height=50, movable=True, ) for _ in range(randint(5, 7))]


# alpha = pygame.transform.scale(pygame.image.load('../images/miscellaneous/alpha.png'), (300, 300)).convert_alpha()
# alpha_pos = (100, 100)
# alpha_mask = pygame.mask.from_surface(alpha)


clock = pygame.time.Clock()
# proj = Point(randint(0, display_width), randint(0, display_height))

shooter = Shooter(randint(0, display_width), randint(0, display_height))

projectiles = []

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                projectiles.append(shooter.shoot())

    display.fill('gray')

    for obst in walls:
        obst.draw_object(display)

    # off_x, off_y = alpha_pos[0] - proj.rect.x, alpha_pos[1] - proj.rect.y
    # if proj.mask.overlap(alpha_mask, (off_x, off_y)):
    #     pygame.draw.circle(proj.surf, 'green', (proj.surf.get_width() // 2,
    #                                              proj.surf.get_height() // 2), proj.surf.get_height() // 2)
    # display.blit(alpha, alpha_pos)
    for proj in projectiles:
        proj.draw(display)

        proj.update()
        proj.collide(walls)

    shooter.draw(display)
    shooter.move()

    pygame.display.update()
    clock.tick(60)
