import chess
import constants
import random


class BaseEngine:
    """
    Base class for evaluation classes containing opening knowledge.

    - functions -
    is_opening() : checks the state of the game
    get_opening_move() : finds opening move if in database
    make_opening_move() : returns an opening move as chess.Move object
    """
    
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
        """
        Gets the correct theoretical response to certain opening moves.

        - functions -
        find_move() : checks the response to a move from a given opening

        - variables -
        sicilian (list) : opening moves for the open sicilian
        q_gambit (list) : opening moves for the queens gambit declined 
        """

        # Engine playing black
        sicilian = [['e2e4', 'g1f3', 'd2d4', 'f3d4'], ['c7c5', 'd7d6', 'c5d4', 'g8f6']]
        q_gambit = [['d2d4', 'c2c4', 'b1c3', 'g1f3'], ['d7d5', 'e7e6', 'g8f6', 'c7c6']]

        # Engine playing white
        # add openings

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
        print(self.move)
        for legal_move in self.board.legal_moves:
            if self.move == str(legal_move):
                return legal_move



class RandomEval(BaseEngine):
    """
    Engine class that does no board evalatuon but produces a random move.
    Inherits BaseEngine-Class.

    Functions:
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
    Inherits BaseEngine-Class.

    - functions -
    is_end_game() : determines end-game status by simple piece evaluation
    evaluate_piece() : evaluates piece by piece-square tables
    is_capture() : checks whether a move is a capture
    evaluate_capture() : evaluates whether a trade is favorable
    under_attack_now() : checks for attacks at current square
    under_attack_future() : checks for attacks on future square
    evaluate_board() : makes overall board evaluation based on piece-square tables
    get_move_score() : estimates best move from evaluation functions.
    get_best_move() : gets the best move in the position
    """

    def __init__(self, board, made_moves, user):
        super().__init__(board, made_moves, user)
    

    def is_end_game(self):
        """
        Checks the state of the game as specified here;
        https://www.chessprogramming.org/Simplified_Evaluation_Function
        """

        queens = 0
        minors = 0

        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if not piece:
                continue
            if piece.piece_type == chess.QUEEN:
                queens += 1
            if (piece.piece_type == chess.BISHOP or piece.piece_type == chess.KNIGHT):
                minors += 1
        
        if queens == 0 or (queens == 2 and minors <= 1):
            return True


    def evaluate_piece(self, piece, loc):
        """
        Evaluates the current value of a piece from the specified piece-square tables and locations.    
        """

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
                    return constants.piece_value[6] + constants.white_king_end[loc]
                else:
                    return constants.piece_value[6] + constants.white_king_mid[loc]

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
                    return constants.piece_value[6] + constants.black_king_end[loc]
                else:
                    return constants.piece_value[6] + constants.black_king_mid[loc]

    
    def is_capture(self, _sq):
        """
        Checks whether their is a piece on a given square.
        """
        _sq = self.board.piece_at(_sq)
        if _sq is None:
            return False
        return True
    

    def evaluate_capture(self, to_sq, from_sq):
        """
        Evaluates the dfifference between an attacking piece and an attacked piece.
        """

        # attacked piece
        piece_1 = self.board.piece_at(to_sq).piece_type
        # capturing piece
        piece_2 = self.board.piece_at(from_sq).piece_type

        # difference in piece values according to constants.py
        piece_diff = (constants.piece_value[piece_1] - constants.piece_value[piece_2])

        # e.g. knight for bishop or pawn for pawn
        if piece_diff >= 0 and piece_diff < 100: 
            return 1
        # minor piece for major piece
        if piece_diff >= 100 and piece_diff < 300:
            return 2
        # minor/major piece for queen/king
        if piece_diff >= 300:
            return 3
        # badly weighed trade
        if piece_diff < 0:
            return 0
            
    
    def under_attack_now(self, move):
        """
        Checks whether an piece is currently under attack and evaluates how many and
        which piece are attacking.

        - variables -
        attackers : list of squares from which square is attacked
        att_types : list of piece_types on attacking squares
        """

        # Check attacking pieces when engine is black
        if self.user == chess.WHITE:
            if self.board.is_attacked_by(chess.WHITE, move.from_square):
                attackers = list(self.board.attackers(chess.WHITE, move.from_square))
                att_types = []
                for att in attackers:
                    att_types.append(self.board.piece_at(att).piece_type)
                return att_types

        # Check attackibg pieces when engine is white
        if self.user == chess.BLACK:
            if self.board.is_attacked_by(chess.BLACK, move.from_square):
                attackers = list(self.board.attackers(chess.BLACK, move.from_square))
                att_types = []
                for att in attackers:
                    att_types.append(self.board.piece_at(att).piece_type)
                return att_types

    
    def under_attack_future(self, move):
        """
        Checks whether a piece will be under attack if move is made and evaluates,
        how many and which pieces are attacking.

        - variables -
        attackers : list of squares from which square is attacked
        att_types : list of piece_types on attacking squares
        """

        # Check attacking pieces when engine is black
        if self.user == chess.WHITE:
            if self.board.is_attacked_by(chess.WHITE, move.to_square):
                attackers = list(self.board.attackers(chess.WHITE, move.to_square))
                att_types = []
                for att in attackers:
                    att_types.append(self.board.piece_at(att).piece_type)
                return att_types

        # Check attacking pieces when engine is white
        if self.user == chess.BLACK:
            if self.board.is_attacked_by(chess.BLACK, move.to_square):
                attackers = list(self.board.attackers(chess.BLACK, move.to_square))
                att_types = []
                for att in attackers:
                    att_types.append(self.board.piece_at(att).piece_type)
                return att_types


    def evaluate_board(self, board):
        """
        Make an overall evaluation of the board by piece-values and piece-square tables.
        positive (+) for white and negative (-) for black.

        - variables -
        piece : chess-piece on current square
        value : piece-square table value of piece
        total : overall board-evaluation
        """

        # iterate through all squares in board
        total = 0
        for sq in chess.SQUARES:
            piece = board.piece_at(sq)

            # continues if there is no piece on the square
            if not piece:
                continue
            
            # estimates value of piece by piece-square tables
            value = self.evaluate_piece(piece, sq)

            # adds value to overall board-evaluation
            if piece.color == chess.WHITE:
                total += value
            elif piece.color == chess.BLACK:
                total -= value
            
        return total
    

    def evaluate_board_2(self, move):
        """
        Make an overall evaluation of the board by piece-values and piece-square tables
        on the future position of the board.
        positive (+) for white and negative (-) for black.

        - variables -
        see evaluate_board()
        """

        tmp_board = self.board.copy()
        tmp_board.push(move)

        return self.evaluate_board(tmp_board)
    

    def move_is_check(self, move):
        """
        Checks if a move is a check
        """

        # make a copy of the board and push move to tmp_board
        tmp_board = self.board.copy()
        tmp_board.push(move)
        if tmp_board.is_check():
            return True
        return False
            

    def get_move_score(self, move):
        """
        Simple Move Evaluation Function. Tweak this to change the behavior of the engine.
        Uses all previously defined functions to estimate the best move.

        - input -
        move : a chess.Move object from the engine.Board

        - variables -
        score : the score of a given move
        loc_1, loc_2 : from and to squares related to the move
        piece : chess-piece on current board location.
        """


        score = 0
        loc_1 = move.from_square
        loc_2 = move.to_square
        piece = self.board.piece_at(loc_1)
        cur_attackers = self.under_attack_now(move)
        fut_attackers = self.under_attack_future(move)

        if self.is_capture(loc_2):
            capt_score = self.evaluate_capture(loc_2, loc_1)
            if capt_score == 0:
                if not fut_attackers:
                    score += 50
                else:
                    score -= 15
            elif capt_score == 1:
                score += 15
            elif capt_score == 2:
                score += 30
            elif capt_score == 3:
                score += 100
        
        if self.evaluate_piece(piece, loc_1) <= self.evaluate_piece(piece, loc_2):
            score += (self.evaluate_piece(piece, loc_2) - self.evaluate_piece(piece, loc_1))
        else:
            score -= 10
        
        if self.move_is_check(move):
            score += 10
        
        if self.user == chess.WHITE:
            if self.evaluate_board(self.board) < self.evaluate_board_2(move):
                score += 10
            else:
                score -= 10
        else:
            if self.evaluate_board(self.board) < self.evaluate_board_2(move):
                score -= 10
            else:
                score += 10
        
        if cur_attackers != None:
            if (
                piece.piece_type == 2 or piece.piece_type == 3 or 
                piece.piece_type == 4 or piece.piece_type == 5
                ):
                if 1 in cur_attackers:
                    score += 40
        
        if fut_attackers != None:
            if (
                piece.piece_type == 2 or piece.piece_type == 3 or 
                piece.piece_type == 4 or piece.piece_type == 5
                ):
                if 1 in fut_attackers:
                    score -= 30
            

        return score


    def get_best_move(self):
        """
        Gets move-values for all currently legal moves by iterating through
        legal moves and saving move-scores to a dictionary.

        Returns the best move according to the Simple Evaluation Algorithm.
        """

        all_moves = dict()

        # iterate through currently legal moves
        for move in self.board.legal_moves:

            score = self.get_move_score(move)
            all_moves[move] = score
        
        # create a sorted dictionary of move scores and pick best move
        moves = dict(sorted(all_moves.items(), key=lambda x:x[1], reverse=True))
        best_move = list(moves.items())[0][0]
        
        return best_move

