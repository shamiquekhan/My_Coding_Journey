# python credit card validator
card=input("Enter your credit card number: ")
sum_odd_digits=0
sum_even_digits=0
total =0
card=card.replace(" ", "")  # Remove spaces if any
card=card.replace("-", "")  # Remove dashes if any
card=card[::-1]  # Reverse the card number
for x in card[::2]:
    sum_odd_digits+=int(x)
for y in card[1::2]:
    y=int(y)*2
    if y>9:
        y-=9
    sum_even_digits+=y
total=sum_odd_digits+sum_even_digits
if total%10==0:
    print("Valid credit card number.")
else:
    print("Invalid credit card number.")

# if not card.isdigit():
#     print("Invalid credit card number. Only digits are allowed.")
# elif len(card) < 13 or len(card) > 19:
#     print("Invalid credit card number.")
# else:
#     print("Valid credit card number.")
