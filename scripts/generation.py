from classes.rooms import *


def generate_random_loot(classes: list[type], x, y, n=1):
    return [LyingItem(x, y, choice(classes)) for _ in range(n)]


class DungNode:

    def __init__(self, type: int):
        self.neighbours = set()
        self.comp = 0
        self.type = type


def create_dung_matr(dung_width, dung_length) -> list[list[DungNode]]:
    room_types = [0, 1, 1, 1, 1, 2, 2, 3]

    '''
    0 - none; 
    1 - common; 
    2 - storage (with crates);
    3 - shop;
    4 - boss room
    '''
    dung = [[DungNode(-1) for _ in range(dung_length + 2)]] + \
           [[DungNode(-1)] + [DungNode(choice(room_types)) for _ in range(dung_length)
                              ] + [DungNode(-1)] for __ in range(dung_width)] \
           + [[DungNode(-1) for _ in range(dung_length + 2)]]
    b_r, b_c = randint(1, dung_width - 1), randint(1, dung_length - 1)
    dung[b_r][b_c].type = 4
    return dung


def find_neigh(matr: list[list[DungNode]]) -> list[list[DungNode]]:
    for i in range(1, len(matr) - 1):
        for j in range(1, len(matr[0]) - 1):
            if matr[i][j].type > 0:
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    create_entr = randint(0, 2)
                    if create_entr and matr[i + dx][j + dy].type > 0:
                        matr[i + dx][j + dy].neighbours.add((i, j))
                        matr[i][j].neighbours.add((i + dx, j + dy))

    return matr


def create_connected_dung(dung_width, dung_length) -> list[list[DungNode]]:
    def DFS(xv: int, yv: int, cur_comp):
        nonlocal dung_map
        dung_map[xv][yv].comp = cur_comp
        for xu, yu in dung_map[xv][yv].neighbours:
            if dung_map[xu][yu].comp == 0 and dung_map[xu][yu].type > 0:
                DFS(xu, yu, cur_comp)

    connected_dung = False
    gens = 0

    while not connected_dung:
        gens += 1
        connected_dung = True
        dung_map = find_neigh(create_dung_matr(dung_width, dung_length))
        cur_comp = 1

        for i in range(1, len(dung_map) - 1):
            for j in range(1, len(dung_map[0]) - 1):
                if dung_map[i][j].type > 0 and dung_map[i][j].comp == 0:
                    DFS(i, j, cur_comp)
                    cur_comp += 1
            if cur_comp > 2:
                connected_dung = False
                break
        if cur_comp > 2:
            connected_dung = False
    print(gens)

    return dung_map


room_types = ['node', 'common', 'storage', 'shop nowalls friendly', 'boss']


