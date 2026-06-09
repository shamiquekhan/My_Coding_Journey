import random
# Snake, Water, Gun Game
print("Welcome to the Snake, Water, Gun game!")
computer = random.choice([1, -1, 0])  # 1 for Snake, -1 for Water, 0 for Gun
print("Computer has made its choice.")
youstr=input("Enter your choice ")
print("Choices are s for Snake, w for Water, g for Gun")
if youstr not in ["s", "w", "g"]:
    print("Invalid choice! Please enter 's', 'w', or 'g'.")
    exit()
youdict={"s":1,"w":-1,"g":0}
you=youdict[youstr]
if(computer==1 and you==1):
    print("It's a tie!")
#     print(f"{num} x {i} = {num * i}")  # This will print the multiplication table of the number
elif(computer==1 and you==-1):
    print("You lose!")
elif(computer==1 and you==0):
    print("You win!")
elif(computer==-1 and you==1):
    print("You win!")
elif(computer==-1 and you==-1):
    print("It's a tie!")
elif(computer==-1 and you==0):
    print("You lose!")
elif(computer==0 and you==1):
    print("You lose!")
elif(computer==0 and you==-1):
    print("You win!")
else:
    print("It's a tie!")  # This will handle the case when both choices are the same
