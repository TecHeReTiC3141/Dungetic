import PySimpleGUI as sg
from scripts.game_manager import *


class GUI:

    def __init__(self, manager: GameManager):
        self.manager = manager
        self.layout = [
            []
        ]
        self.window = sg.Window('Gui', manager)

    def run(self):
        pass

    def close(self):
        self.window.close()
        print('closed')


class Settings(GUI):

    def __init__(self, manager: GameManager):
        self.manager = manager
        sg.theme('DarkAmber')
        sg.set_options(font='Frank 12')

        graphics_tab = sg.Tab('Graphics', [
            [sg.Frame('Game', [
                [sg.Checkbox('Blood', default=True, text_color='red', key='-BLOOD-')]
            ])],
            [sg.HorizontalSeparator()],
            [sg.Frame('Graphics', [
                [sg.Text('Resolution'), sg.Spin(['900x600', '1080x720', '1440x900'],
                                                initial_value='1440x900', key='-RES-'),
                 sg.Checkbox('Fullscreen', key='-FULLSCREEN-')]
            ], )]], expand_y=True, expand_x=True)

        sound_tab = sg.Tab('Sounds', [
            [sg.Frame('Sounds', [
                [sg.Slider((1, 10), key='-SOUNDVOL', orientation='h', default_value=5)]
            ], expand_y=True, expand_x=True)],

            [sg.Frame('Music', [
                [sg.Slider((1, 10), key='-MUSICVOL', orientation='h', default_value=5)]
            ], expand_y=True, expand_x=True)]
        ])

        self.layout = [
            [sg.TabGroup([
                [graphics_tab, sound_tab],
            ])],
            [sg.HorizontalSeparator()],
            [sg.Push(), sg.Button('Reset', button_color='red'), sg.Button('Apply', button_color='green')]
        ]
        self.window = sg.Window('Settings', layout=self.layout, element_justification='left')

    def run(self):

        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED or event == 'Reset':
                self.close()
                break

            elif event == 'Apply':
                blood, res, full = values['-BLOOD-'], \
                                   tuple(map(int, values['-RES-'].split('x'))), \
                                   values['-FULLSCREEN-']
                self.manager.update(res, blood, full)
                self.close()
                break


class ConsoleGui(GUI):

    def __init__(self, manager: GameManager, console: Console):
        self.manager = manager
        self.console = console

        sg.theme('DarkAmber')
        sg.set_options(font='Frank 12')

        self.layout = [
            [sg.Text('Please insert command:')],
            [sg.Input(key='Command')],
            [sg.Button('Apply command'), sg.Button('List of commands')]
        ]

        self.window = sg.Window('DungeonConsole', layout=self.layout)

    def run(self):

        while True:

            event, values = self.window.read()

            if event == sg.WIN_CLOSED:
                self.close()
                break

            elif event == 'Apply command':
                pass

