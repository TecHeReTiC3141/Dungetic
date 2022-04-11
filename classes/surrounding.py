from math import *
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
        self.phys_rect = pygame.Rect(x, y, width, height)
        self.inner_phys_rect = pygame.Rect(x + 5, y + 5,
                                           max(width - 10, 10), max(height - 10, 10))
        self.outer_phys_rect = pygame.Rect(x - 10, y - 10, width + 20, height + 20)
        self.visible_zone = pygame.Surface((width, height))
        self.visible_zone.set_colorkey('#FFFFFF')
        self.collised = collised
        self.movable = movable
        super().__init__(*args)

    def draw_object(self, display: pygame.Surface):

        # pygame.draw.rect(display, ('#CCCCCC'), self.outer_phys_rect)
        pygame.draw.rect(self.visible_zone, (70, 70, 70), (0, 0, self.width, self.height))

        display.blit(self.visible_zone, self.phys_rect)
        # pygame.draw.rect(display, ('#AAAAAA'), self.inner_phys_rect)

    def collide(self, entities: list[Heretic], direction: str):

        for entity in entities:
            if isinstance(entity, NPC):
                if entity.cur_rect.collidelist([self.outer_phys_rect, self.phys_rect]) == -1:
                    for direct in entity.collised_walls:
                        if entity.collised_walls[direct] == self:
                            entity.speed_directions[direct] = 5
                            entity.collised_walls[direct] = None
                move = [0, 0]
                if self.phys_rect.colliderect(entity.cur_rect):

                    if self.phys_rect.left + 15 >= entity.cur_rect.right:
                        move[0] = max(5 - self.weight, 1)
                        entity.collised_walls['right'] = self
                        if not self.movable:
                            entity.speed_directions['right'] = 0
                        else:
                            entity.speed_directions['right'] = max(5 - self.weight, 1)

                    if self.phys_rect.right - 15 <= entity.cur_rect.left:
                        move[0] = -max(5 - self.weight, 1)
                        entity.collised_walls['left'] = self
                        if not self.movable:
                            entity.speed_directions['left'] = 0
                        else:
                            entity.speed_directions['left'] = max(5 - self.weight, 1)
                    if self.phys_rect.top + 15 >= entity.cur_rect.bottom:
                        move[1] = max(5 - self.weight, 1)
                        entity.collised_walls['down'] = self
                        if not self.movable:
                            entity.speed_directions['down'] = 0
                        else:
                            entity.speed_directions['down'] = max(5 - self.weight, 1)

                    if self.phys_rect.bottom - 15 <= entity.cur_rect.top:
                        move[1] = -max(5 - self.weight, 1)
                        entity.collised_walls['up'] = self
                        if not self.movable:
                            entity.speed_directions['up'] = 0
                        else:
                            entity.speed_directions['up'] = max(5 - self.weight, 1)
            else:
                if entity.cur_rect.colliderect(self.phys_rect):
                    if direction == 'hor':
                        # left side
                        if entity.cur_rect.right >= self.phys_rect.left >= entity.prev_rect.right:
                            entity.cur_rect.right = self.phys_rect.left
                            move[0] = max(5 - self.weight, 1)
                        # right side
                        elif entity.cur_rect.left <= self.phys_rect.right <= entity.prev_rect.left:
                            entity.cur_rect.left = self.phys_rect.right
                            move[0] = -max(5 - self.weight, 1)
                    else:
                        # top side
                        if entity.cur_rect.bottom >= self.phys_rect.top >= entity.prev_rect.bottom:
                            entity.cur_rect.bottom = self.phys_rect.top
                            move[1] = max(5 - self.weight, 1)
                        # bottom side
                        elif entity.cur_rect.top <= self.phys_rect.bottom <= entity.prev_rect.top:
                            entity.cur_rect.top = self.phys_rect.bottom
                            move[1] = -max(5 - self.weight, 1)

            if self.movable:
                self.phys_rect.move_ip(*move)
                self.inner_phys_rect.move_ip(*move)
                self.outer_phys_rect.move_ip(*move)


