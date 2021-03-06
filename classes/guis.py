from scripts.Console import *


class GUI:

    def __init__(self, manager: GameManager):
        self.manager = manager
        self.manager.is_paused = True
        self.layout = [
            []
        ]
        self.window = sg.Window('Gui', manager)

    def run(self):
        pass

    def close(self):
        self.window.close()
        self.manager.is_paused = False
        print('closed')


class Settings(GUI):
    # TODO add gamma to display settings
    def __init__(self, manager: GameManager):
        self.manager = manager
        self.manager.is_paused = True

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
                 sg.Checkbox('Fullscreen', key='-FULLSCREEN-'), sg.Checkbox('Show damage', key='-DAMAGEIND-')]
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
        self.run()

    def run(self):

        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED or event == 'Reset':
                self.close()
                break

            elif event == 'Apply':
                blood, res, full, show_damage = values['-BLOOD-'], \
                                                tuple(map(int, values['-RES-'].split('x'))), \
                                                values['-FULLSCREEN-'], values['-DAMAGEIND-']
                self.manager.update(res, blood, full, show_damage)
                self.close()
                break


class ConsoleGui(GUI):

    def __init__(self, console: Console):
        self.console = console

        sg.theme('Dark')
        sg.set_options(font='Ubuntu 12')

        self.layout = [
            [sg.Text('Please insert command:')],
            [sg.Input(key='-COMMAND-')],
            [sg.Button('Apply command'), sg.Button('List of commands')]
        ]

        self.window = sg.Window('DungeonConsole', layout=self.layout)
        self.run()

    def run(self):

        while True:

            event, values = self.window.read()

            if event == sg.WIN_CLOSED:
                self.close()
                break

            elif event == 'Apply command':
                try:
                    self.console.parse_command(values['-COMMAND-'])
                    print(self.console.game_manager.curr_room,
                          self.console.player_manager.player.inventory)
                except Exception as e:
                    sg.Popup(str(e), title='Error')

            elif event == 'List of commands':
                with open('../console_commands.txt') as comm:
                    sg.popup(comm.read(), title='Hello!')

    def close(self):
        self.window.close()
        self.console.game_manager.is_paused = False
        print('closed')


