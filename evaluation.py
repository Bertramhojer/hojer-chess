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
    is_end_game() : takes no arguments and determines end-game status by simple piece evaluation
    evaluate_piece() : gets the current value of a given piece estimated from its intrinsic value added by the piece-square table value.
    evaluate_capture() : evaluates whether a possible trade is desirable.
    evaluate_move() : makes use of above-stated evaluation functions to find the best move in the current position.
    evaluate_board() : makes an evaluation of the board by calculating the values from evaluate_piece() for all pieces on the board.
    """


    def __init__(self, board, made_moves, user):
        super().__init__(board, made_moves, user)
    

    def is_end_game(self):
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


    def evaluate_piece(self, piece, loc):

        type = piece.piece_type
        
        if piece.color == chess.WHITE:
            if type == chess.PAWN:
                return constants.piece_value[1] + constants.white_pawn[loc]
            if type == chess.KNIGHT:
                return constants.piece_value[2] + constants.knight[loc]
            if type == chess.BISHOP:
                return constants.piece_value[3] + constants.white_bishop[loc]
            if type == chess.ROOK:
                return constants.piece_value[4] + constants.white_rook[loc]
            if type == chess.QUEEN:
                return constants.piece_value[5] + constants.queen[loc]
            if type == chess.KING:
                if self.is_end_game():
                    return constants.piece_value[6] + constants.white_king_end
                else:
                    return constants.piece_value[6] + constants.white_king_mid

        elif piece.color == chess.BLACK:
            if type == chess.PAWN:
                return constants.piece_value[1] + constants.black_pawn[loc]
            if type == chess.KNIGHT:
                return constants.piece_value[2] + constants.knight[loc]
            if type == chess.BISHOP:
                return constants.piece_value[3] + constants.black_bishop[loc]
            if type == chess.ROOK:
                return constants.piece_value[4] + constants.black_rook[loc]
            if type == chess.QUEEN:
                return constants.piece_value[5] + constants.queen[loc]
            if type == chess.KING:
                if self.is_end_game():
                    return constants.piece_value[6] + constants.black_king_end
                else:
                    return constants.piece_value[6] + constants.black_king_mid

    
    def evaluate_capture(self):
        pass



    def evaluate_move(self):

        move_val = 0

        for move in self.board.legal_moves:

            loc = move.from_square
            new_loc = move.to_square
            piece = self.board.piece_at(loc)
            value = self.evaluate_piece(piece, loc)
            new_value = self.evaluate_piece(piece, new_loc)
            if new_value > value:
                if (new_value - value) > move_val:
                    cur_best_move = move
        
        return cur_best_move


    def evaluate_board(self):
        total = 0
        for sq in chess.SQUARES:
            piece = self.board.piece_at(sq)

            if not piece:
                continue

            value = self.evaluate_piece(piece, sq)

            if piece.color == chess.WHITE:
                total += value
            elif piece.color == chess.BLACK:
                total -= value
            
            return total