def generate_room(x, y, dung_matr: list[list[DungNode]]) -> Room:
    room_width, room_height = round(uniform(1, 1.5) * display_width), \
                              round(uniform(1, 1.5) * display_height)

    enters = []
    walls = []
    cont = []
    drops = []
    entities = []
    cur_node = dung_matr[x][y]
    room_type = room_types[cur_node.type].split()

    nodes = [[MyNode(j * grid_size, i * grid_size, grid_size, grid_size)
              for j in range(ceil(room_width / grid_size))]
             for i in range(ceil(room_height / grid_size))]

    if (x - 1, y) in cur_node.neighbours:
        walls.append(Wall(0, 0, width=randint(room_width // 2 - 250, room_width // 2 - 100),
                          height=randint(50, 100)))
        walls.append(Wall(wall_x := randint(room_width // 2 + 150, room_width // 2 + 220), 0,
                          room_width - wall_x, randint(50, 100)))
        enters.append('up')
    else:
        walls.append(Wall(0, 0, room_width, randint(50, 100)))

    if (x, y - 1) in cur_node.neighbours:
        walls.append(Wall(0, 0, width=randint(50, 100),
                          height=randint(room_height // 2 - 250, room_height // 2 - 100)))
        walls.append(Wall(0, wall_y := randint(room_height // 2 + 150, room_height // 2 + 220),
                          randint(50, 100), room_height - wall_y))
        enters.append('left')
    else:
        walls.append(Wall(0, 0, randint(50, 100), room_height))

    if (x + 1, y) in cur_node.neighbours:
        walls.append(Wall(0, wall_y := randint(room_height - 100, room_height - 50),
                          randint(room_width // 2 - 250, room_width // 2 - 100),
                          room_height - wall_y))
        walls.append(
            Wall(wall_x := randint(room_width // 2 + 150, room_width // 2 + 220),
                 wall_y := randint(room_height - 100, room_height - 50),
                 width=room_width - wall_x, height=room_height - wall_y))
        enters.append('down')
    else:
        walls.append(Wall(0, wall_y := randint(room_height - 100, room_height - 50), room_width,
                          room_height - wall_y))

    if (x, y + 1) in cur_node.neighbours:
        walls.append(Wall(randint(room_width - 100, room_width - 50), 0, width=room_width - x,
                          height=randint(room_height // 2 - 250, room_height // 2 - 100)))
        walls.append(Wall(wall_x := randint(room_width - 100, room_width - 50),
                          wall_y := randint(room_height // 2 + 150, room_height // 2 + 220),
                          width=room_width - wall_x, height=room_height - wall_y))
        enters.append('right')
    else:
        walls.append(
            Wall(wall_x := randint(room_width - 100, room_width - 50), 0, room_width - wall_x,
                 room_height))
    if 'nowalls' not in room_type:
        walls += [Wall(randrange(100, room_width - 100, 5), randrange(100, room_height - 100, 5),
                   width=randrange(50, 120, 5),
                   height=randrange(50, 100, 5), movable=False) for
              _ in range(round(randint(5, 8) * (room_height * room_width /
                                                (display_width * display_height))))]

        for node_l in range(len(nodes)):
            for node in nodes[node_l]:
                node.collide(walls)

    for _ in range(round(randint(2, 4) * (room_height * room_width /
                                          (display_width * display_height)))):
        while True:
            x, y = randrange(100, room_width - 100, 5), randrange(100, room_height - 100, 5)
            width, height = 40, 45
            x_n, y_n = (x + width // 2) // grid_size, (y + height) // grid_size
            if nodes[y_n][x_n].status:
                cont.append(Vase(x, y, width, height, movable=True, health=10,
                                 container=generate_random_loot([Potion, GoldCoin, SilverCoin], wall_x, wall_y,
                                                                n=randint(1, 3))))
                break

    for node_l in range(len(nodes)):
        for node in nodes[node_l]:
            node.collide(walls)

    if room_type[0] == 'storage':
        for _ in range(round(randint(2, 4) * (room_height * room_width /
                                              (display_width * display_height)))):
            while True:
                x, y = randrange(100, room_width - 100, 5), randrange(100, room_height - 100, 5)
                width, height = randint(45, 80), randint(45, 80)
                x_n, y_n = (x + width // 2) // grid_size, (y + height) // grid_size
                if nodes[y_n][x_n].status:
                    cont.append(Crate(x, y, width, height, movable=True, health=10,
                                      container=generate_random_loot([Knife, GoldCoin, SilverCoin, Helmet], wall_x,
                                                                     wall_y,
                                                                     n=randint(2, 3))))
                    break

        for node_l in range(len(nodes)):
            for node in nodes[node_l]:
                node.collide(walls)

    if 'friendly' not in room_type:
        entities = NPC.produce_NPC(randint(2, 4), nodes, room_width, room_height) \
                   + Hostile.produce_Hostiles(randint(2, 4), nodes, room_width, room_height)
        for entity in entities:
            entity.loot = generate_random_loot([SilverCoin, GoldCoin, Potion], 0, 0, n=randint(1, 2))
            if not isinstance(entity.weapon, Fist):
                entity.loot.append(LyingItem(0, 0, type(entity.weapon)))
            entity.loot += [LyingItem(0, 0, Experience) for _ in range(randint(2, 3))]

    if room_type[0] == 'shop':
        n_goods = randint(3, 5)
        for x in range(room_width // 3, room_width * 2 // 3 + 1,
                       room_width // 3 // n_goods):
            drops.append(SellingGood(x, display_height * 2 // 3,
                              choice([Knife, GoldCoin, SilverCoin, Helmet, Potion]), randint(1, 10)))
        entities.append(Trader(room_width // 2, display_height // 2, 90, 108, 100, 'left', speed=0, loot=[]))

    return (Room if room_type[0] != 'boss' else BossRoom)(walls, cont, drops, entities, [],
                enters, nodes, choice(['stone', 'wooden']),
                (room_width, room_height), type=room_type[0])


def generate_dungeons(dung_width, dung_length) -> tuple[dict[int, Room], int, int, int]:
    dung_matr = create_connected_dung(dung_width, dung_length)
    for i in dung_matr:
        print(*[str((j.type, j.comp)).ljust(5) for j in i])
    rooms = {}
    for i in range(1, dung_width + 1):
        for j in range(1, dung_length + 1):
            cur_ind = (i - 1) * dung_length + j
            if dung_matr[i][j].type > 0:
                rooms[cur_ind] = generate_room(i, j, dung_matr)
    cur_room = choice(list(rooms.keys()))
    return rooms, cur_room, dung_width, dung_length
