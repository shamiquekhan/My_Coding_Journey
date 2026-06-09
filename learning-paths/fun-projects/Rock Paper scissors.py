import random
import time

# Emoji signs for gestures
emoji_signs = {
    "rock": "👊 Rock",
    "paper": "✋ Paper",
    "scissors": "✌️ Scissors"
}

options = ["rock", "paper", "scissors"]

def animate_choices():
    print("Rock...")
    time.sleep(0.5)
    print("Paper...")
    time.sleep(0.5)
    print("Scissors...")
    time.sleep(0.5)
    print("Shoot!")
    time.sleep(0.3)

def play_game():
    user_choice = input("Enter rock, paper, or scissors: ").lower()
    if user_choice not in options:
        print("❌ Invalid choice. Please try again.")
        return play_game()

    animate_choices()

    computer_choice = random.choice(options)

    # Show emoji hand signs
    print("\nYou chose:", emoji_signs[user_choice])
    print("Computer chose:", emoji_signs[computer_choice])

    # Determine winner
    if user_choice == computer_choice:
        print("🤝 It's a tie!")
    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "paper" and computer_choice == "rock") or \
         (user_choice == "scissors" and computer_choice == "paper"):
        print("🎉 You win!")
    else:
        print("😢 You lose!")

    # Replay option
    play_again = input("\nDo you want to play again? (yes/no): ").lower()
    if play_again == "yes":
        play_game()
    else:
        print("👋 Thanks for playing!")

play_game()
