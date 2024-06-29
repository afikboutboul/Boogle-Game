from boggle_board_randomizer import *
from ex11_utils import *
import copy


class BoggleModel:

    def __init__(self) -> None:
        '''Initiates the model'''
        with open('boggle_dict.txt', 'rt') as file:
            self._word_bank = file.read().splitlines()
        self._board = randomize_board()
        self._current_path = []
        self._played_words = []
        self._cur_word = ""
        self._game_state = 0  # 0: menu, 1: game, 2:end screen
        self._remaining_time = 181
        self._score = 0
        self._new_word = False

    def action(self, button_name: str) -> None:
        '''
        :button_name: the button that press on gui board
        the function update the game data according the press button
        '''
        self._new_word = False
        if type(button_name) == tuple:
            if self.is_valid_press(button_name):
                self._current_path.append(button_name)
                self._cur_word += self._board[button_name[0]][button_name[1]]
        elif button_name == 'start':
            self._board = randomize_board()
            self._game_state = 1
            self._remaining_time = 181
            self._current_path = []
            self._played_words = []
            self._cur_word = ""
            self._score = 0
        elif button_name == 'clear':
            self._current_path = []
            self._cur_word = ""
        elif button_name == 'submit':
            if self.is_valid_word():
                self._score += len(self._current_path)**2
                self._played_words.append(self._cur_word)
                self._new_word = True
            self._current_path = []
            self._cur_word = ""

    def get_remaining_time(self) -> Tuple[int, bool]:
        if self._remaining_time < 0:
            self._game_state = 2
        return (self._remaining_time, self._game_state)

    def set_remaining_time(self) -> None:
        self._remaining_time -= 1

    def get_info(self) -> dict[str: Optional]:
        '''craet dict of data, the comander will send it to gui for update display'''
        d = {}
        d["current_path"] = self._current_path[:]
        d["played_words"] = self._played_words[:]
        d["cur_word"] = self._cur_word
        d["score"] = self._score
        d["new_word"] = self._new_word
        return d

    def get_board(self) -> Board:
        return copy.deepcopy(self._board)

    def is_valid_press(self, button_name: str) -> bool:
        new_path = self._current_path + [button_name]
        if len(new_path) <= 1:
            return True
        i = len(new_path)-1
        if new_path[i] in new_path[:-1]:
            return False
        row, col = new_path[i]
        next_row, next_col = new_path[i-1]
        move = (row-next_row, col-next_col)
        if move not in LEGAL_MOVES:
            return False
        return True

    def is_valid_word(self) -> bool:
        word = is_valid_path(self._board, self._current_path, self._word_bank)
        if not word:
            return False
        if word in self._played_words:
            return False
        return True
