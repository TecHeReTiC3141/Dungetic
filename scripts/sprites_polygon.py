from classes.Heretic import *
from classes.surrounding import *

heretic = Heretic(100, 100, 75, 100, 78, random.choice(directions), [])

vase = Vase(random.randint(100, 300), random.randint(100, 300), 50, 50)
polygon = Room([Wall(random.randint(100, 900), random.randint(100, 900),
            random.randint(50, 150), random.randint(50, 150)) for i in range(random.randint(3, 5))],
               produce_NPC(random.randint(1, 3)), None, 'wooden')
pygame.image.save(vase.draw_object(display), '../images/vase_sprite.png')
print(polygon.walls_list)
sp_ev = pygame.USEREVENT + 1
show_speed = pygame.time.set_timer(sp_ev, 60)
clock = pygame.time.Clock()

while game_cycle:
    for event in pygame.event.get():
        if event.type == sp_ev:
            pass
        if event.type == pygame.QUIT:
            pygame.quit()

    polygon.draw_object(display)
    heretic.draw_object(display)
    heretic.move()
    pygame.display.update()
    polygon.life()
    polygon.physics(heretic)
    clock.tick(60)
