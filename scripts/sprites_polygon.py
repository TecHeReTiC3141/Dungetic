from classes.Heretic import *
from classes.surrounding import *

heretic = Heretic(100, 100, 75, 100, 78, random.choice(directions), [])
npc = NPC(100, 100, 75, 100, 6, 'right', [], 5)
vase = Vase(random.randint(100, 300), random.randint(100, 300), 50, 50)
wall = Wall(random.randint(100, 300), random.randint(100, 300),
            random.randint(50, 150), random.randint(50, 150))
pygame.image.save(vase.draw_object(display), '../images/vase_sprite.png')
direction = 'left right up down'.split()

clock = pygame.time.Clock()

while game_cycle:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    display.fill((218, 150, 61))
    wall.draw_object(display)
    heretic.draw_object(display)
    npc.draw_object(display)
    heretic.move()
    npc.passive_exist()
    pygame.display.update()
    wall.collide([heretic, npc])
    clock.tick(60)
