import random
# Function to let one player play the guessing game
def play_game(player_name):
    number_to_guess = random.randint(1, 100)
    guesses = 0
    print(f"\n{player_name}, it's your turn to guess the number between 1 and 100.")

    while True:
        try:
            guess = int(input("Enter your guess: "))
            guesses += 1
            if guess < number_to_guess:
                print("Too low!")
            elif guess > number_to_guess:
                print("Too high!")
            else:
                print("You win!")
                print(f"{player_name}, you guessed it in {guesses} attempts.")
                return guesses
        except ValueError:
            print("Please enter a valid integer.")

# Start of the game
print("🎮 Welcome to the 2-Player Number Guessing Game!")

# Ask for both player names before starting
player1_name = input("Enter the name of Player 1: ")
player2_name = input("Enter the name of Player 2: ")

# Player 1's turn
print(f"\nNow it's {player1_name}'s turn:")
player1_attempts = play_game(player1_name)

# Player 2's turn
print(f"\nNow it's {player2_name}'s turn:")
player2_attempts = play_game(player2_name)

# Determine the winner
print("\n📢 Game Over! Let's see who wins:")
print(f"{player1_name} took {player1_attempts} guesses.")
print(f"{player2_name} took {player2_attempts} guesses.")

if player1_attempts < player2_attempts:
    print(f"🏆 {player1_name} wins!")
elif player2_attempts < player1_attempts:
    print(f"🏆 {player2_name} wins!")
else:
    print("🤝 It's a tie!")
# Thank the players for playing
print("\nThank you for playing the 2-Player Number Guessing Game! 🎉")
