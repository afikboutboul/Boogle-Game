##############################################################################
#                                   Imports                                  #
##############################################################################
import tkinter as tk
import random
from typing import Callable

##############################################################################
#                                 CONSTANTS                                  #
##############################################################################
# IMAGES
MENU_BG_IMG = "menu_bg.png"
START_BUTTON_IMG = "start_btn.png"
GAME_OVER_BG_IMG = "game_over.png"
MENU_BUTTON_IMG = "menu_btn.png"

# COLORS
MAIN_COLOR = "#FDB750"
SECONDARY_COLOR = "#F57921"
BUTTON_COLOR = "#F57921"
BUTTON_HOVER_COLOR = "#FC2E20"
BUTTON_CLICK_COLOR = "#900800"
BUTTON_PRESSED_COLOR = "#E23734"
BUTTON_ERROR_COLOR = "red"


# BUTTON STYLES
BUTTON_STYLE = {"borderwidth": 1,
                "relief": tk.RAISED,
                "bg": BUTTON_COLOR,
                "activebackground": BUTTON_CLICK_COLOR}
MENU_BUTTON_STYLE = {"borderwidth": 0,
                     "highlightthickness": 0,
                     "bd": 0,
                     "relief": tk.FLAT}

FONT = "Small Fonts"

GOOD_MESSAGE_BANK = ["Well Done!!", "Good Word!!", "Nice!!",
                     "Profesional!!", "You are the BOGGLE king!!", "Wonderful!!"]
BAD_MESSAGE_BANK = ["Can't do that...",
                    "Are you trying to trick on me?", "NOPE!"]

##############################################################################
#                                  CLASS                                     #
##############################################################################