class SkillsGui(GUI):
    descr = {
        'speed': 'How fast can you run',
        'damage': 'Increases player damage',
        'resist': 'Adds natural armor'
    }

    def __init__(self, manager: GameManager, player: Heretic):
        self.player = player
        self.manager = manager

        sg.theme('DarkAmber')
        sg.set_options(font='Frank 12')

        self.stats_table = [[k, v[0], v[1]] for k, v in player.skills.items()]

        self.layout = [
            [sg.Text('Player stats and improvement', font='Frank 20')],
            [sg.HorizontalSeparator()],
            [sg.Table(values=self.stats_table, headings=['Skill', 'Level', 'Value'], key='-DATA-', expand_x=True)],
            [sg.Frame(f'Level {player.level}', layout=[
                [sg.ProgressBar(max_value=20 * (player.level + 1),
                                orientation='h', key='-PROGRESS-', size=(10, 8)),
                 sg.Text(f'{self.player.experience} / {20 * (player.level + 1)}')],
                [sg.Text(f'Points remaining: {self.player.exp_points}', key='-REMAIN-')]
            ],
                      tooltip=f'{20 * (player.level + 1) - self.player.experience} to the next level'),
             sg.Frame('Improve yourself!', layout=[
                 [sg.Spin(list(self.player.skills.keys()), text_color='black', key='-SKILLS-',
                          readonly=True, background_color='black', tooltip=self.descr['speed']),
                  sg.Button('Improve')],
                 [sg.Output(key='-SKILLDESCR-', s=(25, 4))]
             ])
             ],
        ]

        self.window = sg.Window('Stats', layout=self.layout, element_justification='left', finalize=True)
        self.window['-PROGRESS-'].update(self.player.experience)
        self.run()

    def run(self):

        while True:
            event, values = self.window.read(timeout=15)
            try:

                if event == sg.WIN_CLOSED:
                    self.window.close()
                    break

                elif event == 'Improve':
                    if self.player.exp_points > 0:
                        self.player.exp_points -= 1
                        self.window['-REMAIN-'].update(f'Points remaining: {self.player.exp_points}')

                        skill = values['-SKILLS-']
                        self.player.skills[skill][0] += 1
                        if skill == 'damage':
                            self.player.skills[skill][1] += .1 * (self.player.skills[skill][0] // 3 + 1)
                        elif skill == 'speed':
                            self.player.skills[skill][1] += .4 * (self.player.skills[skill][0] // 5 + 1)
                        elif skill == 'resist':
                            self.player.skills[skill][1] += .1 * (self.player.skills[skill][0] // 3 + 1)

                        self.stats_table = [[k, round(v[0], 2), round(v[1], 2)] for k, v in self.player.skills.items()]

                        self.window['-DATA-'].update(values=self.stats_table)

                    print(values)
                self.window['-SKILLS-'].set_tooltip(self.descr[values['-SKILLS-']], )
                self.window['-SKILLDESCR-'].update(self.descr[values['-SKILLS-']])
                self.window.refresh()
            except Exception as e:
                layout = [
                    [sg.Text(f'It seems that an error happened: {e}')],
                    [sg.OK('Kill up?'), sg.No('Or continue')]
                ]
                window = sg.Window('Error', layout)
                ev, values = window.read()
                window.close()
                assert ev != 'Kill app?', str(e)


class Saving(GUI):

    def __init__(self, manager: GameManager, player: Heretic):
        self.player = player
        self.manager = manager

        sg.theme('DarkAmber')
        sg.set_options(font='Frank 12')

        layout = [
            [sg.T('Enter name of saving'),],
            [sg.HSep()],
            [sg.In(key='-SAVENAME-'), sg.B('Save')],
        ]

        event, values = sg.Window('Saving', layout=layout, element_justification='center').read(close=True)
        if event == 'Save':
            # cur_time = strftime( '%m.%d.%y %H-%M-%S %a', gmtime(time()))
            with open(f'../saving/{values["-SAVENAME-"]}.pcl', 'wb') as save:
                pickle.dump(self.manager.curr_room, save)
                pickle.dump(self.manager.dung_width, save)
                pickle.dump(self.manager.dung_length, save)
                pickle.dump(self.manager.dungeon, save)
                pickle.dump(self.player, save)
            sg.popup('Successfully saved!')
            # except Exception as e:
            #     sg.popup_error(str(e.args) + ' ' + str(e))
            #     del_save = Path(f'../saving/{values["-SAVENAME-"]}.pcl')
            #     del_save.unlink()


class Loading(GUI):

    def __init__(self, manager: GameManager, player: Heretic):
        self.player = player
        self.manager = manager

        saving = Path('../saving')

        self.saves = sorted(saving.glob('*.pcl'), key=lambda i: i.stat().st_ctime)

        sg.theme('DarkAmber')
        sg.set_options(font='Frank 12')
        layout = [
            [sg.T('Choose save')],
            [sg.HSep()],
            [sg.Table(values=[(i.name, strftime('%m.%d.%y %H-%M-%S',
                                                 localtime(i.stat().st_ctime)))
                              for i in self.saves],
                      headings=['name', 'created'], enable_events=True, key='-SAVES-')],
            [sg.B('Load', disabled=True)]
        ]

        self.window = sg.Window('Loading', layout=layout)
        self.run()

    def run(self):
        save_active = -1

        while True:
            event, values = self.window.read()

            if event == sg.WIN_CLOSED:
                break

            elif event == '-SAVES-':
                self.window['Load'].update(disabled=False)
                save_active, = values[event]

            elif event == 'Load':
                save_name = self.saves[save_active].name
                with open(Path('../saving') / save_name, 'rb') as save:
                    cur_room, dung_width, dung_length, dungeon, player = [pickle.load(save) for _ in '.....']
                    self.manager.dungeon = dungeon
                    self.manager.dung_width = dung_width
                    self.manager.dung_length = dung_length
                    self.manager.set_room(cur_room)
                    self.player.set_player(player)
                break
        self.window.close()

# TODO think about progressbars of serialization and deseriali


# manager = GameManager((720, 480), [], 0)
# heretic = Heretic(100, 100, 100, 100, 100, 'left', manager)
# heretic.exp_points = 10
# heretic.level = 5
# heretic.experience = 75
# player_manager = PlayerManager(heretic)
# Saving(manager, heretic)
#
# save_data = Loading().run()
#
# pprint(save_data)
