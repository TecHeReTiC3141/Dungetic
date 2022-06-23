from classes.surrounding import *

class Room:

    # TODO set type annotations everywhere it's necessary
    def __init__(self, obst_list: list[Wall], containers: list[Wall], drops: list[Drop],
                 entities_list: list[NPC], projectiles: list[Projectile], entrances, nodes: list[list[MyNode]],
                 floor: str, size: tuple,type: str = 'common'):
        self.obst_list = obst_list
        self.containers = containers
        self.drops = drops
        self.decors = []
        self.entities_list = entities_list

        self.projectiles = projectiles

        self.entrances = entrances
        self.is_safe = len([i for i in self.entities_list if isinstance(i, Hostile)]) == 0
        self.floor = pygame.transform.scale(stone_floor if floor == 'stone' else wooden_floor, size)
        self.floor_name = floor
        self.visited = True
        self.type = type
        self.width, self.height = size

        self.nodes = nodes
        for node_l in range(len(self.nodes)):
            for node in self.nodes[node_l]:
                node.collide(self.obst_list + self.containers)
        'grid for pathfinding'
        self.grid = Grid(matrix=[[self.nodes[i][j].status for j in range(ceil(self.width / grid_size))]
                                 for i in range(ceil(self.height / grid_size))])

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
            elif isinstance(entity, Trader):
                entity.target = target

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
                        if isinstance(cont, Container) and hasattr(cont, 'cur_rect'):
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
        state.pop('floor')
        state['decors'] = []
        return state

    def __setstate__(self, state):
        self.floor = pygame.transform.scale(stone_floor if state['floor_name'] == 'stone'
                                            else wooden_floor,
                                            (state['width'], state['height']))
        self.__dict__.update(state)


class BossRoom(Room):

    def clear(self):
        super().clear()
        if self.is_safe and \
                not hasattr(self, 'trapdoor'):
            self.trapdoor: TrapDoor = TrapDoor(display_width // 2 - 30, display_height // 3)

    def physics(self, heretic: Heretic):
        super().physics(heretic)
        if self.is_safe and self.trapdoor.collide(heretic):
            return True

    def draw_object(self, surface: pygame.Surface, tick: int, show_grid: bool):
        surface.blit(self.floor, (0, 0))
        if hasattr(self, 'trapdoor'):
            self.trapdoor.draw_object(surface)
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
