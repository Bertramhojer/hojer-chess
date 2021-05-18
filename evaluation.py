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

        # Engine playing black
        sicilian = [['e2e4', 'g1f3', 'd2d4', 'f3d4'], ['c7c5', 'd7d6', 'c5d4', 'g8f6']]
        q_gambit = [['d2d4', 'c2c4', 'b1c3', 'g1f3'], ['d7d5', 'e7e6', 'g8f6', 'c7c6']]
        caro_kann = [[], []]

        # Engine playing white

        # Function to run through opening-lines
        def find_move(self, opening_moves):
            try:
                if self.made_moves[0] == opening_moves[0][0]:
                    try:
                        if self.made_moves[2] == opening_moves[0][1]:
                            pass
                            try:
                                if self.made_moves[4] == opening_moves[0][2]:
                                    try:
                                        if self.made_moves[6] == opening_moves[0][3]:
                                            return opening_moves[1][3]
                                    except:
                                        return opening_moves[1][2]
                            except:
                                return opening_moves[1][1]
                    except:
                        return opening_moves[1][0]
            except:
                return None
        

        # Engine playing black
        if self.user == chess.WHITE:
            if find_move(self, sicilian) != None:
                return find_move(self, sicilian)
            if find_move(self, q_gambit) != None:
                return find_move(self, q_gambit)
            return None


        # Engine playing white
        if self.user == chess.BLACK:
            pass




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
    is_capture() : checks whether a move is a capture
    evaluate_capture() : evaluates whether a trade is favorable
    is_attacked() : checks whether a given move will place the piece under attack
    is_defended() : check whether a given move will place the piece on a defended square
    evaluate_board() : makes an evaluation of the board by calculating the values from evaluate_piece() for all pieces on the board.
    evaluate_move() : makes use of above-stated evaluation functions to find the best move in the current position.

    """


    def __init__(self, board, made_moves, user):
        super().__init__(board, made_moves, user)
    

    def is_end_game(self, board):
        queens = 0
        minors = 0

        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if not piece:
                continue
            if piece.piece_type == chess.QUEEN:
                queens += 1
            if (piece.piece_type == chess.BISHOP or piece.piece_type == chess.KNIGHT):
                minors += 1
        
        if queens == 0 or (queens == 2 and minors <= 1):
            return True


    def evaluate_piece(self, board, piece, loc):

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
                if self.is_end_game(board):
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
                if self.is_end_game(board):
                    return constants.piece_value[6] + constants.black_king_end[loc]
                else:
                    return constants.piece_value[6] + constants.black_king_mid[loc]

    
    def is_capture(self, board, _sq):
        _sq = board.piece_at(_sq)
        if _sq is None:
            return False
        return True
    

    def evaluate_capture(self, to_sq, from_sq):
        piece_1 = self.board.piece_at(to_sq).piece_type
        piece_2 = self.board.piece_at(from_sq).piece_type

        if (constants.piece_value[piece_1] - constants.piece_value[piece_2]) <= 0:
            return True
        return False

    
    def under_attack(self, board, move):
        # define a function that checks whether any opposite side pieces can attack the piece on current square
        pass

    
    def is_attacked(self, board, move):
        tmp_board = board.copy()
        tmp_board.push(move)
        for attack in tmp_board.legal_moves:
            if attack.to_square == move.to_square:
                return True
        
        return False


    def evaluate_board(self, board):
        total = 0
        for sq in chess.SQUARES:
            piece = board.piece_at(sq)

            if not piece:
                continue

            value = self.evaluate_piece(board, piece, sq)

            if piece.color == chess.WHITE:
                total += value
            elif piece.color == chess.BLACK:
                total -= value
            
            return total
    
    def evaluate_board_2(self, board, move):

        tmp_board = board.copy()
        tmp_board.push(move)

        return self.evaluate_board(tmp_board)
    

    def move_is_check(self, board, move):

        tmp_board = board.copy()
        tmp_board.push(move)
        if tmp_board.is_check():
            return True
        return False
            


    def evaluate_move(self, board):
        
        high_score = 0
        best_move = None

        for move in board.legal_moves:
            # check capture
            # evaluate capture
            # check defended
            # check attacked
            
            score = 0
            loc_1 = move.from_square
            loc_2 = move.to_square
            piece = board.piece_at(loc_1)

            if best_move is None:
                best_move = move

            if self.is_capture(board, loc_2):
                if self.evaluate_capture(loc_1, loc_2):
                    score += 10
                else:
                    score -= 5
            
            if self.evaluate_piece(board, piece, loc_1) <= self.evaluate_piece(board, piece, loc_2):
                score += (self.evaluate_piece(board, piece, loc_2))-(self.evaluate_piece(board, piece, loc_1))
            else:
                score -= 10
            
            if self.is_attacked(board, move):
                score += 10
            else:
                score -= 30
            
            if self.move_is_check(board, move):
                score += 10
            
            if self.evaluate_board(board) < self.evaluate_board_2(board, move):
                score += 20
            else:
                score -= 1
            
            print(f"score: {score}, move: {move}")
            
            if score > high_score:
                high_score = score
                best_move = move
                
        
        return best_move