class Vase(Wall, Breakable, Container):

    def __init__(self, x, y, width, height, collised=False, movable=False, health=120, container=None):
        super().__init__(x, y, width, height, collised, movable, health, container)
        self.sprite = pygame.image.load('../images/Vase1.png').convert_alpha()
        self.sprite.set_colorkey('#FFFFFF')

    def draw_object(self, display: pygame.Surface):
        self.visible_zone.fill('#FFFFFF')
        display.blit(self.visible_zone, self.phys_rect)
        display.blit(self.sprite, self.phys_rect)
        return self.visible_zone


class MyNode:
    '''
    A class for nodes for pathfinding grid
    '''

    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.status = 1

    def collide(self, obsts: list[Wall]):
        for wall in obsts:
            if wall.outer_phys_rect.colliderect(self.rect):
                self.status = 0
                break

    def draw_object(self, display):
        pygame.draw.rect(display, [RED, BLUE][self.status], self.rect)

        # drawing the grid
        pygame.draw.line(display, BLACK, self.rect.topleft, (display_width, self.rect.top))
        pygame.draw.line(display, BLACK, self.rect.bottomleft, (display_width, self.rect.bottom))
        pygame.draw.line(display, BLACK, self.rect.topleft, (self.rect.left, display_height))
        pygame.draw.line(display, BLACK, self.rect.topright, (self.rect.right, display_height))


class Room:

    def __init__(self, obst_list: list[Wall], containers: list[Wall],
                 entities_list: list[NPC], entrances, floor: str):
        self.obst_list = obst_list
        self.containers = containers
        self.drops = []
        self.decors = []
        self.entities_list = entities_list
        self.entrances = entrances
        self.is_safe = len([i for i in self.entities_list if isinstance(i, Hostile)]) == 0
        self.floor = c_a_s.stone_floor if floor == 'stone' else c_a_s.wooden_floor
        self.visited = True
        self.nodes = [
            [MyNode(j * grid_size, i * grid_size, grid_size, grid_size) for j in range(ceil(display_width / grid_size))]
            for i in range(ceil(display_height / grid_size))]
        for node_l in range(len(self.nodes)):
            for node in self.nodes[node_l]:
                node.collide(self.obst_list)
        'grid for pathfinding'
        self.grid = Grid(matrix=[[self.nodes[i][j].status for j in range(ceil(display_width / grid_size))]
                                 for i in range(ceil(display_height / grid_size))])

    def draw_object(self, surface: pygame.Surface, show_grid: bool):
        surface.blit(self.floor, (0, 0))
        if show_grid:
            self.draw_grid(surface)
            for entity in self.entities_list:
                if len(entity.path) > 1:
                    pygame.draw.lines(surface, BLACK, False, entity.path, width=10)

        for wall in self.obst_list + self.containers + self.drops:
            wall.draw_object(surface)
        for entity in self.entities_list:
            entity.draw_object(surface)
        for decor in self.decors:
            if isinstance(decor, Decor):
                if isinstance(decor, Banner):
                    decor.draw_object(surface)
                elif isinstance(decor, Particle):
                    decor.draw_object(surface)
                    decor.move()


    def draw_grid(self, surface):
        for node_l in self.nodes:
            for node in node_l:
                node.draw_object(surface)

    def physics(self, heretic: Heretic):
        for wall in self.obst_list + self.containers:
            wall.collide(self.entities_list + [heretic], 'hor')
            wall.collide(self.entities_list + [heretic], 'vert')
        for drop in self.drops:
            drop.collide([heretic])

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
            if isinstance(entity, Hostile):
                entity.hostile_exist()
            else:
                entity.passive_exist()
            entity.update(tick)

    def clear(self):
        sorted_conts = []
        for cont in self.containers:
            if isinstance(cont, Breakable):
                if cont.is_broken:
                    loot = cont.get_broken()
                    for loo in loot:
                        if isinstance(cont, Container):
                            loo.rect.topleft = cont.phys_rect.topleft
                            self.drops.append(loo)
                else:
                    sorted_conts.append(cont)

        self.containers = sorted_conts.copy()

        alive = []
        for entity in self.entities_list:
            if entity.dead:
                for loot in entity.loot:
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
