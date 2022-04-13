class GameManager:
    possible_states = ['main_menu',
                       'settings',
                       'main_game',
                       'inventory',
                       'inventory_skills',
                       'inventory_stats']

    def __init__(self, state='main_menu'):
        if state not in self.possible_states:
            raise RuntimeError('State is not supported')
        self.state = state
