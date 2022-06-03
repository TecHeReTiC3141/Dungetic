from math import *

import pygame

from classes.drops import *
from classes.decors import *


class Container:
    # interface for all game containers

    def __init__(self, content: list):
        self.content = content


class Breakable:
    def __init__(self, health, *args):
        self.health = health
        self.is_broken = False
        super().__init__(*args)

    def get_broken(self):
        self.is_broken = True
        if isinstance(self, Container):
            return self.content


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
        pygame.draw.rect(self.sprite, (70, 70, 70), (0, 0, self.width, self.height), border_radius=8)

        self.mask = pygame.mask.from_surface(self.sprite)
        self.collised = collised
        self.movable = movable
        super().__init__(*args)

    def draw_object(self, display: pygame.Surface):

        # pygame.draw.rect(display, ('#CCCCCC'), self.outer_phys_rect)
        pygame.draw.rect(self.sprite, (70, 70, 70), (0, 0, self.width, self.height), border_radius=8)

        display.blit(self.sprite, self.cur_rect)
        # pygame.draw.rect(display, ('#AAAAAA'), self.inner_phys_rect)

    def collide(self, entities: list[Heretic], direction: str, walls_list: list):

        for entity in entities:
            if isinstance(entity, NPC):
                if entity.cur_rect.collidelist([self.outer_phys_rect, self.cur_rect]) == -1:
                    for direct in entity.collised_walls:
                        if entity.collised_walls[direct] == self:
                            entity.speed_directions[direct] = 5
                            entity.collised_walls[direct] = None
                move = [0, 0]
                if self.cur_rect.colliderect(entity.cur_rect):

                    if self.cur_rect.left + 15 >= entity.cur_rect.right:
                        move[0] = max(5 - self.weight, 1)
                        entity.collised_walls['right'] = self
                        if not self.movable:
                            entity.speed_directions['right'] = 0
                        else:
                            entity.speed_directions['right'] = max(5 - self.weight, 1)

                    if self.cur_rect.right - 15 <= entity.cur_rect.left:
                        move[0] = -max(5 - self.weight, 1)
                        entity.collised_walls['left'] = self
                        if not self.movable:
                            entity.speed_directions['left'] = 0
                        else:
                            entity.speed_directions['left'] = max(5 - self.weight, 1)
                    if self.cur_rect.top + 15 >= entity.cur_rect.bottom:
                        move[1] = max(5 - self.weight, 1)
                        entity.collised_walls['down'] = self
                        if not self.movable:
                            entity.speed_directions['down'] = 0
                        else:
                            entity.speed_directions['down'] = max(5 - self.weight, 1)

                    if self.cur_rect.bottom - 15 <= entity.cur_rect.top:
                        move[1] = -max(5 - self.weight, 1)
                        entity.collised_walls['up'] = self
                        if not self.movable:
                            entity.speed_directions['up'] = 0
                        else:
                            entity.speed_directions['up'] = max(5 - self.weight, 1)
            else:
                if entity.cur_rect.colliderect(self.cur_rect):
                    if direction == 'hor':
                        # left side
                        if entity.cur_rect.right >= self.cur_rect.left >= entity.prev_rect.right:
                            entity.cur_rect.right = self.cur_rect.left
                            move[0] = max(5 - self.weight, 1)
                        # right side
                        elif entity.cur_rect.left <= self.cur_rect.right <= entity.prev_rect.left:
                            entity.cur_rect.left = self.cur_rect.right
                            move[0] = -max(5 - self.weight, 1)
                    else:
                        # top side
                        if entity.cur_rect.bottom >= self.cur_rect.top >= entity.prev_rect.bottom:
                            entity.cur_rect.bottom = self.cur_rect.top
                            move[1] = max(5 - self.weight, 1)
                        # bottom side
                        elif entity.cur_rect.top <= self.cur_rect.bottom <= entity.prev_rect.top:
                            entity.cur_rect.top = self.cur_rect.bottom
                            move[1] = -max(5 - self.weight, 1)
            # TODO update physics for all entities
            if self.movable:
                self.prev_rect = self.cur_rect.copy()

                self.cur_rect.move_ip(*move)
                self.inner_phys_rect.move_ip(*move)
                self.outer_phys_rect.move_ip(*move)
                for wall in walls_list:
                    if self.cur_rect.colliderect(wall.cur_rect):
                        if direction == 'hor':
                            # left side
                            if self.cur_rect.right >= wall.cur_rect.left >= self.prev_rect.right:
                                if not wall.movable:
                                    self.cur_rect.right = wall.cur_rect.left
                                else:
                                    wall.cur_rect.left = self.cur_rect.right

                            # right side
                            elif self.cur_rect.left <= wall.cur_rect.right <= self.prev_rect.left:
                                if not wall.movable:
                                    self.cur_rect.left = wall.cur_rect.right
                                else:
                                    wall.cur_rect.right = self.cur_rect.left

                        else:
                            # top side
                            if self.cur_rect.bottom >= wall.cur_rect.top >= self.prev_rect.bottom:
                                if not wall.movable:
                                    self.cur_rect.bottom = wall.cur_rect.top
                                else:
                                    wall.cur_rect.top = self.cur_rect.bottom

                            # bottom side
                            elif self.cur_rect.top <= wall.cur_rect.bottom <= self.prev_rect.top:
                                if not wall.movable:
                                    self.cur_rect.top = wall.cur_rect.bottom
                                else:
                                    wall.cur_rect.bottom = self.cur_rect.top


    def __getstate__(self):
        state = self.__dict__.copy()
        vis_zone, sprite = state.pop('visible_zone'), state.pop('sprite')
        state['visible_zone'] = (pygame.image.tostring(vis_zone, 'RGB'), vis_zone.get_size())
        state['sprite'] = (pygame.image.tostring(sprite, 'RGB'), sprite.get_size())

        return state

    def __setstate__(self, state):
        state['visible_zone'] = pygame.image.fromstring(*state['visible_zone'], 'RGB')
        state['sprite'] = pygame.image.fromstring(*state['sprite'], 'RGB')
        self.__dict__.update(state)


