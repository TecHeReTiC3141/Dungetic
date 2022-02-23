from classes.Heretic import Heretic
from classes.entities import produce_NPC
from classes.interfaces import MapInter, Inventory
from classes.surrounding import Wall, Vase, Room
from scripts.constants_and_sources import *

print(*[''.join([str(i).rjust(3) for i in list(range(1 + dung_length * i, dung_length * (i + 1) + 1))]) for i in
        range(dung_width)], sep='\n')
pygame.mouse.set_visible(False)
'''
TODO:
Изменить систему столкновений со стенами. 550 - 600

'''

pygame.display.set_caption('Dungetic')

bullets_list = []

Map = MapInter((display_width, display_height))
Invent = Inventory((display_width, display_height))

heretic = Heretic(100, 100, 75, 100, 100, 'left',
                  [], location=random.randint(1, dung_width * dung_length))

stop = []

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
        walls.append(Wall(0, 0, width=random.randint(50, 100),
                          height=random.randint(display_height // 2 - 250, display_height // 2 - 100)))
        walls.append(Wall(0, y := random.randint(display_height // 2 + 150, display_height // 2 + 220),
                          width := random.randint(50, 100), height := display_height - y))
        enters.append('left')
    else:
        walls.append(Wall(0, 0, width=random.randint(50, 100), height=1000))

    if 'down' in ways and i < (dung_width - 1) * dung_length:
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

    if 'right' in ways and i % dung_length:
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
                   height=random.randrange(50, 120, 5), movable=True) for
              j in range(random.randint(5, 10))]
    walls += [Vase(random.randrange(100, 905, 5), random.randrange(100, 705, 5),
                   width=40, height=45, movable=True) for j in range(random.randint(3, 5))]
    if not enters:
        enters = [i for i in directions if i not in ways]
    entities_list = produce_NPC(random.randint(1, 3))
    rooms[i] = Room(walls, entities_list, enters, random.choice(['stone', 'wooden']))

# Кажется, после генерации следует проверить все стены на смежные переходы вложенным циклом !


collised_walls = {wall: [] for wall in rooms[curr_room].walls_list}

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
                            and heretic.x in wall.active_zone[0] and heretic.y in wall.active_zone[
                        1] and heretic.attack_time <= 0:
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
            heretic.left_stop = True

        if any([3 in collised_walls[wall], 4 in collised_walls[wall],
                5 in collised_walls[wall]]) and wall.x > heretic.x + 60:
            if wall.movable:
                wall.x += 1
                wall.active_zone = [list(range(wall.x - 100, wall.x + wall.width + 25)),
                                    list(range(wall.y - 100, wall.y + wall.height + 25))]
                wall.visible_zone = [list(range(wall.x, wall.x + wall.width)),
                                     list(range(wall.y, wall.y + wall.height))]
            heretic.right_stop = True
        if any([1 in collised_walls[wall], 2 in collised_walls[wall], 3 in collised_walls[wall]]) and wall.y + len(
                wall.visible_zone[1]) - 15 < heretic.y:
            if wall.movable:
                wall.y -= 1
                wall.active_zone = [list(range(wall.x - 100, wall.x + wall.width + 25)),
                                    list(range(wall.y - 100, wall.y + wall.height + 25))]
                wall.visible_zone = [list(range(wall.x, wall.x + wall.width)),
                                     list(range(wall.y, wall.y + wall.height))]
            heretic.up_stop = True
        if any([5 in collised_walls[wall], 6 in collised_walls[wall],
                7 in collised_walls[wall]]) and wall.y > heretic.y + 85:
            if wall.movable:
                wall.y += 1
                wall.active_zone = [list(range(wall.x - 100, wall.x + wall.width + 25)),
                                    list(range(wall.y - 100, wall.y + wall.height + 25))]
                wall.visible_zone = [list(range(wall.x, wall.x + wall.width)),
                                     list(range(wall.y, wall.y + wall.height))]
            heretic.down_stop = True

    if not current_interface:
        heretic.move()

    if current_interface == 'Inventory':
        Invent.draw_object(display, heretic)

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
            Map.draw_object(display, rooms)
            # print(i, j, (i - 90) // 80, (j - 90) // 80 * dung_length)

    display.blit(text_font.render(str(curr_room), True, (255, 255, 255)), (950, 20))
    display.blit(cursor_for_battle, cursor_for_battle.get_rect(center=(mouse_pos[0], mouse_pos[1])))

    pygame.display.update()
    clock.tick(60)

    tick += 1

    #
    # for i in bullets_list:
    #     if any([i.x < 0, i.x > 1000, i.y < 0, i.y > 800]):
    #         bullets_list.remove(i)
    #     i.mark_list = list(filter(lambda j: j.life_time > 0, i.mark_list))
    #     i.mark_list.append(Mark(i.x, i.y, 10))
    #     for entity in entities_list:
    #         if i.owner != entity and i.x in entity.visible_zone[0] and i.y in entity.visible_zone[1]:
    #             bullets_list.remove(i)
    #             if entity.health >= 5:
    #                 entity.health -= 5

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
