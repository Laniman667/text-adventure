import string
import time
import random

def cool_print(text, delay=0.05):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()

items = [
    "book", "burger", "diamond", "rubber duck", "rare sword", "common sword",
    "magic wand", "potion", "shield", "helmet", "unicorn", "vanilla ice cream",
    "key", "apple", "pizza", "chocolate bar", "soda", "candy cane",
    "energy drink", "cake", "chestplate"
]

def get_money():
    return f"money ({random.randint(1, 100)})"

food_items = {
    "burger": {"hp": 20, "energy": 10, "display": "burger (20HP, 10eng)"},
    "vanilla ice cream": {"hp": 10, "energy": 25, "display": "vanilla ice cream (10HP, 25eng)"},
    "apple": {"hp": 5, "energy": 10, "display": "apple (5HP, 10eng)"},
    "pizza": {"hp": 15, "energy": 15, "display": "pizza (15HP, 15eng)"},
    "chocolate bar": {"hp": 0, "energy": 40, "display": "chocolate bar (0HP, 40eng)"},
    "soda": {"hp": 0, "energy": 50, "display": "soda (0HP, 50eng)"},
    "candy cane": {"hp": 5, "energy": 60, "display": "candy cane (5HP, 60eng)"},
    "energy drink": {"hp": 0, "energy": 80, "display": "energy drink (0HP, 80eng)"},
    "cake": {"hp": 10, "energy": 60, "display": "cake (15HP, 60eng)"}
}

weapons = {"rare sword", "common sword", "magic wand"}
armor = {"shield", "helmet", "chestplate"}

cheat_codes = {
    "89257925": {"action": "remove_hp", "value": 20, "message": "Cheat code activated: 20 HP removed!"},
    "92575235": {"action": "remove_energy", "value": 20, "message": "Cheat code activated: 20 energy removed!"},
    "12345678": {"action": "add_hp", "value": 20, "message": "Cheat code activated: 20 HP added!"},
    "87654321": {"action": "add_energy", "value": 20, "message": "Cheat code activated: 20 energy added!"},
    "11223344": {"action": "full_restore_hp", "message": "Cheat code activated: HP fully restored!"},
    "44332211": {"action": "full_restore_energy", "message": "Cheat code activated: Energy fully restored!"},
    "55667788": {"action": "add_item", "value": "rare sword", "message": "Cheat code activated: Rare sword added to inventory!"},
    "88776655": {"action": "add_item", "value": "shield", "message": "Cheat code activated: Shield added to inventory!"},
    "12121212": {"action": "add_item", "value": "soda", "message": "Cheat code activated: Soda added to inventory!"},
    "34343434": {"action": "add_item", "value": "pizza", "message": "Cheat code activated: Pizza added to inventory!"},
    "56565656": {"action": "add_item", "value": "money (50)", "message": "Cheat code activated: 50 gold coins added to inventory!"},
    "78787878": {"action": "clear_inventory", "message": "Cheat code activated: Inventory cleared!"},
    "99999999": {"action": "win_fight", "message": "Cheat code activated: Monster instantly defeated!"}
}

def get_damage_multiplier(equipped_weapon):
    if equipped_weapon and equipped_weapon[0] == "rare sword":
        return 2.0
    if equipped_weapon and equipped_weapon[0] == "common sword":
        return 1.35
    return 1.0

def apply_damage_to_player(damage, equipped_armor, hp, max_hp):
    if equipped_armor:
        armor_type = equipped_armor[0]
        if armor_type == "shield" and random.random() < 0.5:
            cool_print("Your shield deflected the attack!")
            return
        elif armor_type == "helmet":
            damage = int(damage * 0.75)
            cool_print(f"Your helmet reduced the damage to {damage}!")
        elif armor_type == "chestplate":
            damage = int(damage * 0.5)
            cool_print(f"Your chestplate reduced the damage to {damage}!")
    hp[0] -= damage
    if damage > 0:
        cool_print(f"Took {damage} damage. (HP: {hp[0]}/{max_hp})")

def display_status(hp, max_hp, energy, max_energy, equipped_weapon, equipped_armor):
    print(f"HP: {hp[0]}/{max_hp} | Energy: {energy[0]}/{max_energy} | Equipped Weapon: {equipped_weapon or 'None'} | Equipped Armor: {equipped_armor or 'None'}")

