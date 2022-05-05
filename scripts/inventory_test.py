from scripts.algorithms_of_generation import *
from classes.interfaces import *

heretic = Heretic(75, 100, 75, 100, 100, 'right', [])
game_manager = GameManager((1440, 1080), [], 0)
inventory = InventoryInter(heretic, game_manager)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    inventory.draw_object(display)
    display.blit(text_font.render(str(pygame.mouse.get_pos()), True, 'Black'), (10, 10))
    #pygame.image.save(inventory, '../images/interfaces/inventory.jpg')
    pygame.display.update()