# python slot machine 
import random
def spin_row():
    symbols = ["🍒", "🍋", "🍊", "🍉", "⭐", "💎"]
    return [random.choice(symbols) for _ in range(3)]   
def print_row(row):
    print("****************************************")
    print(" | ".join(row))
    print("****************************************")
def get_payout(row, bet):
    if row[0] == row[1] == row[2]:
        return bet * 10  # Example payout logic
    return 0
def main():
    balance = 100  # Starting balance
    print("****************************************")
    print("Welcome to the Slot Machine!")
    print("Your starting balance is $", balance)
    print("symbols = [\"🍒\", \"🍋\", \"🍊\", \"🍉\", \"⭐\", \"💎\"]")
    print("****************************************")
    while balance > 0:
        print("\nCurrent balance: $", balance)
        bet = input("Enter your bet (or 'q' to quit): ")
        if bet.lower() == 'q':
            print("Thanks for playing!")
            break
        try:
            bet = int(bet)
            if bet <= 0 or bet > balance:
                print("Invalid bet amount. Please try again.")
                continue
        except ValueError:
            print("Please enter a valid number.")
            continue
        
        row = spin_row()
        print("Spinning....\n")
        print_row(row)
        
        if row[0] == row[1] == row[2]:
            payout = bet * 10  # Example payout logic
            balance += payout
            print("You won $", payout)
        elif row[0] == row[1] or row[1] == row[2] or row[0] == row[2]:
            payout = bet * 5
            balance += payout
            print("You won $", payout)
        else:
            balance -= bet
            print("You lost your bet of $", bet)

    print("Game over! Your final balance is $", balance)


if __name__ == "__main__":
    main()