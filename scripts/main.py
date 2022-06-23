from scripts.generation import generate_dungeons, Room, BossRoom
from classes.interfaces import Interface, MapInter, MainMenu, InventoryInter, ConsoleGui
from scripts.Console import *
from classes.camera import *

dung_length, dung_width = randint(4, 6), randint(4, 6)

polygon, curr_room, dung_width, dung_height = generate_dungeons(dung_width, dung_length)

tick = 0
draw_grid = False
cur_inter = None

game_manager = GameManager((display_width, display_height),
                           polygon, dung_width, dung_height, curr_room)
heretic = Heretic(100, 100, 75, 100, 100, choice(directions), game_manager)

camera = Camera(game_manager.surf, heretic)

player_manager = PlayerManager(heretic)

console = Console(camera, game_manager, player_manager)

Map = MapInter(game_manager)
Inventory = InventoryInter(heretic, game_manager)
Menu = MainMenu(game_manager, heretic)

print(*[''.join([str(j).rjust(3) for j in list(range(1 + dung_length * i,
                                                     dung_length * i + 1))]) for i in range(1, dung_width + 1)],
      sep='\n')

scrolling = (0, 0)

wipe = pygame.USEREVENT + 1
show_paths = pygame.USEREVENT + 2
pygame.time.set_timer(wipe, 10)
pygame.time.set_timer(show_paths, 150)
clock = pygame.time.Clock()
logging.info('The game cycle has begun')

while game_cycle:

    cur_room = game_manager.dungeon[game_manager.curr_room]
    for event in pygame.event.get():
        if event.type == wipe:
            cur_room.clear()
            # print(heretic.collided_walls, heretic.speed_directions)
        elif event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == show_paths:
            cur_room.make_paths(heretic)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                if isinstance(cur_inter, MapInter):
                    cur_inter = None
                else:
                    cur_inter = Map

            elif event.key == pygame.K_i:
                if isinstance(cur_inter, InventoryInter):
                    cur_inter = None
                    Inventory.close()
                    print(heretic.inventory)
                else:
                    cur_inter = Inventory
                    Inventory.open()

            elif event.key == pygame.K_e:
                if isinstance(heretic.weapon, Melee):
                    cur_room.decors.extend(heretic.hit(cur_room.entities_list,
                                                       cur_room.containers))
                elif isinstance(heretic.weapon, LongRange):
                    proj = heretic.shoot()
                    if proj is not None:
                        cur_room.projectiles.append(proj)

            elif event.key == pygame.K_g:
                draw_grid = ~draw_grid

            elif event.key == pygame.K_ESCAPE:
                game_manager.state = 'main_menu'

            elif event.key == pygame.K_SLASH:
                ConsoleGui(console)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse = list(pygame.mouse.get_pos())
            print(mouse)
            mouse[0] /= game_manager.res[0] / 1440
            mouse[1] /= game_manager.res[1] / 900
            mouse = tuple(mouse)
            if isinstance(cur_inter, InventoryInter):
                cur_inter.process(event.button, mouse)
            if event.button == 1:
                if game_manager.state == 'main_menu':
                    Menu.process(mouse)
                elif game_manager.state == 'main_game':
                    cur_room.check_drops((mouse[0] + scrolling[0], mouse[1] + scrolling[1]), [heretic])

    if game_manager.state == 'main_menu':
        Menu.draw_object(game_manager.display)

    elif game_manager.state == 'main_game':
        cur_room.draw_object(game_manager.surf, tick, draw_grid)
        heretic.draw_object(game_manager.surf)

        if isinstance(cur_inter, Interface):
            cur_inter.draw_object(game_manager.display)

        elif not game_manager.is_paused:
            heretic.move()
            heretic.update(tick, cur_room.is_safe)
            cur_room.life(tick)
            transition = cur_room.physics(heretic)
            ############################################################################
            if isinstance(cur_room, BossRoom) and transition:
                display.blit(stone_floor, (0, 0))
                display.blit(label := inventory_font.render('Go to the next level of dungeon...', True, BLACK),
                             (display_width - label.get_width() // 2, display_height - label.get_height() // 2))
                #  generating new level
                polygon, curr_room, dung_width, dung_height = generate_dungeons(dung_width, dung_length)
                game_manager.dungeon = polygon
                game_manager.dung_width = dung_width
                game_manager.dung_length = dung_length
                game_manager.set_room(curr_room)
                camera.set_surf(game_manager.surf)
            ############################################################################
            game_manager.display.fill('black')

            scrolling = camera.scroll()
            game_manager.display.blit(game_manager.surf, (0, 0), scrolling)
            game_manager.display.blit(screen_blur, (0, 0))
            game_manager.display.blits((
                (text_font.render(f'{game_manager.curr_room}', True, WHITE), (25, 25)),
                (text_font.render(f'{heretic.money}', True, '#f8b800'), (25, 55)),
                (text_font.render(f'{heretic.experience}', True, 'green'), (25, 85)),
                (text_font.render(f'{round(clock.get_fps())}', True, 'red'), (25, 115))
            ))


    pygame.display.update()

    clock.tick(60)
    tick += 1
    try:
        if heretic.cur_rect.colliderect(left_border):
            heretic.manager.set_room(heretic.manager.curr_room - 1)
            cur_room = game_manager.dungeon[game_manager.curr_room]
            camera.set_surf(heretic.manager.surf)
            heretic.cur_rect.left = cur_room.width - 100

        elif heretic.cur_rect.colliderect(right_border):
            heretic.manager.set_room(heretic.manager.curr_room + 1)
            cur_room = game_manager.dungeon[game_manager.curr_room]
            camera.set_surf(heretic.manager.surf)
            heretic.cur_rect.left = 50

        elif heretic.cur_rect.colliderect(upper_border):
            heretic.manager.set_room(heretic.manager.curr_room - dung_length)
            cur_room = game_manager.dungeon[game_manager.curr_room]
            camera.set_surf(heretic.manager.surf)
            heretic.cur_rect.top = cur_room.height - 125

        elif heretic.cur_rect.colliderect(lower_border):
            heretic.manager.set_room(heretic.manager.curr_room + dung_length)
            cur_room = game_manager.dungeon[game_manager.curr_room]
            camera.set_surf(heretic.manager.surf)
            heretic.cur_rect.top = 25

    except Exception as e:
        sg.popup("'Please don't leave my dungeon")
        rand_room = choice(list(game_manager.dungeon.keys()))
        heretic.manager.set_room(rand_room)
        cur_room = game_manager.dungeon[game_manager.curr_room]

    left_border = pygame.Rect(5, 0, 5, cur_room.height)
    right_border = pygame.Rect(cur_room.width - 15, 0, 5, cur_room.height)
    upper_border = pygame.Rect(0, 5, cur_room.width + 5, 5)
    lower_border = pygame.Rect(0, cur_room.height - 15, cur_room.width, 5)
