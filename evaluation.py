""""
Will contain multiple different move-evaluation algorithms 
"""
import chess
import constants
import random
import game


class BaseEngine:
    
    def __init__(self, board, made_moves, user):
        self.board = board
        self.made_moves = made_moves
        self.user = user

    def is_opening(self):
        """
        Check if the game is in the opening phase
        """
        if self.board.fullmove_number <= 5:
            return True
        return False

    def get_opening_move(self):

        self.sicilian = [['e2e4', 'g1f3', 'd2d4', 'f3d4'], ['c7c5', 'd7d6', 'c5d4', 'g8f6']]
        self.q_gambit = [['d2d4', 'c2c4', 'b1c3', 'g1f3'], ['d7d5', 'e7e6', 'g8f6', 'c7c6']]

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


        # Engine playing white
        if self.user == chess.BLACK:

            if self.made_moves == []:
                return 'e2e4'

            # open sicilian
            try:
                if self.made_moves[1]=='c7c5':
                    try:
                        if self.made_moves[3] == 'd7d6':
                            pass
                            try:
                                if self.made_moves[5] == 'c5d4':
                                    pass
                                    try:
                                        if self.made_moves[7] == 'g8f6':
                                            return 'b1c3'
                                    except:
                                        return str('f3d4')
                            except:
                                return str('d2d4')
                    except:
                        return str('g1f3')
            except:
                return None


    def make_opening_move(self):
        self.move = self.get_opening_move()
        for legal_move in self.board.legal_moves:
            if self.move == str(legal_move):
                return legal_move



class RandomEval(BaseEngine):
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



class SimpleEval(BaseEngine):
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
    

    def move_evaluation(self, board, move, endgame):
        """
        Evaluating the score of a given move
        """
        if move.promotion is not None:
            return -float("inf") if board.turn == chess.BLACK else float("inf")
        


    def capture_evaluation(self, board, move):
        """
        Evaluate the effects of making a capture
        """
        pass


    def piece_evaluation(self, piece, square, endgame):
        """
        Evaluate the value of a given piece on a given square
        """

        self.type = piece.piece_type
        self.mapping = list()
        if self.type == chess.PAWN:
            if piece.color == chess.WHITE:
                self.mapping = constants.white_pawn
            else:
                self.mapping = constants.black_pawn
        if self.type == chess.KNIGHT:
            self.mapping = constants.knight
        if self.type == chess.BISHOP:
            if piece.color == chess.WHITE:
                self.mapping = constants.white_bishop
            else:
                self.mapping = constants.black_bishop
        if self.type == chess.ROOK:
            if piece.color == chess.WHITE:
                self.mapping = constants.white_rook
            else:
                self.mapping = constants.black_rook
        if self.type == chess.QUEEN:
            self.mapping = constants.queen
        if self.type == chess.KING:
            if piece.color == chess.WHITE:
                if endgame:
                    self.mapping = constants.white_king_end
                else:
                    self.mapping = constants.white_king_mid
            else:
                if endgame:
                    self.mapping = constants.black_king_end
                else:
                    self.mapping = constants.black_king_mid


        return self.mapping[square]


    
    def board_evaluation(self):
        """
        Evaluates the current state of the board
        """

        self.total = 0

        for square in chess.SQUARES:
            self.piece = self.board.piece_at(square)
            if not self.piece:
                continue
                
            self.value = constants.piece_value[self.piece.piece_type] + self.piece_evaluation(self.piece, square, self.is_end_game(self.board))
            
            if self.piece.color == chess.WHITE:
                self.total += self.value
            else:
                self.total -= self.value
            
            return self.total
