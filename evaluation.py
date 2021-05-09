""""
Will contain multiple different move-evaluation algorithms 
"""
import chess
import constants
import random


class BaseEngine:

    def __init__(self):
        pass



class RandomEval:

    def __init__(self, board):
        self.board = board

    def make_move(self):
        self.moves = self.board.legal_moves

        self.moves = []
        for move in self.board.legal_moves:
            self.moves.append(str(move))
        self.random_move = self.moves[random.randrange(0, 20))]

        return self.random.move




class SimpleEval:

    def __init__(self, board):
        pass

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
