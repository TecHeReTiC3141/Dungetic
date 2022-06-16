from classes.entities import *
from classes.camera import Camera

class Console:
    commands = ['tp',
                'add_item',
                'regen', 'clear_room']

    def __init__(self, camera: Camera, manager: GameManager, player_manager: PlayerManager):
        self.game_manager = manager
        self.player_manager = player_manager
        self.camera = camera

    def parse_command(self, command: str):
        name, *args = command.split()
        print(args)
        assert name in self.commands, 'Please enter existing command'
        if name == 'tp':
            self.tp(*args)
        elif name == 'add_item':
            self.add_item(*args)
        elif name == 'regen':
            self.regen(*args)
        elif name == 'clear_room':
            self.clear_room(*args)

    # TODO fix problems with grid after teleport
    def tp(self, *args):
        assert len(args) == 1, 'Only one arg for room number is required'
        room_ind = int(args[0])
        assert room_ind in self.game_manager.dungeon, \
            'This number is greater than number of rooms'
        self.game_manager.set_room(room_ind)
        self.camera.set_surf(self.game_manager.surf)
        print(self.game_manager.curr_room)

    def add_item(self, *args):
        assert 1 <= len(args) <= 2, 'Too many args'
        if len(args) == 1:
            itemclass = str(args[0])
            assert len(self.player_manager.player.inventory) < 20, 'Inventory is full'
            exec(f'self.player_manager.player.inventory.append({itemclass}())')
        elif len(args) == 2:
            itemclass, amount = str(args[0]), int(args[1])
            assert len(self.player_manager.player.inventory) < 20, 'Inventory is full'
            for i in range(min(amount, 20 - len(self.player_manager.player.inventory))):
                exec(f'self.player_manager.player.inventory.append({itemclass}())')

    def regen(self, *args):
        assert len(args) <= 1, 'Too many args'
        if not args:
            self.player_manager.player.actual_health = 100
        else:
            self.player_manager.player.actual_health = max(self.player_manager.player.actual_health + int(args[0]), 100)

    def clear_room(self, *args):
        assert not args, 'No args are required'
        for entity in self.game_manager.dungeon[self.game_manager.curr_room].entities_list:
            if isinstance(entity, Hostile):
                entity.actual_health = 0
