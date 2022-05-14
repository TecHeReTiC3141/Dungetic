from classes.surrounding import *

game_manager = GameManager((1440, 720), )
heretic = Heretic(100, 100, 75, 100, 78, random.choice(directions), speed=5, weapon=Knife(), )

vase = Vase(random.randint(100, 300), random.randint(100, 300), 50, 50, movable=True)
polygon = Room([Wall(random.randint(100, 900), random.randint(100, 900),
            random.randint(50, 150), random.randint(50, 150)) for i in range(random.randint(9, 15))],
               [vase], NPC.produce_NPC(random.randint(1, 2))
               + Hostile.produce_Hostiles(random.randint(2, 3)), [], None, 'wooden', )

tick = 0
show_grid = False
sp_ev = pygame.USEREVENT + 1
show_paths = pygame.USEREVENT + 2
pygame.time.set_timer(sp_ev, 5)
pygame.time.set_timer(show_paths, 150)
clock = pygame.time.Clock()

while game_cycle:
    for event in pygame.event.get():
        if event.type == sp_ev:
            polygon.clear()

        elif event.type == show_paths:
            polygon.make_paths(heretic)


        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                heretic.hit(polygon.entities_list, polygon.containers)

            elif event.key == pygame.K_r:
                polygon.projectiles.append(heretic.throw_ball())

            elif event.key == pygame.K_q:
                show_grid = ~show_grid

    polygon.draw_object(display, tick, show_grid)
    heretic.draw_object(display)
    polygon.life(tick)
    polygon.physics(heretic)
    heretic.move()
    heretic.update(tick)
    pygame.display.update()

    tick += 1
    clock.tick(60)
