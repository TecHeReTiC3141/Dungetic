import PySimpleGUI as sg
from scripts.game_manager import GameManager

class Settings:

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
            ],)]], expand_y=True, expand_x=True)

        sound_tab = sg.Tab('Sounds', [
            [sg.Frame('Sounds', [
                [sg.Slider((1, 10), key='-SOUNDVOL', orientation='h')]
            ])]
        ], expand_y=True, expand_x=True)


        self.layout = [
            [sg.TabGroup([
                [graphics_tab, sound_tab],
            ])],
            [sg.HorizontalSeparator()],
            [sg.Push(), sg.Button('Reset', button_color='red'), sg.Button('Apply', button_color='green')]
        ]
        self.window = sg.Window('Settings', layout=self.layout, element_justification='left')
        # TODO create a frame for sounds and music

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

    def close(self):
        self.window.close()
        print('closed')

