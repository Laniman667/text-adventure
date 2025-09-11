import string
import time
import random

items = [
    f"money ({random.randint(1, 100)})",
    "book",
    "burger",
    "diamond",
    "rubber duck",
    "rare sword",
    "common sword",
    "magic wand",
    "potion",
    "shield",
    "helmet",
    "unicorn",
    "vanilla ice cream",
    "key"
]

# Opening message with effect
text = "how is your day?"
output = ""
for target_ch in text:
    for ch in string.printable:
        print(f"Trying: {output + ch}", end='\r')
        time.sleep(0.001)
        if ch == target_ch:
            output += ch
            break
print(f"\nFinal output: {output}")

# Good or bad choice
choice = input("(good or bad): ")

if choice == "good":
    text2 = "thats great!"
    output2 = ""
    for target_ch in text2:
        for ch in string.printable:
            print(f"Trying: {output2 + ch}", end='\r')
            time.sleep(0.0005)
            if ch == target_ch:
                output2 += ch
                break
    print(f"\nFinal output: {output2}")

    # Username prompt with effect
    text3 = "make a name for your character:"
    output3 = ""
    for target_ch in text3:
        for ch in string.printable:
            print(f"Trying: {output3 + ch}", end='\r')
            time.sleep(0.001)
            if ch == target_ch:
                output3 += ch
                break
    print(f"\nFinal output: {output3}")
    username = input()  # Let the user type their name

    welcome_text = f"Welcome, {username}! Lets begin!"
    welcome_output = ""
    for target_ch in welcome_text:
        for ch in string.printable:
            print(f"Trying: {welcome_output + ch}", end='\r')
            time.sleep(0.0005)
            if ch == target_ch:
                welcome_output += ch
                break
    print(f"\nFinal output: {welcome_output}")

elif choice == "bad":
    text2 = "oh no! Well maybe wait to play the game later."
    output2 = ""
    for target_ch in text2:
        for ch in string.printable:
            print(f"Trying: {output2 + ch}", end='\r')
            time.sleep(0.001)
            if ch == target_ch:
                output2 += ch
                break
    print(f"\nFinal output: {output2}")
else:
    print("Invalid choice. Bye!")
    exit()

# Adventure path
print("you're in a dark room, you see two paths, one to the left and one to the right.")
choice = input(" left or right: ")

inventory = []  # Create an empty inventory list

if choice == "left":
    text3 = "you walk down the left path and find a treasure chest!"
    output3 = ""
    for target_ch in text3:
        for ch in string.printable:
            print(f"Trying: {output3 + ch}", end='\r')
            time.sleep(0.001)
            if ch == target_ch:
                output3 += ch
                break
    print(f"\nFinal output: {output3}")

    # Give a random item from the list
    found_item = random.choice(items)
    inventory.append(found_item)  # Add the found item to the inventory

    if found_item.startswith("money"):
        amount = found_item.split("(")[1].split(")")[0]
        text4 = f"you open the treasure chest and find {amount} gold coins! You win!"
    else:
        text4 = f"you open the treasure chest and find a {found_item}! You win!"
    output4 = ""
    for target_ch in text4:
        for ch in string.printable:
            print(f"Trying: {output4 + ch}", end='\r')
            time.sleep(0.001)
            if ch == target_ch:
                output4 += ch
                break
    print(f"\nFinal output: {output4}")

    # Show inventory to the user
    print(f"Your inventory: {inventory}")

elif choice == "right":
    text3 = "you walk down the right path and encounter a monster!"
    output3 = ""
    for target_ch in text3:
        for ch in string.printable:
            print(f"Trying: {output3 + ch}", end='\r')
            time.sleep(0.001)
            if ch == target_ch:
                output3 += ch
                break
    print(f"\nFinal output: {output3}")

    text4 = "The monster starts to attack you, do you fight or run?"
    output4 = ""
    for target_ch in text4:
        for ch in string.printable:
            print(f"Trying: {output4 + ch}", end='\r')
            time.sleep(0.001)
            if ch == target_ch:
                output4 += ch
                break
    print(f"\nFinal output: {output4}")

    ForR = input("fight or run: ")
    if ForR == "fight":
        monster_hp = 100

        text5 = "Do you dodge left or right?"
        output5 = ""
        for target_ch in text5:
            for ch in string.printable:
                print(f"Trying: {output5 + ch}", end='\r')
                time.sleep(0.001)
                if ch == target_ch:
                    output5 += ch
                    break
        print(f"\nFinal output: {output5}")

        dodge = input("left or right: ")
        if dodge == "left":
            monster_hp //= 2
            print(f"You dodge left and take no damage! You hit the monster for {monster_hp} damage (half its HP)!")
        elif dodge == "right":
            print("You dodge right and the monster hits you! You lose!")
        else:
            print("Invalid choice.")
    elif ForR == "run":
        text6 = "you try to run away but the monster is faster! You lose!"
        output6 = ""
        for target_ch in text6:
            for ch in string.printable:
                print(f"Trying: {output6 + ch}", end='\r')
                time.sleep(0.001)
                if ch == target_ch:
                    output6 += ch
                    break
        print(f"\nFinal output: {output6}")
    else:
        print("Invalid choice. Bye!")
else:
    print("Invalid choice. Bye!")