def handle_eat_drink(command, item_name, inventory, hp, energy, max_hp, max_energy):
    found = None
    food_key_found = None
    for item in inventory:
        for food_key, food_data in food_items.items():
            if item == food_data["display"] and (item_name == food_key or item_name in food_key):
                found = item
                food_key_found = food_key
                break
        if found:
            break
    if found and food_key_found:
        heal = food_items[food_key_found]["hp"]
        energize = food_items[food_key_found]["energy"]
        old_hp, old_energy = hp[0], energy[0]
        hp[0] = min(hp[0] + heal, max_hp)
        energy[0] = min(energy[0] + energize, max_energy)
        inventory.remove(found)
        msg = f"You {'drink' if food_key_found in ['soda', 'energy drink'] else 'eat'} the {food_items[food_key_found]['display']}."
        if heal > 0:
            msg += f" Healed {hp[0] - old_hp} HP."
        if energize > 0:
            msg += f" Restored {energy[0] - old_energy} energy."
        cool_print(msg + f" (HP: {hp[0]}/{max_hp}, Energy: {energy[0]}/{max_energy})")
        return True
    cool_print(f"You can't {'drink' if command == 'drink' else 'eat'} {item_name}. It's either not in your inventory or not consumable.")
    return False

def handle_equip(item_name, inventory, equipped_weapon, equipped_armor):
    found = next((item for item in inventory if item.lower() == item_name), None)
    if found and found in weapons:
        if equipped_weapon:
            inventory.append(equipped_weapon[0])
        equipped_weapon.clear()
        equipped_weapon.append(found)
        inventory.remove(found)
        cool_print(f"You equipped the {found} as your weapon.")
        return True
    if found and found in armor:
        if equipped_armor:
            inventory.append(equipped_armor[0])
        equipped_armor.clear()
        equipped_armor.append(found)
        inventory.remove(found)
        cool_print(f"You equipped the {found} as your armor.")
        return True
    cool_print(f"You can't equip {item_name}. It's either not in your inventory or not equippable.")
    return False

def handle_cheat(user_input, inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy):
    cheat = cheat_codes[user_input]
    if cheat["action"] == "remove_hp":
        hp[0] = max(0, hp[0] - cheat["value"])
        cool_print(f"{cheat['message']} (HP: {hp[0]}/{max_hp})")
    elif cheat["action"] == "remove_energy":
        energy[0] = max(0, energy[0] - cheat["value"])
        cool_print(f"{cheat['message']} (Energy: {energy[0]}/{max_energy})")
    elif cheat["action"] == "add_hp":
        hp[0] = min(max_hp, hp[0] + cheat["value"])
        cool_print(f"{cheat['message']} (HP: {hp[0]}/{max_hp})")
    elif cheat["action"] == "add_energy":
        energy[0] = min(max_energy, energy[0] + cheat["value"])
        cool_print(f"{cheat['message']} (Energy: {energy[0]}/{max_energy})")
    elif cheat["action"] == "full_restore_hp":
        hp[0] = max_hp
        cool_print(f"{cheat['message']} (HP: {hp[0]}/{max_hp})")
    elif cheat["action"] == "full_restore_energy":
        energy[0] = max_energy
        cool_print(f"{cheat['message']} (Energy: {energy[0]}/{max_energy})")
    elif cheat["action"] == "add_item":
        item = cheat["value"]
        if item in food_items:
            item = food_items[item]["display"]
        inventory.append(item)
        cool_print(f"{cheat['message']} (Inventory: {inventory})")
    elif cheat["action"] == "clear_inventory":
        inventory.clear()
        equipped_weapon.clear()
        equipped_armor.clear()
        cool_print(f"{cheat['message']} (Inventory: {inventory})")
    elif cheat["action"] == "win_fight":
        cool_print(cheat["message"])
        return "win_fight"
    if hp[0] <= 0:
        cool_print("You have 0 HP. Game over!")
        return None
    return None

def get_input_with_inventory(prompt, inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy, allow_wand=False):
    while True:
        display_status(hp, max_hp, energy, max_energy, equipped_weapon, equipped_armor)
        user_input = input(prompt).strip().lower()
        if user_input == "inventory":
            cool_print(f"Your inventory: {inventory}")
        elif user_input.startswith(("eat ", "drink ")):
            command, item_name = user_input.split(" ", 1)
            item_name = item_name.strip().lower()
            handle_eat_drink(command, item_name, inventory, hp, energy, max_hp, max_energy)
        elif user_input.startswith("equip "):
            item_name = user_input[6:].strip().lower()
            handle_equip(item_name, inventory, equipped_weapon, equipped_armor)
        elif user_input == "use wand" and allow_wand:
            if equipped_weapon and equipped_weapon[0] == "magic wand":
                return "use_wand"
            cool_print("You don't have the magic wand equipped.")
        elif user_input in cheat_codes:
            result = handle_cheat(user_input, inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy)
            if result:
                return result
        else:
            return user_input