class Vase(Wall, Breakable, Container):

    def __init__(self, x, y, width, height, collised=False, movable=False, health=120, container=None):
        super().__init__(x, y, width, height, collised, movable, health, container)

        self.sprite = pygame.image.load('../images/surroundings/Vase1.png').convert_alpha()
        self.visible_zone = pygame.Surface(self.sprite.get_size())

        self.mask = pygame.mask.from_surface(self.sprite)
        self.cur_rect.update(*self.cur_rect.topleft, *self.sprite.get_size())
        self.sprite.set_colorkey('#FFFFFF')
        self.visible_zone.set_colorkey('White')

    def draw_object(self, display: pygame.Surface):
        self.visible_zone.fill('#FFFFFF')
        self.visible_zone.blit(self.sprite, (0, 0))
        display.blit(self.visible_zone, self.cur_rect)
        return self.visible_zone


class Crate(Vase):

    def __init__(self, x, y, width, height, collised=False,
                 movable=False, health=120, container=None):
        super().__init__(x, y, width, height, collised,
                         movable, health, container)
        self.sprite = pygame.transform.scale(pygame.image.load('../images/surroundings/crate.png'), (width, height))
        self.visible_zone = pygame.Surface(self.sprite.get_size())
        self.visible_zone.set_colorkey('White')
        self.cur_rect.update(*self.cur_rect.topleft, width, height)


class MyNode:

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.status = 1

    def collide(self, obsts: list[Wall]):
        for wall in obsts:
            if wall.outer_phys_rect.colliderect(self.rect):
                self.status = 0
                break
        else:
            self.status = 1

    def draw_object(self, display):
        pygame.draw.rect(display, [RED, BLUE][self.status], self.rect)

        # drawing the grid
        pygame.draw.line(display, BLACK, self.rect.topleft, (display_width, self.rect.top))
        pygame.draw.line(display, BLACK, self.rect.bottomleft, (display_width, self.rect.bottom))
        pygame.draw.line(display, BLACK, self.rect.topleft, (self.rect.left, display_height))
        pygame.draw.line(display, BLACK, self.rect.topright, (self.rect.right, display_height))


