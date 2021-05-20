import chess
from constants import pieces
import evaluation
import matplotlib.pyplot as plt


def play():
    """
    Runs the chess engine allowing for play with oneself or AI.

    - variables -
    board : instantiation of the chess.Board class from the python-chess library
    game_mode : specifies the game-mode
    engine : specifies the evaluation-algorithm to be used for playing
    engine_move : the best move according to the evaluation algorithm
    user_move : the move entered by the user
    """


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

        while True:
            user = input("'w' to play as white or 'b' to play as black: ")
            if user == 'w':
                user = chess.WHITE
                break
            elif user == 'b':
                user = chess.BLACK
                break
            else:
                print("Please enter either 'w' or 'b'")

        while True:
            engine = input("Enter 1 or 2: \n1) Random Move AI \n2) Simple Evaluation Algorithm AI\n")
            if engine == '1':
                engine = evaluation.RandomEval(board, made_moves = list(), user=user)
                break
            elif engine == '2':
                engine = evaluation.SimpleEval(board, made_moves = list(), user=user)
                evaluations = list()
                break

        if user == chess.WHITE:
            print(display(board))
            user_move = make_move(board)
            engine.board.push(user_move)
            engine.made_moves.append(str(user_move))
            evaluations.append(engine.evaluate_board(engine.board))
        
        while not board.is_game_over():

            # Check if we're in the opening
            if engine.is_opening():
                engine_move = engine.make_opening_move()
                # no opening move found
                if engine_move == None:
                    engine_move = engine.get_best_move()
            else:
                engine_move = engine.get_best_move()

            # push the engine move to the board and display board
            engine.made_moves.append(str(engine_move))
            engine.board.push_san(str(engine_move))
            evaluations.append(engine.evaluate_board(engine.board))
            print(f"\nEngine plays: {engine_move}")
            print(display(engine.board))

            # get move from user
            user_move = make_move(board)
            if user_move == 'resign':
                break
            engine.board.push(user_move)
            engine.made_moves.append(str(user_move))
            evaluations.append(engine.evaluate_board(engine.board))
    
    else:
        print("Invalid input - enter '1' or '2'")
        try:
            play()
        except KeyboardInterrupt:
            pass

    # check game-result
    if board.result() == "1-0":
        print("White wins!")
    elif board.result() == "0-1":
        print("Black wins!")
    elif user_move == 'resign':
        print(f"User has resigned!")
    else:
        print("Game ends in a draw!")
    
    # display the move-evaluation as evaluated by the engine
    visualize_game(engine.made_moves, evaluations)


def display(board):
    """
    Displays the chess-board in terminal with unicode chess symbols as well
    as ranks and files. Inspired by Andrew Healey's terminal GUI.
    https://healeycodes.com/building-my-own-chess-engine/

    Iterates the board and represents letter by unicode symbols.

    - variables - 
    board_str : iterable chr-list
    pieces : unicode chess pieces found in constants.py
    """

    # create list representation of chess-board
    board_str = list(str(board))

    # iterate through board-elements
    for i, piece in enumerate(board_str):
        if piece in pieces:
            board_str[i] = pieces[piece]

    ranks = ["1", "2", "3", "4", "5", "6", "7", "8"]
    uni_board = []

    # add rank and file labels to board
    for rank in "".join(board_str).split("\n"):
        uni_board.append(f"  {ranks.pop()} {rank}")

    if board.turn == chess.BLACK:
        uni_board.reverse()

    uni_board.append("    a b c d e f g h")

    return "\n" + "\n".join(uni_board)


def visualize_game(x, y):
    """
    Plots a simple line-graph of the board-evaluation.

    - variables -
    x (list of strings) : list of move-values
    y (list of ints) : list of board-evaluation at each move
    """

    x.insert(0, 'start')
    y.insert(0, 0)

    plt.plot(x, y, color='red', marker='o')
    plt.title('Board Evaluation Throughout Game', fontsize=14)
    plt.xlabel('Move', fontsize=12)
    plt.xticks(rotation = 90)
    plt.ylabel('Evaluation', fontsize=12)
    plt.grid(True)
    plt.show()


def make_move(board):
    """
    Gets a move from user and returns chess.Move object.
    """

    move = input("('?') for legal moves\nYour move:\n")

    if move == '?':
        print("Legal moves are")
        for legal_move in board.legal_moves:
            print(legal_move, end=", ")
        print("\n")
    elif move == 'resign':
        return 'resign'
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