class BoggleGUI:
    def __init__(self) -> None:
        '''Initiates the gui'''
        root = tk.Tk()
        root.title("Boggle")
        root.resizable(False, False)
        root.geometry("800x600")
        self._buttons = dict()  # Dictionary of all game buttons

        # Menu: First frame of the game, has a button to start the game
        self._menu = tk.Frame(root)
        self._menu.pack(fill=tk.BOTH, expand=True)
        self._bg_img = tk.PhotoImage(file=MENU_BG_IMG)
        self._strt_btn_img = tk.PhotoImage(file=START_BUTTON_IMG)
        self._background_image = tk.Label(self._menu, image=self._bg_img)
        self._background_image.pack()
        self._start = tk.Button(
            self._menu, image=self._strt_btn_img, **MENU_BUTTON_STYLE)  # Start Button
        self._buttons['start'] = self._start
        self._start.place(x=300, y=400)

        # Game: Main frame of the game
        self._main_window = root
        self._outer_frame = tk.Frame(root, bg=MAIN_COLOR)
        self._display_label = tk.Label(self._outer_frame, bg=SECONDARY_COLOR, text="BOGGLE",
                                       font=(FONT, 30), width=100, relief="ridge")
        self._display_label.pack(side=tk.TOP, fill=tk.BOTH)

        # Right Frame
        self._right_frame = tk.Frame(self._outer_frame, bg=MAIN_COLOR)
        self._right_frame.pack(side=tk.RIGHT, fill=tk.BOTH)

        # Right Frame: Score: tallies the score
        self._score_frame = tk.Frame(
            self._right_frame, height=80, bg=MAIN_COLOR)
        self._score_frame.pack(side=tk.TOP, fill=tk.BOTH)
        self._score_title_label = tk.Label(
            self._score_frame, text="Score:", font=(FONT, 20), bg=MAIN_COLOR)
        self._score_title_label.pack(side=tk.TOP)
        self._score_label = tk.Label(
            self._score_frame, text='0', font=(FONT, 20), bg=MAIN_COLOR)
        self._score_label.pack()

        # Right Frame: Words List: listbox containing all of the played words
        self._cur_word_lable = tk.Label(
            self._right_frame, font=(FONT, 25, "bold"), bg=MAIN_COLOR)
        self._cur_word_lable.pack(pady=10,)
        self._words_frame = tk.Frame(self._right_frame, bg=MAIN_COLOR)
        self._words_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self._words_lst_title_label = tk.Label(self._words_frame, font=(
            FONT, 20), text="Words you've found: ", bg=MAIN_COLOR)
        self._words_lst_title_label.pack(side=tk.TOP)
        self._words_list_scrollbar = tk.Scrollbar(
            self._words_frame, orient=tk.VERTICAL, bg=MAIN_COLOR)
        self._words_listbox = tk.Listbox(self._words_frame, font=(FONT, 15), bg=SECONDARY_COLOR,
                                         justify=tk.CENTER, yscrollcommand=self._words_list_scrollbar.set)
        self._words_list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self._words_listbox.pack(fill=tk.BOTH, expand=True)
        self._words_list_scrollbar.config(command=self._words_listbox.yview)

        def clear_selection(event):
            '''this function removes selection feature of listbox'''
            self._words_listbox.selection_clear(0, tk.END)
        self._words_listbox.bind('<<ListboxSelect>>', clear_selection)

        # Left Frame
        self._left_frame = tk.Frame(self._outer_frame, bg=MAIN_COLOR)
        self._left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Left Frame: Time: Countdown of the game time, game ends at 0
        self._time_frame = tk.Frame(self._left_frame, bg=MAIN_COLOR)
        self._time_frame.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10)
        self._clock_title = tk.Label(self._time_frame, font=(
            FONT, 20), text="Time left:", bg=MAIN_COLOR)
        self._clock_title.pack(side=tk.LEFT)
        self._clock_label = tk.Label(self._time_frame, font=(
            FONT, 20), text="3 : 00", bg=MAIN_COLOR)
        self._clock_label.pack(side=tk.LEFT)
        self._message_label = tk.Label(
            self._time_frame, font=(FONT, 15), bg=MAIN_COLOR)
        self._message_label.pack(expand=True)
        self.clock_command = None

        # Left Frame: Board Frame: 4x4 board of buttons each corrasponding to a letter
        self._board_frame = tk.Frame(self._left_frame, bg=MAIN_COLOR)
        self._board_frame.pack(side=tk.TOP, fill=tk.BOTH,
                               expand=True, padx=10, pady=10)
        self._create_board_buttons()

        # Left Frame: Submission Frame: Submission and clear buttons for board
        self._sumbmission_frame = tk.Frame(self._left_frame, bg=MAIN_COLOR)
        self._sumbmission_frame.pack(
            side=tk.BOTTOM, fill=tk.BOTH, padx=10, pady=10)
        self._submit = tk.Button(
            self._sumbmission_frame, text="Submit", width=20, font=(FONT, 18), **BUTTON_STYLE)
        self._buttons['submit'] = self._submit
        self._buttons["submit"].pack(side=tk.LEFT)
        self._clear = tk.Button(
            self._sumbmission_frame, text="Clear", width=10, font=(FONT, 18), **BUTTON_STYLE)
        self._buttons['clear'] = self._clear
        self._buttons["clear"].pack(side=tk.RIGHT)

        # Game Over: Final frame of the game, has a button to return to menu
        self._game_over_img = tk.PhotoImage(file=GAME_OVER_BG_IMG)
        self._return_menu_img = tk.PhotoImage(file=MENU_BUTTON_IMG)
        self._game_over_frame = tk.Frame(root, bg=SECONDARY_COLOR)
        self._game_over_bg = tk.Label(
            self._game_over_frame, image=self._game_over_img)
        self._game_over_label = tk.Label(self._game_over_frame, font=(
            FONT, 38, "bold"), bg=SECONDARY_COLOR, fg="white")
        self._menu_button = tk.Button(
            self._game_over_frame, image=self._return_menu_img, **MENU_BUTTON_STYLE)
        self._buttons['menu'] = self._menu_button

    # Functions

    def start_game(self, board):
        '''Forgets the menu frame and packs the main game frame
        board: List of Lists containing letters
        '''
        self._menu.pack_forget()
        for key, button in self._buttons.items():
            if type(key) == tuple:
                button['background'] = BUTTON_COLOR
        self._cur_word_lable['text'] = ""
        self._score_label['text'] = '0'
        self._words_listbox.delete(0, tk.END)
        self._outer_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self._grid_board(board)
        self.clock_command()

    def _game_over(self):
        '''Forgets the game from and packs the game over frame'''
        self._game_over_label['text'] = "FINAL SCORE:\n" + \
            self._score_label['text']
        self._outer_frame.pack_forget()
        self._game_over_frame.pack(fill=tk.BOTH, expand=True)
        self._game_over_bg.pack()
        self._game_over_label.place(relx=0.3, rely=0.4)
        self._menu_button.place(x=300, y=400)

    def _create_board_buttons(self):
        '''creates the board buttons'''
        for i in range(4):
            for j in range(4):
                self._make_button(i, j)

    def _make_button(self, row, col):
        '''makes a single button given a row and column'''
        button = tk.Button(self._board_frame, font=(
            FONT, 20), width=10, **BUTTON_STYLE)
        self._buttons[(row, col)] = button

        def _on_enter(event):
            if button['background'] != BUTTON_PRESSED_COLOR:
                button['background'] = BUTTON_HOVER_COLOR

        def _on_leave(event):
            if button['background'] != BUTTON_PRESSED_COLOR:
                button['background'] = BUTTON_COLOR

        def _on_release(event):
            if button['background'] == BUTTON_ERROR_COLOR:
                button['background'] = BUTTON_HOVER_COLOR

        def _on_press(event):
            if button['activebackground'] != BUTTON_CLICK_COLOR:
                button['background'] = BUTTON_CLICK_COLOR

        button.bind("<Enter>", _on_enter)
        button.bind("<Leave>", _on_leave)
        button.bind("<ButtonRelease>", _on_release)
        button.bind("<Button-1>", _on_press)

    def _grid_board(self, board):
        '''places all board buttons in a grid'''
        for i in range(4):
            self._board_frame.grid_rowconfigure(i, weight=1)
            self._board_frame.grid_columnconfigure(i, weight=1)
        for key, button in self._buttons.items():
            if type(key) == tuple:
                self._buttons[key]['text'] = board[key[0]][key[1]]
                button.grid(row=key[0], column=key[1], sticky=tk.NSEW)

    # Get/Set Functions

    def get_button_names(self):
        return self._buttons.keys()

    # Updates (Set functions)
    def set_button_command(self, button_name, action):
        self._buttons[button_name]['command'] = action

    def update_display(self, paramaters, button_name):
        '''This single function calls to all update functions
        paramaters: a dictionary containg relevent model attributes
        button_name: name of button pressed
        '''
        if button_name == 'menu':
            self._game_over_frame.pack_forget()
            self._menu.pack(fill=tk.BOTH, expand=True)
        else:
            self.update_board(
                paramaters["current_path"], button_name, paramaters["new_word"])
            self.update_score(paramaters["score"])
            self.update_word_list(
                paramaters["played_words"], paramaters["new_word"])
            self.update_word(paramaters["cur_word"])

    def update_board(self, path, button_name, new_word):
        '''Updates the game board
        path: a list of tuples representing button locations
        button_name: the last button pressed, could be the submit button
        new_word: True if is a new word, False otherwise
        '''
        if new_word:
            self._message_label['text'] = random.choice(GOOD_MESSAGE_BANK)

            def command():
                self._message_label['text'] = ""
            self._message_label.after(1000, command)
        elif button_name == "submit":
            self._message_label['text'] = random.choice(BAD_MESSAGE_BANK)

            def command():
                self._message_label['text'] = ""
            self._message_label.after(1000, command)
        if not path:
            for key, button in self._buttons.items():
                if type(key) == tuple:
                    button['background'] = BUTTON_COLOR
        else:
            if path[-1] == button_name and self._buttons[button_name]['background'] != BUTTON_PRESSED_COLOR:
                self._buttons[button_name]['background'] = BUTTON_PRESSED_COLOR
            elif button_name in path or self._buttons[button_name]['background'] == BUTTON_PRESSED_COLOR:
                self._buttons[button_name]['background'] = BUTTON_ERROR_COLOR

                def command():
                    self._buttons[button_name]['background'] = BUTTON_PRESSED_COLOR
                self._buttons[button_name].after(100, command)
            else:
                self._buttons[button_name]['background'] = BUTTON_ERROR_COLOR

                def command():
                    self._buttons[button_name]['background'] = BUTTON_COLOR
                self._buttons[button_name].after(100, command)

    def update_word(self, cur_word):
        '''updates word on display to cur_word
        if word is too long, shortens the font
        '''
        if len(cur_word) < 10:
            self._cur_word_lable['font'] = (FONT, 25, "bold")
        else:
            if len(cur_word) < 13:
                sub = 5
            else:
                sub = 10
            self._cur_word_lable['font'] = (FONT, 25-sub, "bold")

        self._cur_word_lable['text'] = cur_word

    def update_score(self, score):
        self._score_label['text'] = str(score)

    def update_word_list(self, word_lst, new_word):
        if new_word:
            self._words_listbox.insert(tk.END, word_lst[-1])

    def set_clock_command(self, command: Callable) -> None:
        self.clock_command = command

    def update_clock(self, info):
        '''Updates in-game clock in sync with model
        info: tuple containing remaining time, and game_state
        '''
        if info[1] == 1:
            remaining_time = info[0]
            second_st = '0' + \
                str(remaining_time % 60) if remaining_time % 60 < 10 else str(
                    remaining_time % 60)
            st = str(remaining_time//60) + ' : ' + second_st
            self._clock_label.config(text=st)
            self._time_frame.after(1000, self.clock_command)
        else:
            self._game_over()

    # Run
    def run(self):
        self._main_window.mainloop()