class Room:

    def __init__(self, obst_list: list[Wall], containers: list[Wall],
                 entities_list: list[NPC], projectiles: list[Projectile], entrances, floor: str, size: tuple,type: str = 'common'):
        self.obst_list = obst_list
        self.containers = containers
        self.drops = []
        self.decors = []
        self.entities_list = entities_list
        self.projectiles = projectiles

        self.entrances = entrances
        self.is_safe = len([i for i in self.entities_list if isinstance(i, Hostile)]) == 0
        self.floor = pygame.transform.scale(stone_floor if floor == 'stone' else wooden_floor, size)
        self.visited = True
        self.type = type
        self.width, self.height = size

        self.nodes = [
            [MyNode(j * grid_size, i * grid_size, grid_size, grid_size) for j in range(ceil(self.width / grid_size))]
            for i in range(ceil(self.height / grid_size))]
        for node_l in range(len(self.nodes)):
            for node in self.nodes[node_l]:
                node.collide(self.obst_list + self.containers)
        'grid for pathfinding'
        self.grid = Grid(matrix=[[self.nodes[i][j].status for j in range(ceil(self.width / grid_size))]
                                 for i in range(ceil(self.height / grid_size))])

        # TODO make Room object serializable !!!

    def draw_object(self, surface: pygame.Surface, tick: int, show_grid: bool):
        surface.blit(self.floor, (0, 0))
        if show_grid:
            self.draw_grid(surface)
            for entity in self.entities_list:
                if len(entity.path) > 1:
                    pygame.draw.lines(surface, BLACK, False, entity.path, width=10)

        for wall in self.obst_list + self.containers + self.drops:
            wall.draw_object(surface)

        for decor in self.decors:
            if isinstance(decor, Decor):
                if isinstance(decor, Particle) and decor.type == 'background':
                    decor.draw_object(surface)
                    decor.move(tick)

        for entity in self.entities_list:
            entity.draw_object(surface)

        if self.projectiles.count(None):
            logging.warning(f'{self.projectiles}')

        for proj in self.projectiles:
            proj.draw_object(surface)

        for decor in self.decors:
            if isinstance(decor, Decor):
                if isinstance(decor, Banner):
                    decor.draw_object(surface)
                elif isinstance(decor, Particle) and decor.type != 'background':
                    decor.draw_object(surface)
                    decor.move(tick)

    def draw_grid(self, surface):
        for node_l in self.nodes:
            for node in node_l:
                node.draw_object(surface)

    def check_drops(self, mouse: tuple, entities: list[Heretic]):
        for drop in self.drops:
            drop.collide(entities, mouse)

    def physics(self, heretic: Heretic):
        for wall in self.obst_list + self.containers:
            wall.collide(self.entities_list + [heretic], 'hor', self.obst_list + self.containers)
            wall.collide(self.entities_list + [heretic], 'vert', self.obst_list + self.containers)

        for drop in self.drops:
            drop.collide([heretic])

        # Fix bug connected with projectiles
        for proj in self.projectiles:
            proj.move()
            for obst in self.obst_list + self.containers:
                if proj.rect.colliderect(obst.cur_rect):
                    off_x = obst.cur_rect.x - proj.rect.x
                    off_y = obst.cur_rect.y - proj.rect.y

                    if proj.mask.overlap(obst.mask, (off_x, off_y)):
                        if obst.movable:
                            obst.cur_rect.move_ip(proj.vector * proj.damage)
                            obst.health -= proj.damage
                        proj.collided = True
                        break
            for ent in self.entities_list:
                if proj.rect.colliderect(ent.cur_rect):
                    ent.cur_rect.move_ip(proj.vector * proj.damage)
                    ent.actual_health -= proj.damage
                    proj.collided = True
                    break

        if not self.is_safe:
            for node_l in range(len(self.nodes)):
                for node in self.nodes[node_l]:
                    node.collide(self.obst_list + self.containers)

    def make_paths(self, target: Heretic):
        target.node = self.grid.node(*target.get_center_coord(True))
        for entity in self.entities_list:
            if isinstance(entity, Hostile):
                entity.target = [target]
                entity.node = self.grid.node(*entity.get_center_coord(True))
                entity.path, _ = PathFinder.find_path(entity.node, target.node, self.grid)
                entity.path = deque([(x * grid_size + grid_size // 2,
                                      y * grid_size + grid_size // 2) for x, y in entity.path])
                self.grid.cleanup()

    def life(self, tick: int):
        for entity in self.entities_list:
            blood_list = entity.exist()
            if blood_list:
                self.decors.extend(blood_list)

            entity.update(tick)

    def clear(self):
        sorted_conts = []
        for cont in self.containers:
            if isinstance(cont, Breakable):
                if cont.health <= 0:
                    loot = cont.get_broken()
                    for loo in loot:
                        if isinstance(cont, Container):
                            loo.rect.left = randint(cont.cur_rect.left, cont.cur_rect.centerx)
                            loo.rect.top = randint(cont.cur_rect.top, cont.cur_rect.centery)
                            self.drops.append(loo)
                else:
                    sorted_conts.append(cont)

        self.containers = sorted_conts.copy()

        alive = []
        for entity in self.entities_list:
            if entity.dead:
                for loot in entity.loot:
                    loot.rect.left = randint(entity.cur_rect.left, entity.cur_rect.right)
                    loot.rect.top = randint(entity.cur_rect.top, entity.cur_rect.bottom)
                    if isinstance(loot, Drop):
                        self.drops.append(loot)

            else:
                alive.append(entity)
        self.entities_list = alive.copy()

        new_decors = []
        for decor in self.decors:
            if isinstance(decor, Decor):
                if decor.life_time <= 0:
                    new = decor.delete()
                    if isinstance(new, Decor):
                        new_decors.append(new)
                else:
                    new_decors.append(decor)
        self.decors = new_decors.copy()

        if len([i for i in self.entities_list if isinstance(i, Hostile)]) == 0 and not self.is_safe:
            self.decors.append(Banner(display_width // 3, 20, 'The room was cleaned', 180))
        self.is_safe = len([i for i in self.entities_list if isinstance(i, Hostile)]) == 0

        self.drops = list(filter(lambda i: not i.picked,
                                 self.drops))

        self.projectiles = list(filter(lambda i: not i.collided,
                                       self.projectiles))

    def __getstate__(self):
        state = self.__dict__.copy()
        floor = state.pop('floor')
        state['floor'] = (pygame.image.tostring(floor, 'RGB'), floor.get_size())
        return state
