""""
Will contain multiple different move-evaluation algorithms 
"""
import chess



# evaluate whether the end-game stage has been reached
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