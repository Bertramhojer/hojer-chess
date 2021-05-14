""""
Will contain multiple different move-evaluation algorithms 
"""
import chess
import constants
import random
import game




class Openings:
    
    def __init__(self, board, made_moves, user):
        self.board = board
        self.made_moves = made_moves
        self.user = user

    def is_opening(self):
        """
        Check if the game is in the opening phase
        """
        if self.board.fullmove_number <= 4:
            return True
        return False

    def get_opening_move(self):
        
        # Engine playing black
        if self.user == chess.WHITE:
            # open sicilian
       
            try:
                if self.made_moves[0]=='e2e4':
                    try:
                        if self.made_moves[2] == 'g1f3':
                            pass
                            try:
                                if self.made_moves[4] == 'd2d4':
                                    pass
                                    try:
                                        if self.made_moves[6] == 'f3d4':
                                            return 'g8f6'
                                    except:
                                        return str('c5d4')
                            except:
                                return str('d7d6')
                    except:
                        return str('c7c5')
            except:
                return None

            # queens gambit declined
            try:
                if self.made_moves[0]=='d2d4':
                    try:
                        if self.made_moves[2] == 'c2c4':
                            pass
                            try:
                                if self.made_moves[4] == 'b1c3':
                                    pass
                                    try:
                                        if self.made_moves[6] == 'g1f3':
                                            return 'c7c6'
                                    except:
                                        return str('g8f6')
                            except:
                                return str('e7e6')
                    except:
                        return str('d7d5')
            except:
                return None

        """
            if self.made_moves[0] == 'd2d4':
                if self.made_moves[2] == 'c2c4':
                    if self.made_moves[4] == 'b1c3':
                        if self.made_moves[6] == 'g1f3':
                            return 'c7c6'
                        return 'g8f6'
                    return 'e7e6'
                return 'd7d5'
        """

        if self.user == chess.BLACK:
            if self.made_moves == []:
                return 'e2e4'
            if self.made_moves[1] == 'c7c5':
                return 'g1g3'

    def make_opening_move(self):
        self.move = self.get_opening_move()
        for legal_move in self.board.legal_moves:
            if self.move == str(legal_move):
                return legal_move



        

class RandomEval(Openings):
    """
    Engine class that does no board evalatuon but produces a random move.

    Functions:
    Init intitiates the class with the current board from game.py
    make_move(): loops through legal moves and returns a random legal move
    """

    def __init__(self, board, made_moves, user):
        super().__init__(board, made_moves, user)
    

    def make_move(self):
        self.moves = self.board.legal_moves

        self.moves = []
        for move in self.board.legal_moves:
            self.moves.append(str(move))
        self.random_move = self.moves[random.randrange(0, len(self.moves))]

        return self.random_move



class SimpleEval(Openings):
    """
    Engine Class performing a simple evaluation inspired by Michniewski's simple evaluation;
    https://www.chessprogramming.org/Simplified_Evaluation_Function


    Functions:

    Init initiates the class with the current board from game.py

    is_opening(): takes no arguments and determines whether we're in the opening based on fullmoves made.

    is_end_game(): takes no arguments and determines end-game status by simple piece evaluation


    """

    def __init__(self, board, made_moves, user):
        super().__init__(board, made_moves, user)


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
