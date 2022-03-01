from classes.Heretic import *
from classes.surrounding import *
from scripts.algorithms_of_generation import generate_dungeons

heretic = Heretic(100, 100, 75, 100, 78, random.choice(directions), [])

polygon = generate_dungeons()
print(*polygon)

sp_ev = pygame.USEREVENT + 1
show_speed = pygame.time.set_timer(sp_ev, 60)
clock = pygame.time.Clock()

while game_cycle:
    for event in pygame.event.get():
        if event.type == sp_ev:
            print(curr_room)
        if event.type == pygame.QUIT:
            pygame.quit()

    polygon[curr_room].draw_object(display)
    heretic.draw_object(display)
    heretic.move()
    pygame.display.update()
    polygon[curr_room].life()
    polygon[curr_room].physics(heretic)
    clock.tick(60)
