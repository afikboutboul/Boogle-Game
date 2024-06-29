from typing import List, Tuple, Iterable, Optional
from boggle_board_randomizer import *

Board = List[List[str]]
Path = List[Tuple[int, int]]
LEGAL_MOVES = [(1, 0), (1, 1), (0, 1), (-1, 1),
               (-1, 0), (-1, -1), (0, -1), (1, -1)]


def path_to_word(board: Board, path: Path) -> str:
    ''':return: word created by a given path on a given board'''
    word = ""
    for row, col in path:
        word += board[row][col]
    return word


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    ''':return: word if given path represent legal word on board'''
    if len(set(path)) != len(path):
        return
    for i in range(len(path)-1):
        row, col = path[i]
        next_row, next_col = path[i+1]
        move = (row-next_row, col-next_col)
        if move not in LEGAL_MOVES:
            return
    word = ""
    for row, column in path:
        if cell_in_board((row, column)):
            word += board[row][column]
        else:
            return
    if word in words:
        return word
    else:
        return


def cell_in_board(cell: Tuple[int,int]) -> bool:
    '''
    :cell: Tuple containing cell location
    :retrun: True if cell on board, False otherwise
    '''
    return 0 <= cell[0] < 4 and 0 <= cell[1] < 4


def is_part_word(word: str, words: List) -> bool:
    '''
    :words: sorted list of legal bank_words
    :return: True if the current word is part of word in the words_bank,
    False otherwise
    '''
    start = 0
    end = len(words) - 1
    while end >= start:
        mid = (start+end)//2
        if word == words[mid][:len(word)]:
            return True
        elif words[mid] > word:
            end = mid - 1
        else:
            start = mid + 1
    return False


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    '''
    find all the legal length n path's represent legal word on given board
    '''
    sol = []
    words_lst = sorted([word for word in words if len(word) >= n])
    for row in range(len(board)):
        for column in range(len(board[0])):
            path = [(row, column)]
            sol.extend(_helper_find_length_n_paths(
                0, n, board, words_lst, [], path, board[row][column]))
    return sol


def _helper_find_length_n_paths(ind: int, n: int, board: Board,\
    words: List, sol_lst: List, path: Path, word: str):
    if len(path) == n:
        if word in words:
            sol_lst.append(path[:])
            return sol_lst
        else:
            return sol_lst
    if not is_part_word(word, words):
        return sol_lst
    for i, j in LEGAL_MOVES:
        next_row, next_column = path[ind][0]+i, path[ind][1]+j
        if (next_row, next_column) not in path and cell_in_board((next_row, next_column)):
            path.append((next_row, next_column))
            prev_word = word
            word += board[next_row][next_column]
            sol_lst = _helper_find_length_n_paths(
                ind + 1, n, board, words, sol_lst, path[:], word)
            path.pop()
            word = prev_word
    return sol_lst


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    '''
    find all the legal length n word's represent legal word on given board
    '''
    sol = []
    words_lst = sorted([word for word in words if len(word) == n])
    for row in range(len(board)):
        for column in range(len(board[0])):
            path = [(row, column)]
            sol.extend(_helper_find_length_n_words(
                0, n, board, words_lst, [], path, board[row][column]))
    return sol


def _helper_find_length_n_words(ind: int, n: int, board: Board,\
    words: List, sol_lst: List, path: Path, word: str):
    if len(word) == n:
        if word in words:
            sol_lst.append(path[:])
            return sol_lst
        else:
            return sol_lst
    elif len(word) > n:
        return sol_lst
    if not is_part_word(word, words):
        return sol_lst
    for i, j in LEGAL_MOVES:
        next_row, next_column = path[ind][0]+i, path[ind][1]+j
        if (next_row, next_column) not in path and cell_in_board((next_row, next_column)):
            path.append((next_row, next_column))
            prev_word = word
            word += board[next_row][next_column]
            sol_lst = _helper_find_length_n_words(
                ind + 1, n, board, words, sol_lst, path[:], word)
            path.pop()
            word = prev_word
    return sol_lst


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    '''This function returns the longest possible path for each word
    :return: a list of the paths
    '''
    legal_words = dict()
    for i in range(1, 17):
        paths_list = find_length_n_paths(i, board, words)
        for path in paths_list:
            legal_words[path_to_word(board, path)] = path
    return list(legal_words.values())
