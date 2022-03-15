class GameManager:
    possible_states = ['main_menu',
                       'settings',
                       'main_game',
                       'inventory']

    def __init__(self, state='main_menu'):
        self.state = state
