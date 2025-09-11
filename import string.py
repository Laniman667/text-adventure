import string
import time
import random

def cool_print(text, delay=0.05):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()

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
    "key",
    "apple",
    "pizza",
    "chocolate bar",
    "soda",
    "candy cane",
    "energy drink",
    "cake"
]

# Food items and their heal/energy values
food_items = {
    "burger (20HP, 10eng)":      {"hp": 20, "energy": 10},
    "vanilla ice cream (10HP, 25eng)": {"hp": 10, "energy": 25},
    "apple (5HP, 10eng)":       {"hp": 5,  "energy": 10},
    "pizza (15HP 15eng)":       {"hp": 15, "energy": 15},
    "chocolate bar (0HP 40eng)": {"hp": 0, "energy": 40},  # sugary
    "soda (0HP, 50eng)":        {"hp": 0,  "energy": 50},  # very sugary
    "candy cane (5HP 60eng)":  {"hp": 5,  "energy": 60},  # very sugary
    "energy drink (0HP, 80eng)": {"hp": 0, "energy": 80},  # super sugary
    "cake (15HP 60eng)":        {"hp": 10, "energy": 60}
}

def get_input_with_inventory(prompt, inventory, hp, energy, max_hp, max_energy):
    while True:
        print(f"HP: {hp[0]}/{max_hp} | Energy: {energy[0]}/{max_energy}")
        user_input = input(prompt)
        if user_input.lower() == "inventory":
            cool_print(f"Your inventory: {inventory}")
        elif user_input.lower().startswith("use "):
            item_to_use = user_input[4:].strip().lower()
            found = None
            for item in inventory:
                if item.lower() == item_to_use:
                    found = item
                    break
            if found:
                if found in food_items:
                    heal = food_items[found]["hp"]
                    energize = food_items[found]["energy"]
                    old_hp = hp[0]
                    old_energy = energy[0]
                    hp[0] = min(hp[0] + heal, max_hp)
                    energy[0] = min(energy[0] + energize, max_energy)
                    inventory.remove(found)
                    msg = f"You eat the {found}."
                    if heal > 0:
                        msg += f" Healed {hp[0] - old_hp} HP."
                    if energize > 0:
                        msg += f" Restored {energy[0] - old_energy} energy."
                    cool_print(msg + f" (HP: {hp[0]}/{max_hp}, Energy: {energy[0]}/{max_energy})")
                else:
                    cool_print(f"You can't use the {found} right now.")
            else:
                cool_print(f"You don't have a {item_to_use}.")
        else:
            return user_input

def adventure_path():
    inventory = []
    max_hp = 100
    max_energy = max_hp * 2
    hp = [max_hp]
    if hp = [0] <= 0:
        cool_print("You have 0 HP. Game over!")
        return
    cheat_code_die = max_hp - 100
    #work on cheat codes later
    energy = [max_energy]
    while True:
        cool_print("you're in a dark room, you see two paths, one to the left and one to the right.")
        choice = get_input_with_inventory(" left or right: ", inventory, hp, energy, max_hp, max_energy)

        if choice == "left":
            cool_print("you walk down the left path and find a treasure chest!")
            found_item = random.choice(items)
            inventory.append(found_item)
            if found_item.startswith("money"):
                amount = found_item.split("(")[1].split(")")[0]
                cool_print(f"you open the treasure chest and find {amount} gold coins! You win!")
            else:
                num_items = random.randint(1, 3)
                found_items = random.sample(items, num_items)
                inventory.extend(found_items)
                cool_print(f"You open the treasure chest and find: {', '.join(found_items)}!") 
            cool_print(f"Your inventory: {inventory}")
        elif choice == "right":
            cool_print("you walk down the right path and encounter a monster!")
            cool_print("The monster starts to attack you, do you fight or run?")
            ForR = get_input_with_inventory("fight or run: ", inventory, hp, energy, max_hp, max_energy)
            if ForR == "fight":
                monster_hp = 100
                cool_print("Do you dodge left or right?")
                dodge = get_input_with_inventory("left (30 energy) or right (30 energy): ", inventory, hp, energy, max_hp, max_energy)
                if dodge == "left":
                    monster_hp //= 2
                    energy = [max(0, energy[0] - 30)]
                    cool_print(f"You dodge left and take no damage! You hit the monster for {monster_hp} damage (half its HP)!")
                    cool_print("it starts to attack you again, do you run towards it or jump back? ")
                    action = get_input_with_inventory("run or jump: ", inventory, hp, energy, max_hp, max_energy)
                    if action == "run":
                        cool_print("You run towards the monster and it kicks you! You lose!")
                        hp[0] = 0
                    elif action == "jump":
                        cool_print("You jump back and the monster misses! You hit it again and defeat it!")
                        # Maybe restore some energy for a win
                        energy[0] = min(energy[0] + 20, max_energy)
                    else:
                        cool_print("Invalid choice. Restarting...")
                elif dodge == "right":
                    cool_print("You dodge right and the monster hits you! You lose!")
                    hp[0] = 0
                else:
                    cool_print("Invalid choice.")
            elif ForR == "run":
                cool_print("you try to run away but the monster is faster! You lose!")
                hp[0] = 0
            else:
                cool_print("Invalid choice. Bye!")
        else:
            cool_print("Invalid choice. Bye!")
            break

        if hp[0] <= 0:
            cool_print("You have 0 HP. Game over!")
            break

        again = get_input_with_inventory("Do you want to continue down this path or turn back and try the other path? (continue/turn back): ", inventory, hp, energy, max_hp, max_energy)
        if again.lower() == "turn back":
            continue
        else:
            break

# Opening message with effect
cool_print("Actions: Type 'inventory' at any prompt to see your current items, type \"use (item_name)\" to use an item if applicable. type \"equip (item_name)\" to equip items (like swords). At certain points you can sleep, sleeping will restore 1/2 of your HP and all of your energy, sleeping can leave you vulnerable to monsters, so be careful!")
cool_print("how is your day?")
choice = input("(good or bad): ")

if choice == "good":
    cool_print("thats great!", delay=0.0005)
    cool_print("make a name for your character:")
    username = input()
    cool_print(f"Welcome, {username}! Lets begin!", delay=0.0005)
elif choice == "bad":
    cool_print("oh no! Well maybe wait to play the game later.")
    exit()
else:
    cool_print("Invalid choice. Bye!")
    exit()

adventure_path()