def get_valid_choice(prompt, valid_choices, inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy, allow_wand=False):
    while True:
        choice = get_input_with_inventory(prompt, inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy, allow_wand)
        if choice in ["win_fight", "use_wand", None]:
            return choice
        if choice in valid_choices:
            return choice
        cool_print(f"Invalid choice. Please type {', '.join(valid_choices)}" + (" or 'use wand' if equipped" if allow_wand else "."))

def perform_free_hit(equipped_weapon, target_hp, target_name, max_target_hp):
    multiplier = get_damage_multiplier(equipped_weapon)
    damage = int(50 * multiplier)
    target_hp[0] = max(0, target_hp[0] - damage)
    cool_print(f"You land a free hit for {damage} damage! ({target_name} HP: {target_hp[0]}/{max_target_hp})")

def fight_monster(inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy):
    monster_hp = [100]
    max_monster_hp = 100
    wand_used = False
    cool_print("The monster starts to attack you (Monster HP: 100/100), do you fight or run?")
    choice = get_valid_choice("fight or run: ", ["fight", "run"], inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy)
    if choice == "run":
        cool_print("You try to run away but the monster is faster! You lose 25 HP!")
        apply_damage_to_player(25, equipped_armor, hp, max_hp)
        if hp[0] <= 0:
            return False
        return True  # Allow escape but with damage
    if choice in ["win_fight", None]:
        return choice == "win_fight"
    cool_print("Do you dodge left or right?")
    dodge = get_valid_choice("left (30 energy) or right (30 energy): ", ["left", "right"], inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy, allow_wand=True)
    if dodge == "use_wand" and not wand_used:
        wand_used = True
        cool_print("You use the magic wand to freeze the monster!")
        perform_free_hit(equipped_weapon, monster_hp, "Monster", max_monster_hp)
        if monster_hp[0] <= 0:
            cool_print("You defeated the monster!")
            energy[0] = min(energy[0] + 20, max_energy)
            return True
    elif dodge == "right":
        cool_print("You dodge right and the monster hits you!")
        apply_damage_to_player(25, equipped_armor, hp, max_hp)
        if hp[0] <= 0:
            return False
    else:
        energy[0] = max(0, energy[0] - 30)
        perform_free_hit(equipped_weapon, monster_hp, "Monster", max_monster_hp)
        if monster_hp[0] <= 0:
            cool_print("You defeated the monster!")
            energy[0] = min(energy[0] + 20, max_energy)
            return True
    cool_print("It starts to attack you again, do you run towards it or jump back?")
    action = get_valid_choice("run or jump: ", ["run", "jump"], inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy, allow_wand=True)
    if action == "use_wand" and not wand_used:
        wand_used = True
        cool_print("You use the magic wand to freeze the monster!")
        perform_free_hit(equipped_weapon, monster_hp, "Monster", max_monster_hp)
        if monster_hp[0] <= 0:
            cool_print("You defeated the monster!")
            energy[0] = min(energy[0] + 20, max_energy)
            return True
    elif action == "run":
        cool_print("You run towards the monster and it kicks you!")
        apply_damage_to_player(25, equipped_armor, hp, max_hp)
        if hp[0] <= 0:
            return False
    else:
        perform_free_hit(equipped_weapon, monster_hp, "Monster", max_monster_hp)
        if monster_hp[0] <= 0:
            cool_print("You defeated the monster!")
            energy[0] = min(energy[0] + 20, max_energy)
            return True
    return True  # If not defeated, but for simplicity, assume win if not lost

def fight_boss(inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy):
    boss_hp = [500]
    max_boss_hp = 500
    wand_used = False
    cool_print("You encounter the mighty boss with 500 HP! Reduce its HP to 0 to win.")
    cool_print("Each failed dodge costs 25 HP (reduced by armor). Each successful dodge deals 50 damage (modified by weapon).")
    cool_print("For this fight, the boss's attack pattern is randomized. Be ready to dodge!")
    if equipped_weapon and equipped_weapon[0] == "magic wand":
        cool_print("You have the magic wand equipped! Type 'use wand' once per fight to freeze the boss and get a free hit.")
    while boss_hp[0] > 0 and hp[0] > 0:
        energy_cost = random.randint(30, 60)
        energy[0] = max(0, energy[0] - energy_cost)
        correct_choice = random.choice(["left", "right"])
        cool_print(f"The boss lunges at you (Boss HP: {boss_hp[0]}/{max_boss_hp})! Dodge left or right?")
        dodge = get_valid_choice("left or right: ", ["left", "right"], inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy, allow_wand=True)
        if dodge == "use_wand" and not wand_used:
            if equipped_weapon and equipped_weapon[0] == "magic wand":
                wand_used = True
                cool_print("You freeze the boss with the magic wand! You get a free hit.")
                perform_free_hit(equipped_weapon, boss_hp, "Boss", max_boss_hp)
                if boss_hp[0] <= 0:
                    return True
                continue
            cool_print("You don't have the magic wand equipped.")
        elif dodge == "use_wand":
            cool_print("You've already used the magic wand in this fight.")
        elif dodge in ["win_fight", None]:
            return dodge == "win_fight"
        elif dodge == correct_choice:
            perform_free_hit(equipped_weapon, boss_hp, "Boss", max_boss_hp)
        else:
            apply_damage_to_player(25, equipped_armor, hp, max_hp)
    return boss_hp[0] <= 0

