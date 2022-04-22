import PySimpleGUI as sg
from scripts.game_manager import GameManager

class Settings:

    def __init__(self, manager: GameManager):
        self.manager = manager

        sg.theme('DarkAmber')
        sg.set_options(font='Frank 12')
        self.layout = [
            [sg.Frame('Game', [
                [sg.Checkbox('Blood', default=True, text_color='red', key='-BLOOD-')]
            ])],
            [sg.HorizontalSeparator()],
            [sg.Frame('Graphics', [
                [sg.Text('Resolution'), sg.Spin(['720x480', '900x600'], key='-RES-'),
                 sg.Checkbox('Fullscreen', key='-FULLSCREEN-')]
            ],)],
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
                blood, res, full = values['-BLOOD-'], values['-RES-'].split('x'), values['-FULLSCREEN-']
                print(blood, res, full)
                self.close()
                break

    def close(self):
        self.window.close()
        print('closed')

manager = GameManager()

settings = Settings(manager)

settings.run()