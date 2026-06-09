import random

# Initialize board
board = ['1','2','3','4','5','6','7','8','9']

# Display the board
def display_board():
    print()
    print(f'{board[0]} | {board[1]} | {board[2]}')
    print('--+---+--')
    print(f'{board[3]} | {board[4]} | {board[5]}')
    print('--+---+--')
    print(f'{board[6]} | {board[7]} | {board[8]}')
    print()

# Check if someone has won
def check_winner(symbol):
    win_patterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # cols
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    for pattern in win_patterns:
        if all(board[i] == symbol for i in pattern):
            return True
    return False

# Check for tie
def is_tie():
    return all(space in ['X', 'O'] for space in board)

# Get list of available spots
def available_moves():
    return [i for i in range(9) if board[i] not in ['X', 'O']]

# Computer move
def computer_move():
    moves = available_moves()
    if moves:
        move = random.choice(moves)
        board[move] = 'X'
        print(f"Computer places 'X' in square {move+1}")

# User move
def user_move():
    while True:
        try:
            move = int(input("Enter your move (1-9): "))
            if move < 1 or move > 9:
                print("Invalid move. Choose between 1 and 9.")
                continue
            if board[move-1] in ['X', 'O']:
                print("That square is already taken.")
                continue
            board[move-1] = 'O'
            break
        except ValueError:
            print("Please enter a valid integer.")

# Game starts here
print("Welcome to Tic-Tac-Toe!")
# First move by computer in the center
board[4] = 'X'
display_board()

while True:
    # User's turn
    user_move()
    display_board()
    if check_winner('O'):
        print("You win! 🎉")
        break
    if is_tie():
        print("It's a tie!")
        break

    # Computer's turn
    computer_move()
    display_board()
    if check_winner('X'):
        print("Computer wins! 🤖")
        break
    if is_tie():
        print("It's a tie!")
        break
