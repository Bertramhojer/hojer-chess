import chess
from constants import pieces
import evaluation
# import engines

def play():

    # instantiate the board
    board = chess.Board()

    game_mode = input("Please choose game-mode.\nType '1' to play without AI, type '2' to play with AI: \n")

    if game_mode == '1':
        while True:
            if board.is_game_over() == True:
                print(display(board))
                break
            else:
                print(display(board))
                if board.turn == True: # True if White to move
                    print(" -- White to move --")
                else:
                    print(" -- Black to move --")
                board.push(make_move(board))

    elif game_mode == '2':
        user = (
            chess.WHITE if input("Play as [w]hite or [b]lack: " == "w") else chess.BLACK
            )
        
        if user == chess.WHITE:
            print(display(board))
            board.push(make_move(board))
        
        while not board.is_game_over():
            board.push(next_move(get_depth(), board, debug=False))
            print(display(board))
            board.push(make_move(board))
    
    else:
        print("Invalid input - enter '1' or '2'")
        try:
            play()
        except KeyboardInterrupt:
            pass

    if board.result() == "1-0":
        print("White wins!")
    elif board.result() == "0-1":
        print("Black wins!")
    else:
        print("Game ends in a draw!")


def display(board):

    board_str = list(str(board))

    for i, piece in enumerate(board_str):
        if piece in pieces:
            board_str[i] = pieces[piece]

    ranks = ["1", "2", "3", "4", "5", "6", "7", "8"]
    uni_board = []

    for rank in "".join(board_str).split("\n"):
        uni_board.append(f"  {ranks.pop()} {rank}")
    if board.turn == chess.BLACK:
        uni_board.reverse()
    uni_board.append("    a b c d e f g h")

    return "\n" + "\n".join(uni_board)


def make_move(board: chess.Board) -> chess.Move:

    move = input("('?') for legal moves\nYour move:\n")

    if move == '?':
        print("Legal moves are")
        for legal_move in board.legal_moves:
            print(legal_move, end=", ")
        print("\n")
    else:
        for legal_move in board.legal_moves:
            if move == str(legal_move):
                return legal_move
    return make_move(board)


if __name__ == "__main__":
    try:
        play()
    except KeyboardInterrupt:
        pass

