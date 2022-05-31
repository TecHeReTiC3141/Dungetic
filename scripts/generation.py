from classes.surrounding import *


def generate_random_loot(classes: list[type], x, y, n=1):
    return [LyingItem(x, y, choice(classes)) for _ in range(n)]


class DungNode:

    def __init__(self, type: int):
        self.neighbours = set()
        self.comp = 0
        self.type = type


def create_dung_matr(dung_width, dung_length) -> list[list[DungNode]]:
    room_types = [0, 1, 1, 1, 2]
    return [[DungNode(-1) for _ in range(dung_length + 2)]] + \
           [[DungNode(-1)] + [DungNode(choice(room_types)) for _ in range(dung_length)
                              ] + [DungNode(-1)] for __ in range(dung_width)] \
           + [[DungNode(-1) for _ in range(dung_length + 2)]]


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


room_types = ['node', 'common', 'storage']


def generate_room(x, y, dung_matr: list[list[DungNode]]) -> Room:
    room_width, room_height = round(uniform(1, 1.5) * display_width), \
                              round(uniform(1, 1.5) * display_height)

    enters = []
    walls = []
    cont = []
    entities = NPC.produce_NPC(randint(1, 3)) \
               + Hostile.produce_Hostiles(randint(2, 3))
    cur_node = dung_matr[x][y]
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
        walls.append(Wall(0, 0, width=randint(50, 100), height=1000))

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

    walls += [Wall(randrange(100, 1205, 5), randrange(100, 865, 5),
                   width=randrange(50, 120, 5),
                   height=randrange(50, 100, 5), movable=False) for
              _ in range(randint(5, 10))]

    cont += [Vase(wall_x := randrange(100, 905, 5), wall_y := randrange(100, 705, 5),
                  width=40, height=45, movable=True, health=10,
                  container=generate_random_loot([Potion, GoldCoin, SilverCoin], wall_x, wall_y, n=randint(1, 3)))
             for _ in range(randint(3, 5))]

    if room_types[cur_node.type] == 'storage':
        cont += [Crate(wall_x := randrange(100, 905, 5), wall_y := randrange(100, 705, 5),
                       width=randint(45, 80), height=randint(45, 80), movable=True, health=10,
                       container=generate_random_loot([Knife, GoldCoin, SilverCoin, Helmet], wall_x, wall_y,
                                                      n=randint(2, 3)))
                 for _ in range(randint(3, 5))]

    for entity in entities:
        entity.loot = generate_random_loot([SilverCoin, GoldCoin, Potion], 0, 0, n=randint(1, 2))
        if not isinstance(entity.weapon, Fist):
            entity.loot.append(LyingItem(0, 0, type(entity.weapon)))
        entity.loot += [LyingItem(0, 0, Experience) for _ in range(randint(2, 3))]

    return Room(walls, cont, entities, [], enters, choice(['stone', 'wooden']),
                (room_width, room_height), type=room_types[cur_node.type])


def generate_dungeons(dung_width, dung_length) -> dict[int, Room]:
    dung_matr = create_connected_dung(dung_width, dung_length)
    for i in dung_matr:
        print(*[str((j.type, j.comp)).ljust(5) for j in i])
    rooms = {}
    for i in range(1, dung_width + 1):
        for j in range(1, dung_length + 1):
            cur_ind = i * dung_length + j
            if dung_matr[i][j].type > 0:
                rooms[cur_ind] = generate_room(i, j, dung_matr)

    return rooms
