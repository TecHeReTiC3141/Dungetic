from classes.Heretic import GameManager, Heretic, PlayerManager

class Console:
    commands = ['tp',
                'add_item']

    def __init__(self, manager: GameManager, player_manager: PlayerManager):
        self.manager = manager
        self.player_manager = player_manager

    def parse_command(self, command: str):
        name, *args = command.split()
        print(args)
        return name in self.commands

    def tp(self, curr_room: int):
        pass

    def add_item(self):
        pass