def open_chest(num_items, inventory):
    found_items = random.sample(items, num_items)
    if random.random() < 0.5:
        found_items.append(get_money())
    for i in range(len(found_items)):
        if found_items[i] in food_items:
            found_items[i] = food_items[found_items[i]]["display"]
    inventory.extend(found_items)
    cool_print(f"You open the treasure chest and find: {', '.join(found_items)}!")
    cool_print(f"Your inventory: {inventory}")

def adventure_path():
    inventory = []
    equipped_weapon = []
    equipped_armor = []
    max_hp = 100
    max_energy = max_hp * 2
    hp = [max_hp]
    energy = [max_energy]
    left_chest_opened = False
    left_monster_defeated = False
    right_monster_defeated = False
    right_chest_opened = False
    while True:
        cool_print("You're in a dark room, you see two paths, one to the left and one to the right.")
        choice = get_valid_choice("left or right: ", ["left", "right"], inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy)
        if choice is None:
            return
        if choice == "left":
            cool_print("You walk down the left path.")
            if not left_chest_opened:
                cool_print("You find a treasure chest!")
                open_chest(random.randint(1, 3), inventory)
                left_chest_opened = True
            else:
                cool_print("You already opened the treasure chest here.")
            again = get_valid_choice("Do you want to continue down this path or turn back? (continue/turn back): ",
                                    ["continue", "turn back"], inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy)
            if again != "continue":
                continue
            cool_print("You continue deeper...")
            if not left_monster_defeated:
                cool_print("You encounter a monster!")
                won = fight_monster(inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy)
                if not won:
                    if hp[0] <= 0:
                        cool_print("You have 0 HP. Game over!")
                    return
                left_monster_defeated = True
            else:
                cool_print("The monster here is already defeated.")
            again = get_valid_choice("Do you want to continue down this path or turn back? (continue/turn back): ",
                                    ["continue", "turn back"], inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy)
            if again != "continue":
                continue
            cool_print("You venture further and find the boss chamber!")
            won = fight_boss(inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy)
            cool_print("You defeated the boss! Congratulations, you win the game!" if won else "The boss defeated you. Game over!")
            return
        elif choice == "right":
            cool_print("You walk down the right path.")
            if not right_monster_defeated:
                cool_print("You encounter a monster!")
                won = fight_monster(inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy)
                if not won:
                    if hp[0] <= 0:
                        cool_print("You have 0 HP. Game over!")
                    return
                right_monster_defeated = True
            else:
                cool_print("The monster here is already defeated.")
            again = get_valid_choice("Do you want to continue down this path or turn back? (continue/turn back): ",
                                    ["continue", "turn back"], inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy)
            if again != "continue":
                continue
            cool_print("You continue deeper...")
            if not right_chest_opened:
                cool_print("You find a treasure chest!")
                open_chest(5, inventory)
                right_chest_opened = True
            else:
                cool_print("You already opened the treasure chest here.")
            again = get_valid_choice("Do you want to continue down this path or turn back? (continue/turn back): ",
                                    ["continue", "turn back"], inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy)
            if again != "continue":
                continue
            cool_print("You venture further and find the boss chamber!")
            won = fight_boss(inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy)
            cool_print("You defeated the boss! Congratulations, you win the game!" if won else "The boss defeated you. Game over!")
            return

def main():
    cool_print("Actions: Type 'inventory' to see your current items, type 'eat (item_name)' or 'drink (item_name)' to consume a food or drink item, "
               "type 'equip (item_name)' to equip a weapon or armor. "
               "During fights, if you have the magic wand equipped, type 'use wand' once per fight to freeze the enemy and get a free hit. "
               "Armor effects: Helmet reduces damage by 25%, Chestplate by 50%, Shield has 50% chance to deflect attacks.")
    cool_print("how is your day?")
    choice = get_valid_choice("(good or bad): ", ["good", "bad"], [], [], [], [0], [0], 100, 200)
    if choice == "bad":
        cool_print("oh no! Well maybe wait to play the game later.")
        exit()
    cool_print("thats great!", delay=0.0005)
    cool_print("make a name for your character:")
    username = input()
    cool_print(f"Welcome, {username}! Lets begin!", delay=0.0005)
    adventure_path()

main()

