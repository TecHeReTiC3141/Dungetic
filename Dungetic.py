from classes.Heretic import Heretic
from classes.entities import produce_NPC
from classes.interfaces import MapInter, InventoryInter
from classes.surrounding import Wall, Vase, Room
from scripts.constants import *
from scripts.generation import generate_room, generate_dungeons

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
Invent = InventoryInter((display_width, display_height))

heretic = Heretic(100, 100, 75, 100, 100, 'left',
                  [], location=random.randint(1, dung_width * dung_length))

stop = []

'''
Генерация стен
'''
rooms = generate_dungeons()

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
        if not collised_walls.get(wall):
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
        Invent.draw(display, heretic)

    else:
        display.fill((252, 240, 188))
        rooms[curr_room].draw_object(display)
        rooms[curr_room].physics(heretic)
        rooms[curr_room].life()


        heretic.draw_object(heretic.visible_zone)
        for i in stop:
            pygame.draw.rect(display, (200, 0, 0), (*heretic.points[i - 1], 5, 5))
        # heretic2.draw_object()
        '''
    Отрисовка карты
        '''

        if current_interface == 'Map':
            Map.draw(display, rooms)
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
    collised_walls = {wall: [] for wall in rooms[curr_room].walls_list}
    '''
Расчет столкновений еретика со стеной
    '''
    for point in range(len(heretic.points)):

        for wall in rooms[curr_room].walls_list:
            if heretic.points[point][0] in wall.visible_zone[0] and heretic.points[point][1] in wall.visible_zone[1]:
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
