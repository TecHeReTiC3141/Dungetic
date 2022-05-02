from classes.Heretic import *
from scripts.constants_and_sources import dung_length, dung_width


class Console:
    commands = ['tp',
                'add_item']

    def __init__(self, manager: GameManager, player_manager: PlayerManager):
        self.game_manager = manager
        self.player_manager = player_manager

    def parse_command(self, command: str):
        name, *args = command.split()
        print(args)
        assert name in self.commands, 'Please enter existing command'
        if name == 'tp':
            self.tp(*args)
        elif name == 'add_item':
            self.add_item(*args)

    def tp(self, *args):
        assert len(args) == 1, 'Only one arg for room number is required'
        room_ind = int(args[0]) - 1
        assert 0 <= room_ind < dung_length * dung_width, \
            'This number is greater than number of rooms'
        self.game_manager.curr_room = room_ind
        print(self.game_manager.curr_room)

    def add_item(self, *args):
        assert 1 <= len(args) <= 2, 'Too many args'
        if len(args) == 1:
            itemclass = str(args[0])
            assert len(self.player_manager.player.inventory) < 20, 'Inventory is full'
            exec(f'self.player_manager.player.inventory.append({itemclass.capitalize()}())')
        elif len(args) == 2:
            itemclass, amount = str(args[0]), int(args[1])
            assert len(self.player_manager.player.inventory) < 20, 'Inventory is full'
            for i in range(min(amount, 20 - len(self.player_manager.player.inventory))):
                exec(f'self.player_manager.player.inventory.append({itemclass.capitalize()}())')

# TODO make up and implment some commands