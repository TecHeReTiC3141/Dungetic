from scripts.algorithms_of_generation import *
from classes.interfaces import *

heretic = Heretic(100, 100, 100, 100, 100, 'left', [])
game_manager = GameManager()
inventory = InventoryInter(heretic, game_manager)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

    inventory.draw_object(display)
    #pygame.image.save(inventory, '../images/interfaces/inventory.jpg')
    pygame.display.update()