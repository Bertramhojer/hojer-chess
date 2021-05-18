import chess
from constants import pieces
import evaluation
import time


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

        user = input("'w' to play as white or 'b' to play as black: ")
        user = chess.WHITE if user == 'w' else chess.BLACK

        engine = input("1) RandomEval   2) SimpleEval: ")

        if engine == '1':
            engine = evaluation.RandomEval(board, made_moves = list(), user=user)
        if engine == '2':
            engine = evaluation.SimpleEval(board, made_moves = list(), user=user)
            evaluations = list()

        if user == chess.WHITE:
            print(display(board))
            user_move = make_move(board)
            board.push(user_move)
            engine.made_moves.append(str(user_move))
            evaluations.append(engine.evaluate_board(board))
        
        while not board.is_game_over():

            # Check if we're in the opening
            if engine.is_opening():
                engine_move = engine.make_opening_move()
                if engine_move == None:
                    engine_move = engine.evaluate_move(board)
            else:
                engine_move = engine.evaluate_move(board)

            engine.made_moves.append(engine_move)
            board.push_san(str(engine_move))
            evaluations.append(engine.evaluate_board(board))
            print(f"\nEngine plays: {engine_move}")
            print(display(board))

            user_move = make_move(board)
            board.push(user_move)
            engine.made_moves.append(str(user_move))
            evaluations.append(engine.evaluate_board(board))
    
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
    """
    Displays the chess-board in terminal with unicode chess symbols as well as ranks and files.
    Inspired by Andrew Healey's terminal GUI which in turn is inspired by sunfish.
    Functions iterates over each square and changes letter value to its unicode representation and
    prints out the board in the user-terminal.

    Variables
    board_str : 127 chr iterable list-representation of the chessboard
    pieces : unicode chess pieces found in constants.py
    """

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


def make_move(board):

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
