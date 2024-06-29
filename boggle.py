#################################################################
# FILE : boggle.py
# WRITERS : Yoav, yoav.kagan, 207839028, Afik, afik.boutboul, 315210799
# EXERCISE : intro2cs1 ex11 2023
# DESCRIPTION: Boggle
#################################################################

from boggle_board_randomizer import *
from boggle_model import BoggleModel
from boggle_gui import BoggleGUI


class BoggleController:
    def __init__(self) -> None:
        '''intiates the controller'''
        self._gui = BoggleGUI()
        self._model = BoggleModel()
        for button_name in self._gui.get_button_names():
            if button_name == "start":
                self._gui.set_button_command("start", self.start_game)
            else:
                action = self.create_button_action(button_name)
                self._gui.set_button_command(button_name, action)

    def create_button_action(self, button_name: str) -> callable:
        ''':return: an function to be the action for a given button'''
        def button_action():
            self._model.action(button_name)
            self._gui.update_display(self._model.get_info(), button_name)
        return button_action

    def start_time(self) -> None:
        '''set the clock command of the timer aftre function'''
        def clock_command():
            self._model.set_remaining_time()
            self._gui.update_clock(self._model.get_remaining_time())
        self._gui.set_clock_command(clock_command)

    def start_game(self) -> None:
        '''start button command'''
        self._model.action("start")
        self.start_time()
        self._gui.start_game(self._model.get_board())

    def run(self) -> None:
        self._gui.run()


if __name__ == '__main__':
    game = BoggleController()
    game.run()
