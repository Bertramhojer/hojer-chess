""""
Will contain multiple different move-evaluation algorithms 
"""
import chess
import constants
import random


class BaseEngine:

    def __init__(self, board):
        self.board = board
        



class RandomEval:
    """
    Engine class that does no board evalatuon but produces a random move.

    Init contains the board initiates in the game.py file.
    make_move(): loops through legal moves and returns a random legal move
    """

    def __init__(self, board):
        self.board = board

    def make_move(self):
        self.moves = self.board.legal_moves

        self.moves = []
        for move in self.board.legal_moves:
            self.moves.append(str(move))
        print(self.moves)
        self.random_move = self.moves[random.randrange(0, len(self.moves))]

        return self.random_move



class SimpleEval:

    def __init__(self, board):
        self.board = board


    def is_end_game(board):
        queens = 0
        minors = 0

        for square in chess.SQUARES:
            piece = board.piece_at(square).piece_type
            if piece == chess.QUEEN:
                queens += 1
            if (piece == chess.BISHOP or piece == chess.KNIGHT):
                minors += 1
        
        if queens == 0 or (queens == 2 and minors <= 1):
            return True
