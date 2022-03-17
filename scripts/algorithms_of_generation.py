from classes.surrounding import *


def generate_random_loot(classes: list[type], x, y):
    cl = random.choice(classes)
    return LyingItem(x, y, cl)


def generate_room(cur_ind, dung_width, dung_length) -> Room:
    ways = random.sample(['down', 'right'], random.randint(1, 2))
    enters = []
    walls = []
    cont = []
    entities = NPC.produce_NPC(random.randint(2, 5))
    if cur_ind > dung_length and 'down' in rooms[cur_ind - dung_length].entrances:
        walls.append(Wall(0, 0, width=random.randint(display_width // 2 - 250, display_width // 2 - 100),
                          height=random.randint(50, 100)))
        walls.append(Wall(x := random.randint(display_width // 2 + 150, display_width // 2 + 220), y := 0,
                          width := display_width - x, height := random.randint(50, 100)))
        enters.append('up')
    else:
        walls.append(Wall(0, 0, width := display_width, height := random.randint(50, 100)))

    if cur_ind % dung_length != 1 and 'right' in rooms[cur_ind - 1].entrances:
        walls.append(Wall(0, 0, width=random.randint(50, 100),
                          height=random.randint(display_height // 2 - 250, display_height // 2 - 100)))
        walls.append(Wall(0, y := random.randint(display_height // 2 + 150, display_height // 2 + 220),
                          width := random.randint(50, 100), height := display_height - y))
        enters.append('left')
    else:
        walls.append(Wall(0, 0, width=random.randint(50, 100), height=1000))

    if 'down' in ways and cur_ind < (dung_width - 1) * dung_length:
        walls.append(Wall(0, y := random.randint(display_height - 100, display_height - 50),
                          width := random.randint(display_width // 2 - 250, display_width // 2 - 100),
                          height := display_height - y))
        walls.append(
            Wall(x := random.randint(display_width // 2 + 150, display_width // 2 + 220),
                 y := random.randint(display_height - 100, display_height - 50),
                 width=display_width - x, height=display_height - y))
        enters.append('down')
    else:
        walls.append(Wall(0, y := random.randint(display_height - 100, display_height - 50), width := display_width,
                          height := display_height - y))

    if 'right' in ways and cur_ind % dung_length:
        walls.append(Wall(x := random.randint(display_width - 100, display_width - 50), 0, width=display_width - x,
                          height=random.randint(display_height // 2 - 250, display_height // 2 - 100)))
        walls.append(Wall(x := random.randint(display_width - 100, display_width - 50),
                          y := random.randint(display_height // 2 + 150, display_height // 2 + 220),
                          width=display_width - x, height=display_height - y))
        enters.append('right')
    else:
        walls.append(
            Wall(x := random.randint(display_width - 100, display_width - 50), y := 0, width := display_width - x,
                 height := display_height))

    walls += [Wall(random.randrange(100, 905, 5), random.randrange(100, 705, 5),
                   width=random.randrange(50, 120, 5),
                   height=random.randrange(50, 120, 5), movable=False) for
              j in range(random.randint(5, 10))]
    cont += [Vase(x := random.randrange(100, 905, 5), y := random.randrange(100, 705, 5),
                  width=40, height=45, movable=True, health=15,
                  container=generate_random_loot([Knife], x, y)) for j in range(random.randint(3, 5))]
    if not enters:
        enters = [dir for dir in directions if dir not in ways]

    return Room(walls, cont, entities, enters, floor=random.choice(['stone', 'wooden']))


def generate_dungeons() -> dict[int, Room]:
    global rooms
    for i in range(dung_width):
        for j in range(1, dung_length + 1):
            cur_ind = i * dung_length + j
            rooms[cur_ind] = generate_room(cur_ind, dung_width, dung_length)
    return rooms
