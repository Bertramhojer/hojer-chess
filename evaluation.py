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

    Functions:
    Init intitiates the class with the current board from game.py
    make_move(): loops through legal moves and returns a random legal move
    """

    def __init__(self, board, made_moves=list()):
        self.board = board
        self.made_moves = list()

    def make_move(self):
        self.moves = self.board.legal_moves

        self.moves = []
        for move in self.board.legal_moves:
            self.moves.append(str(move))
        print(self.moves)
        self.random_move = self.moves[random.randrange(0, len(self.moves))]

        return self.random_move



class SimpleEval:
    """
    Engine Class performing a simple evaluation inspired by Michniewski's simple evaluation;
    https://www.chessprogramming.org/Simplified_Evaluation_Function


    Functions:

    Init initiates the class with the current board from game.py

    is_opening(): takes no arguments and determines whether we're in the opening based on fullmoves made.

    is_end_game(): takes no arguments and determines end-game status by simple piece evaluation


    """


    def __init__(self, board, made_moves=list()):
        self.board = board
        self.made_moves = list()
    

    def is_opening(self):
        """
        Check if the game is in the opening phase
        """
        if self.board.fullmove_number < 5:
            return True
        return False


    def evaluate(self):
        pass


    def is_end_game(self):
        """
        Checking whether the end-game has been reached
        """
        queens = 0
        minors = 0

        for square in chess.SQUARES:
            piece = self.board.piece_at(square).piece_type
            if piece == chess.QUEEN:
                queens += 1
            if (piece == chess.BISHOP or piece == chess.KNIGHT):
                minors += 1
        
        if queens == 0 or (queens == 2 and minors <= 1):
            return True
