import PySimpleGUI as sg

class Settings:

    def __init__(self):
        sg.theme('DarkAmber')
        self.layout = [
            [sg.Frame('Game', [
                [sg.Checkbox('Blood', default=True, text_color='red', key='-BLOOD-')]
            ])],
            [sg.HorizontalSeparator()],
            [sg.Frame('Graphics', [
                [sg.Text('Resolution'), sg.Spin(['720x480', '900x600'])]
            ])]
        ]
        self.window = sg.Window('Settings', layout=self.layout)

    def run(self):

        while True:
            event, key = self.window.read()

            if event == sg.WIN_CLOSED:
                self.close()
                break

    def close(self):
        self.window.close()
        print('closed')

settings = Settings()

settings.run()