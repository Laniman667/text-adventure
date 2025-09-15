import time
import random
from turtle import Screen

def cool_print(text, delay=0.00000005):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()

items = [
    "book",
    "burger (20HP, 10eng)",
    "diamond",
    "rubber duck",
    "rare sword",
    "common sword",
    "magic wand",
    "potion",
    "shield",
    "helmet",
    "unicorn",
    "vanilla ice cream (10HP, 25eng)",
    "key",
    "apple (5HP, 10eng)",
    "pizza (15HP 15eng)",
    "chocolate bar (0HP 40eng)",
    "soda (0HP, 50eng)",
    "candy cane (5HP 60eng)",
    "energy drink (0HP, 80eng)",
    "cake (15HP 60eng)"
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

def inventory_menu(inventory):
    cool_print(f"Your inventory: {inventory}")

def left():
    pass

def right():
    pass

def continue_game(direction):
    pass

command_actions = {
    "left": left,
    "right": right,
    "continue": continue_game
}

def get_input_with_inventory(prompt, inventory, hp, energy, max_hp, max_energy):
    while True:
        print(f"HP: {hp[0]}/{max_hp} | Energy: {energy[0]}/{max_energy}")
        user_input = input(prompt).lower().strip()
        
        #try:
        #   command_actions[user_input()]
        #except:
        #    continue

        if user_input == "inventory":
            cool_print(f"Your inventory: {inventory}")
        if user_input.startswith("use "):
            item_to_use = user_input[4:].strip()
            found = None
            for item in inventory:
                if item == item_to_use:
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
        elif user_input == "open map":
            if not "mysterious map" in inventory:
                cool_print("You don't have a map!")
            else:
                cool_print("You tested a map successfully!") #TODO: implement map
        elif user_input.startswith("equip "):
            item_to_equip = user_input[6:].strip()
            found = None
            for item in inventory:
                if item == item_to_equip:
                    found = item
                    break
            if found and ("sword" in found or "armor" in found):
                if "equipped" not in found:
                    inventory.remove(found)
                    equipped_item = f"{found} (equipped)"
                    inventory.append(equipped_item)
                    cool_print(f"You equipped the {found}.")
                else:
                    cool_print(f"You already have the {found} equipped.")
            else:
                cool_print(f"You can't equip {item_to_equip}.")
        else:
            pass
            return user_input

def adventure_path():
    inventory = []
    max_hp = 100
    max_energy = max_hp * 2
    hp = [max_hp]
    if hp == [0] <= 0:
        cool_print("You have 0 HP. Game over!")
        return
    cheat_code_die = max_hp - 100
    #work on cheat codes later
    energy = [max_energy]
    while True:
        cool_print("You're in a dark room, you see two paths, one to the left and one to the right.")
        cool_print("Type 'sleep' to save your progress at a bed. Type 'open map' to view your map if you have one.")
        cool_print("There is a safe bed here. Type 'sleep' to save your progress.")
        choice = get_input_with_inventory("left or right (or sleep): ", inventory, hp, energy, max_hp, max_energy)
        if choice == "sleep":
            while True:
                cool_print("You're in a dark room, you see two paths, one to the left and one to the right.")
                cool_print("Type 'sleep' to save your progress at a bed. Type 'open map' to view your map if you have one.")
                cool_print("There is a safe bed here. Type 'sleep' to save your progress.")
                choice = get_input_with_inventory("left or right (or sleep): ", inventory, hp, energy, max_hp, max_energy)
                if choice == "sleep":
                    last_sleep = "start"
                    hp[0] = max_hp // 2
                    energy[0] = max_energy
                    cool_print("You sleep and restore half your HP and all your energy. Progress saved!")
                    continue
                if choice == "left":
                    cool_print("You walk down the left path and find a treasure chest!")
                    # ...existing chest logic...
                    cool_print("You find a campfire and a bed. Type 'sleep' to save your progress.")
                    chest_choice = get_input_with_inventory("continue forward, turn back, or sleep: ", inventory, hp, energy, max_hp, max_energy)
                    if chest_choice == "sleep":
                        last_sleep = "chest"
                        hp[0] = max_hp // 2
                        energy[0] = max_energy
                        cool_print("You sleep and restore half your HP and all your energy. Progress saved!")
                        continue
                    # First fight in left path
                    cool_print("A shadowy beast leaps from the darkness!")
                    fight1 = get_input_with_inventory("attack, defend, or run: ", inventory, hp, energy, max_hp, max_energy)
                    if "attack" in fight1 and any("sword" in item and "equipped" in item for item in inventory):
                        cool_print("You attack with your sword and wound the beast!")
                    elif "defend" in fight1 and any("armor" in item and "equipped" in item for item in inventory):
                        cool_print("You defend with your armor and survive the attack!")
                    else:
                        cool_print("You are not properly equipped and the beast injures you!")
                        hp[0] -= 30
                    # Second fight in left path
                    cool_print("A second monster blocks your way!")
                    fight2 = get_input_with_inventory("attack, defend, or magic: ", inventory, hp, energy, max_hp, max_energy)
                    if "attack" in fight2 and any("sword" in item and "equipped" in item for item in inventory):
                        cool_print("You attack and defeat the monster!")
                    elif "defend" in fight2 and any("armor" in item and "equipped" in item for item in inventory):
                        cool_print("You defend and survive!")
                    elif "magic" in fight2 and any("wand" in item and "equipped" in item for item in inventory):
                        cool_print("You use magic and defeat the monster!")
                    else:
                        cool_print("You are not properly equipped and the monster injures you!")
                        hp[0] -= 30
                    cool_print("You find another bed here. Type 'sleep' to save your progress.")
                    bed_choice = get_input_with_inventory("continue, turn back, or sleep: ", inventory, hp, energy, max_hp, max_energy)
                    if bed_choice == "sleep":
                        last_sleep = "left_bed"
                        hp[0] = max_hp // 2
                        energy[0] = max_energy
                        cool_print("You sleep and restore half your HP and all your energy. Progress saved!")
                        continue
                elif choice == "right":
                    cool_print("You walk down the right path and encounter a monster!")
                    cool_print("There is a safe bed here. Type 'sleep' to save your progress before fighting.")
                    sleep_choice = get_input_with_inventory("fight, run, or sleep: ", inventory, hp, energy, max_hp, max_energy)
                    if sleep_choice == "sleep":
                        last_sleep = "right_monster"
                        hp[0] = max_hp // 2
                        energy[0] = max_energy
                        cool_print("You sleep and restore half your HP and all your energy. Progress saved!")
                        continue
                    # First fight in right path
                    cool_print("A giant rat attacks!")
                    fight1 = get_input_with_inventory("attack, defend, or run: ", inventory, hp, energy, max_hp, max_energy)
                    if "attack" in fight1 and any("sword" in item and "equipped" in item for item in inventory):
                        cool_print("You attack with your sword and defeat the rat!")
                    elif "defend" in fight1 and any("armor" in item and "equipped" in item for item in inventory):
                        cool_print("You defend with your armor and survive!")
                    else:
                        cool_print("You are not properly equipped and the rat injures you!")
                        hp[0] -= 20
                    # Second fight in right path
                    cool_print("A second monster appears! Prepare for battle.")
                    fight2 = get_input_with_inventory("attack, defend, or magic: ", inventory, hp, energy, max_hp, max_energy)
                    if "attack" in fight2 and any("sword" in item and "equipped" in item for item in inventory):
                        cool_print("You attack and defeat the monster!")
                    elif "defend" in fight2 and any("armor" in item and "equipped" in item for item in inventory):
                        cool_print("You defend and survive!")
                    elif "magic" in fight2 and any("wand" in item and "equipped" in item for item in inventory):
                        cool_print("You use magic and defeat the monster!")
                    else:
                        cool_print("You are not properly equipped and the monster injures you!")
                        hp[0] -= 30
                    cool_print("You find another bed here. Type 'sleep' to save your progress.")
                    bed_choice = get_input_with_inventory("continue, turn back, or sleep: ", inventory, hp, energy, max_hp, max_energy)
                    if bed_choice == "sleep":
                        last_sleep = "right_bed"
                        hp[0] = max_hp // 2
                        energy[0] = max_energy
                        cool_print("You sleep and restore half your HP and all your energy. Progress saved!")
                        #continue
            if choice == "right":
                cool_print("You walk down the right path and encounter a monster!")
                cool_print("There is a safe bed here. Type 'sleep' to save your progress before fighting.")
                sleep_choice = get_input_with_inventory("fight, run, or sleep: ", inventory, hp, energy, max_hp, max_energy)
                if sleep_choice == "sleep":
                    last_sleep = "right_monster"
                    hp[0] = max_hp // 2
                    energy[0] = max_energy
                    cool_print("You sleep and restore half your HP and all your energy. Progress saved!")
                    continue
                # First fight in right path
                cool_print("A giant rat attacks!")
                fight1 = get_input_with_inventory("attack, defend, or run: ", inventory, hp, energy, max_hp, max_energy)
                if "attack" in fight1 and any("sword" in item and "equipped" in item for item in inventory):
                    cool_print("You attack with your sword and defeat the rat!")
                elif "defend" in fight1 and any("armor" in item and "equipped" in item for item in inventory):
                    cool_print("You defend with your armor and survive!")
                else:
                    cool_print("You are not properly equipped and the rat injures you!")
                    hp[0] -= 20
                # Second fight in right path
                cool_print("A second monster appears! Prepare for battle.")
                fight2 = get_input_with_inventory("attack, defend, or magic: ", inventory, hp, energy, max_hp, max_energy)
                if "attack" in fight2 and any("sword" in item and "equipped" in item for item in inventory):
                    cool_print("You attack and defeat the monster!")
                elif "defend" in fight2 and any("armor" in item and "equipped" in item for item in inventory):
                    cool_print("You defend and survive!")
                elif "magic" in fight2 and any("wand" in item and "equipped" in item for item in inventory):
                    cool_print("You use magic and defeat the monster!")
                else:
                    cool_print("You are not properly equipped and the monster injures you!")
                    hp[0] -= 30
                cool_print("You find another bed here. Type 'sleep' to save your progress.")
                bed_choice = get_input_with_inventory("continue, turn back, or sleep: ", inventory, hp, energy, max_hp, max_energy)
                if bed_choice == "sleep":
                    last_sleep = "right_bed"
                    hp[0] = max_hp // 2
                    energy[0] = max_energy
                    cool_print("You sleep and restore half your HP and all your energy. Progress saved!")
                    continue
                lonely_choice4 = get_input_with_inventory("read the letters or keep moving: ", inventory, hp, energy, max_hp, max_energy)
                if lonely_choice4 == "read":
                    cool_print("You read the letters, learning about the hopes and dreams of those who came before. Their words comfort you and inspire you to keep going.")
                else:
                    cool_print("You keep moving, determined to escape. The loneliness weighs on you, but you press forward.")
                cool_print("When you finally find the exit, you pause. The world outside is vast, but you feel small and alone.")
                cool_print("You walk away from the lost prison, determined to reach out to others, to heal, and to grow.")
                cool_print("LONELY ENDING: You survived, but at the price of connection. What will you do next?")
                break
            else:
                cool_print("You hesitate, and the prisoner leaves you behind. You are alone in the darkness.")
                cool_print("TRAGIC ENDING")
                break
        # ...existing code...
            # ...existing code...
                if choice == "left":
                    cool_print("You walk down the left path and find a treasure chest!")
                    # ...existing chest logic...
                    cool_print("You find a campfire and a bed. Type 'sleep' to save your progress.")
                    chest_choice = get_input_with_inventory("continue forward, turn back, or sleep: ", inventory, hp, energy, max_hp, max_energy)
                    if chest_choice == "sleep":
                        last_sleep = "chest"
                        hp[0] = max_hp // 2
                        energy[0] = max_energy
                        cool_print("You sleep and restore half your HP and all your energy. Progress saved!")
                        continue
                    # First fight in left path
                    cool_print("A shadowy beast leaps from the darkness!")
                    fight1 = get_input_with_inventory("attack, defend, or run: ", inventory, hp, energy, max_hp, max_energy)
                    if "attack" in fight1 and any("sword" in item and "equipped" in item for item in inventory):
                        cool_print("You attack with your sword and wound the beast!")
                    elif "defend" in fight1 and any("armor" in item and "equipped" in item for item in inventory):
                        cool_print("You defend with your armor and survive the attack!")
                    else:
                        cool_print("You are not properly equipped and the beast injures you!")
                        hp[0] -= 30
                    # Second fight in left path
                    cool_print("A second monster blocks your way!")
                    fight2 = get_input_with_inventory("attack, defend, or magic: ", inventory, hp, energy, max_hp, max_energy)
                    if "attack" in fight2 and any("sword" in item and "equipped" in item for item in inventory):
                        cool_print("You attack and defeat the monster!")
                    elif "defend" in fight2 and any("armor" in item and "equipped" in item for item in inventory):
                        cool_print("You defend and survive!")
                    elif "magic" in fight2 and any("wand" in item and "equipped" in item for item in inventory):
                        cool_print("You use magic and defeat the monster!")
                    else:
                        cool_print("You are not properly equipped and the monster injures you!")
                        hp[0] -= 30
                    cool_print("You find another bed here. Type 'sleep' to save your progress.")
                    bed_choice = get_input_with_inventory("continue, turn back, or sleep: ", inventory, hp, energy, max_hp, max_energy)
                    if bed_choice == "sleep":
                        last_sleep = "left_bed"
                        hp[0] = max_hp // 2
                        energy[0] = max_energy
                        cool_print("You sleep and restore half your HP and all your energy. Progress saved!")
                        continue
                        energy[0] = min(energy[0] + 20, max_energy)
                    else:
                        cool_print("Invalid choice. Restarting...")
                elif dodge == "right":
                    cool_print("You dodge right and the monster hits you! You lose!")
                    hp[0] = 0
                else:
                    cool_print("Invalid choice.")
            if ForR == "run":
                cool_print("you try to run away but the monster is faster! You lose!")
                hp[0] = 0
            if hp[0] <= 0:
                cool_print("You have 0 HP. Game over!")
                break
            cool_print("Invalid choice. Bye!")
            break

        if hp[0] <= 0:
            cool_print("You have 0 HP. Game over!")
            break

        again = get_input_with_inventory("Do you want to continue down this path or turn back and try the other path? (continue/turn back): ", inventory, hp, energy, max_hp, max_energy)
        if choice == "left" and again == "turn back":
            # Only allow going right, not back to chest
            cool_print("You go back and can only go right now.")
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
            if hp[0] <= 0:
                cool_print("You have 0 HP. Game over!")
                break
            break
        elif choice == "left" and again == "continue":
            # New story branch: slip down a slope and find a lost prisoner
            cool_print("You continue forward, but suddenly the ground gives way!")
            cool_print("You slip down a steep slope, tumbling and sliding until you land in a dimly lit cavern.")
            cool_print("As you stand up and dust yourself off, you hear a faint voice calling for help.")
            cool_print("You follow the sound and discover a lost prisoner chained to the wall.")
            cool_print("The prisoner looks at you with hope in their eyes. Will you try to help them escape?")
            prisoner_choice = get_input_with_inventory("help or leave: ", inventory, hp, energy, max_hp, max_energy)
            if prisoner_choice == "help":
                cool_print("You search the cavern and find a rusty key nearby.")
                cool_print("You unlock the chains and free the prisoner. They thank you and give you a mysterious map as a reward!")
                inventory.append("mysterious map")
                cool_print("You now have a mysterious map in your inventory.")
            else:
                cool_print("You decide to leave the prisoner behind and continue your adventure alone.")
            break
        elif again == "turn back":
            continue
        else:
            break

adventure_path()
#print("i'm dead")
# --- Simple Pygame Map Example ---
