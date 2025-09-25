import string
import time
import random

# ========================================
# UTILITY FUNCTIONS
# ========================================

# Prints text slowly for a cool effect, like in old-school games
# This makes the game feel more immersive by simulating typewriter-style text
def print_with_delay(text, delay=0.05):
    """
    Displays text character by character with a delay for dramatic effect.
    
    Args:
        text (str): The text to print.
        delay (float): Time delay between characters in seconds (default: 0.05).
    """
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()

# List of all possible items you can find in the game
# These are the base items that can appear in chests or be added via cheats
items = [
    "book", "burger", "diamond", "rubber duck", "rare sword", "common sword",
    "magic wand", "potion", "shield", "helmet", "unicorn", "vanilla ice cream",
    "key", "apple", "pizza", "chocolate bar", "soda", "candy cane",
    "energy drink", "cake", "chestplate", "ancient amulet", "cursed relic"
]

# Generates a random amount of money for treasure chests
# Money is formatted as "money (X)" where X is 1-100 gold coins
def generate_money():
    """
    Creates a random money item string for adding to inventory.
    
    Returns:
        str: A formatted money string like "money (42)".
    """
    return f"money ({random.randint(1, 100)})"

# Defines food items and their effects on HP and energy
# Each food has a display name showing its effects, plus actual HP/energy restoration values
food_items = {
    "burger": {"hp": 20, "energy": 10, "display": "burger (20HP, 10eng)"},
    "vanilla ice cream": {"hp": 10, "energy": 25, "display": "vanilla ice cream (10HP, 25eng)"},
    "apple": {"hp": 5, "energy": 10, "display": "apple (5HP, 10eng)"},
    "pizza": {"hp": 15, "energy": 15, "display": "pizza (15HP, 15eng)"},
    "chocolate bar": {"hp": 0, "energy": 40, "display": "chocolate bar (0HP, 40eng)"},
    "soda": {"hp": 0, "energy": 50, "display": "soda (0HP, 50eng)"},
    "candy cane": {"hp": 5, "energy": 60, "display": "candy cane (5HP, 60eng)"},
    "energy drink": {"hp": 0, "energy": 80, "display": "energy drink (0HP, 80eng)"},
    "cake": {"hp": 10, "energy": 60, "display": "cake (15HP, 60eng)"},  # Note: display shows 15HP but actual is 10HP - possible bug?
    "potion": {"hp": 50, "energy": 50, "display": "potion (50HP, 50eng)"}
}

# Sets of equippable items
# Weapons increase damage output, armor reduces incoming damage
weapons = {"rare sword", "common sword", "magic wand"}
armor = {"shield", "helmet", "chestplate"}
# Artifacts provide passive bonuses but aren't equippable
artifacts = {"ancient amulet", "cursed relic"}

# Cheat codes for testing or fun shortcuts
# These are 8-digit codes that trigger special actions like adding items or restoring health
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

# ========================================
# COMBAT AND DAMAGE FUNCTIONS
# ========================================

# Calculates how much extra damage you deal based on your weapon and artifacts
# Multipliers stack: weapons provide base boost, artifacts multiply on top
def calculate_damage_boost(equipped_weapon, inventory):
    """
    Computes the total damage multiplier based on equipped weapon and inventory artifacts.
    
    Args:
        equipped_weapon (list): Currently equipped weapon item.
        inventory (list): Player's current inventory items.
    
    Returns:
        float: The total damage multiplier (e.g., 2.0 for rare sword).
    """
    multiplier = 1.0
    if equipped_weapon and equipped_weapon[0] == "rare sword":
        multiplier = 2.0
    elif equipped_weapon and equipped_weapon[0] == "common sword":
        multiplier = 1.35
    # Ancient amulet gives a 50% damage boost
    if "ancient amulet" in inventory:
        multiplier *= 1.5
    # Cursed relic triples damage but caps incoming damage elsewhere
    if "cursed relic" in inventory:
        multiplier *= 3.0
    return multiplier

# Handles damage taken by the player, factoring in armor and blessings
# Applies reductions in this order: relic cap -> blessing -> armor
def apply_player_damage(damage, equipped_armor, hp, max_hp, has_villager_blessing, inventory):
    """
    Applies damage to the player after applying all defensive modifiers.
    
    Args:
        damage (int): Base damage amount.
        equipped_armor (list): Currently equipped armor item.
        hp (list): Mutable list containing current HP [current].
        max_hp (int): Maximum HP value.
        has_villager_blessing (bool): Whether player has the damage reduction blessing.
        inventory (list): Player's current inventory for artifact checks.
    
    Returns:
        None: Modifies hp[0] in place.
    """
    # Cursed relic caps all incoming damage at 5 HP
    if "cursed relic" in inventory:
        damage = min(damage, 5)
        print_with_delay("The cursed relic's dark aura limits incoming damage to 5!")
    # Villager's blessing reduces damage by 20%
    if has_villager_blessing:
        damage = int(damage * 0.8)
        print_with_delay(f"The villager's blessing reduces damage to {damage}!")
    # Armor effects: shield (50% deflect), helmet (25% reduction), chestplate (50% reduction)
    if equipped_armor:
        armor_type = equipped_armor[0]
        if armor_type == "shield" and random.random() < 0.5:
            print_with_delay("Your shield deflected the attack!")
            return  # No damage applied
        elif armor_type == "helmet":
            damage = int(damage * 0.75)
            print_with_delay(f"Your helmet reduced the damage to {damage}!")
        elif armor_type == "chestplate":
            damage = int(damage * 0.5)
            print_with_delay(f"Your chestplate reduced the damage to {damage}!")
    # Apply the final damage
    hp[0] -= damage
    if damage > 0:
        print_with_delay(f"Took {damage} damage. (HP: {hp[0]}/{max_hp})")

# Shows your current HP, energy, and equipped gear
# This is displayed before every player input for quick status checks
def show_status(hp, max_hp, energy, max_energy, equipped_weapon, equipped_armor):
    """
    Prints the current player status to the console.
    
    Args:
        hp (list): Current HP [current].
        max_hp (int): Maximum HP.
        energy (list): Current energy [current].
        max_energy (int): Maximum energy.
        equipped_weapon (list): Equipped weapon.
        equipped_armor (list): Equipped armor.
    """
    print(f"HP: {hp[0]}/{max_hp} | Energy: {energy[0]}/{max_energy} | Equipped Weapon: {equipped_weapon or 'None'} | Equipped Armor: {equipped_armor or 'None'}")

# ========================================
# INVENTORY AND ITEM FUNCTIONS
# ========================================

# Lets you eat or drink items to restore HP and energy
# Searches inventory for matching display names and applies effects
def consume_item(command, item_name, inventory, hp, energy, max_hp, max_energy):
    """
    Consumes a food or drink item from inventory to restore HP/energy.
    
    Args:
        command (str): "eat" or "drink".
        item_name (str): Name of the item to consume.
        inventory (list): Player's inventory.
        hp (list): Current HP [current].
        energy (list): Current energy [current].
        max_hp (int): Maximum HP.
        max_energy (int): Maximum energy.
    
    Returns:
        bool: True if item was consumed successfully, False otherwise.
    """
    found = None
    food_key_found = None
    # Loop through inventory and match against food display names
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
        # Restore but don't exceed max values
        hp[0] = min(hp[0] + heal, max_hp)
        energy[0] = min(energy[0] + energize, max_energy)
        inventory.remove(found)  # Remove the consumed item
        # Build feedback message
        msg = f"You {'drink' if food_key_found in ['soda', 'energy drink'] else 'eat'} the {food_items[food_key_found]['display']}."
        if heal > 0:
            msg += f" Healed {hp[0] - old_hp} HP."
        if energize > 0:
            msg += f" Restored {energy[0] - old_energy} energy."
        print_with_delay(msg + f" (HP: {hp[0]}/{max_hp}, Energy: {energy[0]}/{max_energy})")
        return True
    print_with_delay(f"You can't {'drink' if command == 'drink' else 'eat'} {item_name}. It's either not in your inventory or not consumable.")
    return False

# Equips a weapon or armor from your inventory
# Swaps out previously equipped items back to inventory
def equip_item(item_name, inventory, equipped_weapon, equipped_armor):
    """
    Equips a weapon or armor item from inventory.
    
    Args:
        item_name (str): Name of item to equip.
        inventory (list): Player's inventory.
        equipped_weapon (list): Currently equipped weapon [item].
        equipped_armor (list): Currently equipped armor [item].
    
    Returns:
        bool: True if equipped successfully, False otherwise.
    """
    found = next((item for item in inventory if item.lower() == item_name), None)
    if found and found in weapons:
        # Unequip current weapon if any
        if equipped_weapon:
            inventory.append(equipped_weapon[0])
        equipped_weapon.clear()
        equipped_weapon.append(found)
        inventory.remove(found)
        print_with_delay(f"You equipped the {found} as your weapon.")
        return True
    if found and found in armor:
        # Unequip current armor if any
        if equipped_armor:
            inventory.append(equipped_armor[0])
        equipped_armor.clear()
        equipped_armor.append(found)
        inventory.remove(found)
        print_with_delay(f"You equipped the {found} as your armor.")
        return True
    print_with_delay(f"You can't equip {item_name}. It's either not in your inventory or not equippable.")
    return False

# Processes cheat codes for quick testing or bonuses
# Handles all cheat actions like modifying stats or adding items
def process_cheat_code(user_input, inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy):
    """
    Executes a cheat code action based on the input code.
    
    Args:
        user_input (str): The 8-digit cheat code.
        inventory (list): Player's inventory.
        equipped_weapon (list): Equipped weapon.
        equipped_armor (list): Equipped armor.
        hp (list): Current HP.
        energy (list): Current energy.
        max_hp (int): Max HP.
        max_energy (int): Max energy.
    
    Returns:
        str or None: "win_fight" if applicable, None otherwise.
    """
    cheat = cheat_codes[user_input]
    if cheat["action"] == "remove_hp":
        hp[0] = max(0, hp[0] - cheat["value"])
        print_with_delay(f"{cheat['message']} (HP: {hp[0]}/{max_hp})")
    elif cheat["action"] == "remove_energy":
        energy[0] = max(0, energy[0] - cheat["value"])
        print_with_delay(f"{cheat['message']} (Energy: {energy[0]}/{max_energy})")
    elif cheat["action"] == "add_hp":
        hp[0] = min(max_hp, hp[0] + cheat["value"])
        print_with_delay(f"{cheat['message']} (HP: {hp[0]}/{max_hp})")
    elif cheat["action"] == "add_energy":
        energy[0] = min(max_energy, energy[0] + cheat["value"])
        print_with_delay(f"{cheat['message']} (Energy: {energy[0]}/{max_energy})")
    elif cheat["action"] == "full_restore_hp":
        hp[0] = max_hp
        print_with_delay(f"{cheat['message']} (HP: {hp[0]}/{max_hp})")
    elif cheat["action"] == "full_restore_energy":
        energy[0] = max_energy
        print_with_delay(f"{cheat['message']} (Energy: {energy[0]}/{max_energy})")
    elif cheat["action"] == "add_item":
        item = cheat["value"]
        if item in food_items:
            item = food_items[item]["display"]
        inventory.append(item)
        print_with_delay(f"{cheat['message']} (Inventory: {inventory})")
    elif cheat["action"] == "clear_inventory":
        inventory.clear()
        equipped_weapon.clear()
        equipped_armor.clear()
        print_with_delay(f"{cheat['message']} (Inventory: {inventory})")
    elif cheat["action"] == "win_fight":
        print_with_delay(cheat["message"])
        return "win_fight"
    # Check for game over after cheats
    if hp[0] <= 0:
        print_with_delay("You have 0 HP. Game over!")
        return None
    return None

# ========================================
# INPUT HANDLING FUNCTIONS
# ========================================

# Gets player input and handles inventory, eating, equipping, and cheats
# Loops until valid non-command input is received
def get_user_input(prompt, inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy, allow_wand=False):
    """
    Prompts user for input and processes commands like inventory checks or item use.
    
    Args:
        prompt (str): The input prompt to display.
        ... (other args): Game state variables.
        allow_wand (bool): If True, allows "use wand" command during combat.
    
    Returns:
        str: Processed user input or special command result.
    """
    while True:
        show_status(hp, max_hp, energy, max_energy, equipped_weapon, equipped_armor)
        user_input = input(prompt).strip().lower()
        if user_input == "inventory":
            print_with_delay(f"Your inventory: {inventory}")
            continue  # Loop back for more input
        elif user_input.startswith(("eat ", "drink ")):
            command, item_name = user_input.split(" ", 1)
            item_name = item_name.strip().lower()
            consume_item(command, item_name, inventory, hp, energy, max_hp, max_energy)
            continue
        elif user_input.startswith("equip "):
            item_name = user_input[6:].strip().lower()
            equip_item(item_name, inventory, equipped_weapon, equipped_armor)
            continue
        elif user_input == "use wand" and allow_wand:
            if equipped_weapon and equipped_weapon[0] == "magic wand":
                return "use_wand"
            print_with_delay("You don't have the magic wand equipped.")
            continue
        elif user_input in cheat_codes:
            result = process_cheat_code(user_input, inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy)
            if result:
                return result
        else:
            return user_input  # Valid non-command input

# Ensures player input is valid for specific choices
# Wraps get_user_input to validate against allowed options
def validate_choice(prompt, valid_choices, inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy, allow_wand=False):
    """
    Gets and validates user choice against a list of valid options.
    
    Args:
        prompt (str): Input prompt.
        valid_choices (list): Allowed choice strings.
        ... (other args): Game state.
        allow_wand (bool): Allow wand use in combat.
    
    Returns:
        str: Valid choice or special command.
    """
    while True:
        choice = get_user_input(prompt, inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy, allow_wand)
        if choice in ["win_fight", "use_wand", None]:
            return choice
        if choice in valid_choices:
            return choice
        print_with_delay(f"Invalid choice. Please type {', '.join(valid_choices)}" + (" or 'use wand' if equipped" if allow_wand else "."))

# ========================================
# COMBAT FUNCTIONS
# ========================================

# Deals damage to a target during combat
# Uses the calculated multiplier for variable damage output
def execute_hit(equipped_weapon, target_hp, target_name, max_target_hp, inventory):
    """
    Performs a player attack on a target, dealing damage based on multipliers.
    
    Args:
        equipped_weapon (list): Equipped weapon.
        target_hp (list): Target's HP [current].
        target_name (str): Name of the target (e.g., "Monster").
        max_target_hp (int): Target's max HP.
        inventory (list): For artifact multipliers.
    """
    multiplier = calculate_damage_boost(equipped_weapon, inventory)
    damage = int(75 * multiplier)  # Base damage is 75, scaled by multiplier
    target_hp[0] = max(0, target_hp[0] - damage)
    print_with_delay(f"You land a hit for {damage} damage! ({target_name} HP: {target_hp[0]}/{max_target_hp})")

# Handles fighting a regular monster
# Simple two-phase combat with dodge choices and wand option
def battle_monster(inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy, has_villager_blessing):
    """
    Manages combat against a standard monster (100 HP).
    
    Args:
        ... (game state args)
        has_villager_blessing (bool): Damage reduction active.
    
    Returns:
        bool: True if player wins/survives, False if defeated.
    """
    monster_hp = [100]
    max_monster_hp = 100
    wand_used = False  # Wand can only be used once per fight
    print_with_delay("The monster starts to attack you (Monster HP: 100/100), do you fight or run?")
    choice = validate_choice("fight or run: ", ["fight", "run"], inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy)
    if choice == "run":
        print_with_delay("You try to run away but the monster is faster! You lose 25 HP!")
        apply_player_damage(25, equipped_armor, hp, max_hp, has_villager_blessing, inventory)
        if hp[0] <= 0:
            return False
        return True  # Escaped but took damage
    if choice in ["win_fight", None]:
        return choice == "win_fight"
    # First dodge phase
    print_with_delay("Do you dodge left or right?")
    dodge = validate_choice("left (30 energy) or right (30 energy): ", ["left", "right"], inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy, allow_wand=True)
    if dodge == "use_wand" and not wand_used:
        wand_used = True
        print_with_delay("You use the magic wand to freeze the monster!")
        execute_hit(equipped_weapon, monster_hp, "Monster", max_monster_hp, inventory)
        if monster_hp[0] <= 0:
            print_with_delay("You defeated the monster!")
            energy[0] = min(energy[0] + 20, max_energy)  # Reward energy
            return True
    elif dodge == "right":  # Wrong choice - take damage
        print_with_delay("You dodge right and the monster hits you!")
        apply_player_damage(25, equipped_armor, hp, max_hp, has_villager_blessing, inventory)
        if hp[0] <= 0:
            return False
    else:  # Left - correct, spend energy and hit
        energy[0] = max(0, energy[0] - 30)
        execute_hit(equipped_weapon, monster_hp, "Monster", max_monster_hp, inventory)
        if monster_hp[0] <= 0:
            print_with_delay("You defeated the monster!")
            energy[0] = min(energy[0] + 20, max_energy)
            return True
    # Second phase
    print_with_delay("It starts to attack you again, do you run towards it or jump back?")
    action = validate_choice("run or jump: ", ["run", "jump"], inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy, allow_wand=True)
    if action == "use_wand" and not wand_used:
        wand_used = True
        print_with_delay("You use the magic wand to freeze the monster!")
        execute_hit(equipped_weapon, monster_hp, "Monster", max_monster_hp, inventory)
        if monster_hp[0] <= 0:
            print_with_delay("You defeated the monster!")
            energy[0] = min(energy[0] + 20, max_energy)
            return True
    elif action == "run":  # Wrong - take damage
        print_with_delay("You run towards the monster and it kicks you!")
        apply_player_damage(25, equipped_armor, hp, max_hp, has_villager_blessing, inventory)
        if hp[0] <= 0:
            return False
    else:  # Jump - correct, hit
        execute_hit(equipped_weapon, monster_hp, "Monster", max_monster_hp, inventory)
        if monster_hp[0] <= 0:
            print_with_delay("You defeated the monster!")
            energy[0] = min(energy[0] + 20, max_energy)
            return True
    return True  # Survived the encounter

# Manages the epic boss fight
# Looping combat with random dodge directions until boss or player is defeated
def battle_boss(inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy, has_villager_blessing):
    """
    Handles the final boss battle (300 HP) with random dodge requirements.
    
    Args:
        ... (game state args)
        has_villager_blessing (bool): Active blessing.
    
    Returns:
        bool: True if boss defeated, False if player loses.
    """
    boss_hp = [300]
    max_boss_hp = 300
    wand_used = False
    print_with_delay("You encounter the mighty boss with 300 HP! Reduce its HP to 0 to win.")
    print_with_delay("Each failed dodge costs 25 HP (reduced by armor). Each successful dodge deals 75 damage (modified by weapon).")
    if "ancient amulet" in inventory:
        print_with_delay("Your ancient amulet glows, boosting your damage by 50%!")
    if has_villager_blessing:
        print_with_delay("The villager's blessing protects you, reducing damage taken by 20%!")
    if equipped_weapon and equipped_weapon[0] == "magic wand":
        print_with_delay("You have the magic wand equipped! Type 'use wand' once per fight to freeze the boss and get a free hit.")
    # Main combat loop
    while boss_hp[0] > 0 and hp[0] > 0:
        # Random energy cost per turn (20-40)
        energy_cost = random.randint(20, 40)
        energy[0] = max(0, energy[0] - energy_cost)
        correct_choice = random.choice(["left", "right"])  # Random correct dodge
        print_with_delay(f"The boss lunges at you (Boss HP: {boss_hp[0]}/{max_boss_hp})! Dodge left or right?")
        dodge = validate_choice("left or right: ", ["left", "right"], inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy, allow_wand=True)
        if dodge == "use_wand" and not wand_used:
            if equipped_weapon and equipped_weapon[0] == "magic wand":
                wand_used = True
                print_with_delay("You freeze the boss with the magic wand! You get a free hit.")
                execute_hit(equipped_weapon, boss_hp, "Boss", max_boss_hp, inventory)
                if boss_hp[0] <= 0:
                    return True
                continue  # Skip normal turn
            print_with_delay("You don't have the magic wand equipped.")
        elif dodge == "use_wand":
            print_with_delay("You've already used the magic wand in this fight.")
        elif dodge in ["win_fight", None]:
            return dodge == "win_fight"
        elif dodge == correct_choice:  # Success - deal damage
            execute_hit(equipped_weapon, boss_hp, "Boss", max_boss_hp, inventory)
        else:  # Fail - take damage
            apply_player_damage(25, equipped_armor, hp, max_hp, has_villager_blessing, inventory)
    return boss_hp[0] <= 0  # Win condition

# ========================================
# QUEST AND PUZZLE FUNCTIONS
# ========================================

# Presents a riddle to unlock the ancient amulet
# Classic echo riddle - correct answer grants powerful artifact
def solve_mystic_cave(inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy):
    """
    Handles the mystic cave riddle puzzle.
    
    Args:
        ... (game state args)
    
    Returns:
        bool: True if solved (amulet gained), False if failed (energy loss).
    """
    print_with_delay("You find a mystic cave with a glowing pedestal. A riddle appears: 'I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?'")
    answer = validate_choice("Your answer (type the word): ", ["echo"], inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy)
    if answer == "echo":
        print_with_delay("The pedestal glows brightly, and you receive the ancient amulet!")
        inventory.append("ancient amulet")
        return True
    else:
        print_with_delay("The cave rumbles, and a surge of energy drains you! You lose 50 energy.")
        energy[0] = max(0, energy[0] - 50)
        return False

# Lets you save a villager for a reward and blessing
# Moral choice: fight a weak creature for potion + 20% damage reduction
def save_villager(inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy, has_villager_blessing):
    """
    Manages the villager rescue side quest.
    
    Args:
        ... (game state args)
        has_villager_blessing (bool): Current blessing status (updated in place).
    
    Returns:
        bool: True if rescued (blessing granted), False otherwise.
    """
    print_with_delay("You hear a cry for help! A villager is trapped by a small creature (HP: 50).")
    creature_hp = [50]
    max_creature_hp = 50
    print_with_delay("Do you fight the creature or ignore the villager?")
    choice = validate_choice("fight or ignore: ", ["fight", "ignore"], inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy)
    if choice == "ignore":
        print_with_delay("You walk away, ignoring the villager's pleas. The guilt weighs on you.")
        return False
    print_with_delay("You engage the creature!")
    dodge = validate_choice("Dodge left or right (20 energy): ", ["left", "right"], inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy)
    if dodge in ["left", "right"]:
        energy[0] = max(0, energy[0] - 20)
        execute_hit(equipped_weapon, creature_hp, "Creature", max_creature_hp, inventory)
        if creature_hp[0] <= 0:
            print_with_delay("You defeated the creature! The villager thanks you and gives you a potion and a blessing.")
            inventory.append(food_items["potion"]["display"])
            return True
        print_with_delay("The creature strikes back!")
        apply_player_damage(15, equipped_armor, hp, max_hp, has_villager_blessing, inventory)
        if hp[0] <= 0:
            return False
        execute_hit(equipped_weapon, creature_hp, "Creature", max_creature_hp, inventory)
        if creature_hp[0] <= 0:
            print_with_delay("You defeated the creature! The villager thanks you and gives you a potion and a blessing.")
            inventory.append(food_items["potion"]["display"])
            return True
    return False

# ========================================
# WORLD AND EXPLORATION FUNCTIONS
# ========================================

# Opens a treasure chest with random loot
# Randomly samples from items list, converts foods to display format, sometimes adds money
def open_chest(num_items, inventory):
    """
    Generates and adds random items from a chest to inventory.
    
    Args:
        num_items (int): Number of items to generate.
        inventory (list): Player's inventory to add to.
    """
    found_items = random.sample(items, num_items)  # Random selection without replacement
    # 50% chance to add money
    if random.random() < 0.5:
        found_items.append(generate_money())
    # Convert food items to their display format
    for i in range(len(found_items)):
        if found_items[i] in food_items:
            found_items[i] = food_items[found_items[i]]["display"]
    inventory.extend(found_items)  # Add all to inventory
    print_with_delay(f"You open the treasure chest and find: {', '.join(found_items)}!")
    print_with_delay(f"Your inventory: {inventory}")

# Runs the main adventure loop with paths and events
# Handles left/right path choices, tracks opened chests and defeated monsters
def explore_paths(inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy, has_villager_blessing):
    """
    Main game loop for exploration and encounters.
    
    Args:
        ... (game state args)
        has_villager_blessing (bool): Updated in place if quest completed.
    
    Returns:
        bool: True if boss defeated (win), False if game over.
    """
    # Trackers for one-time events per path
    left_chest_opened = False
    left_monster_defeated = False
    right_monster_defeated = False
    right_chest_opened = False
    left_puzzle_solved = False
    while True:
        print_with_delay("You're in a dark room, you see two paths, one to the left and one to the right.")
        choice = validate_choice("left or right: ", ["left", "right"], inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy)
        if choice is None:
            return False  # Game over from cheat or low HP
        if choice == "left":
            print_with_delay("You walk down the left path.")
            # Left path chest (1-3 items)
            if not left_chest_opened:
                print_with_delay("You find a treasure chest!")
                open_chest(random.randint(1, 3), inventory)
                left_chest_opened = True
            else:
                print_with_delay("You already opened the treasure chest here.")
            # Ask to continue or turn back
            again = validate_choice("Do you want to continue down this path or turn back? (continue/turn back): ",
                                    ["continue", "turn back"], inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy)
            if again != "continue":
                continue  # Back to room choice
            print_with_delay("You continue deeper...")
            # Left path monster
            if not left_monster_defeated:
                print_with_delay("You encounter a monster!")
                won = battle_monster(inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy, has_villager_blessing)
                if not won:
                    if hp[0] <= 0:
                        print_with_delay("You have 0 HP. Game over!")
                    return False
                left_monster_defeated = True
            else:
                print_with_delay("The monster here is already defeated.")
            # Left path puzzle
            if not left_puzzle_solved:
                print_with_delay("You discover a mystic cave!")
                left_puzzle_solved = solve_mystic_cave(inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy)
            else:
                print_with_delay("You've already explored the mystic cave.")
            # Ask to continue to boss
            again = validate_choice("Do you want to continue down this path or turn back? (continue/turn back): ",
                                    ["continue", "turn back"], inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy)
            if again != "continue":
                continue
            # Boss fight!
            print_with_delay("You venture further and find the boss chamber!")
            won = battle_boss(inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy, has_villager_blessing)
            if won:
                if "ancient amulet" in inventory:
                    print_with_delay("With the ancient amulet's power, you vanquish the boss and restore peace to the land. You are hailed as a legendary hero!")
                else:
                    print_with_delay("You defeated the boss! Congratulations, you win the game as a brave adventurer!")
                # Secret easter egg for "hell yea"
                secret_input = input().strip().lower()
                if secret_input == "hell yea":
                    inventory.append("cursed relic")
                    print_with_delay("A dark energy surges through you, and a cursed relic appears in your inventory!")
                return True
            else:
                print_with_delay("The boss defeated you. Game over!")
                return False
        elif choice == "right":
            print_with_delay("You walk down the right path.")
            # Right path monster first
            if not right_monster_defeated:
                print_with_delay("You encounter a monster!")
                won = battle_monster(inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy, has_villager_blessing)
                if not won:
                    if hp[0] <= 0:
                        print_with_delay("You have 0 HP. Game over!")
                    return False
                right_monster_defeated = True
            else:
                print_with_delay("The monster here is already defeated.")
            # Right path villager quest (only once)
            if not has_villager_blessing:
                has_villager_blessing = save_villager(inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy, has_villager_blessing)
                if not has_villager_blessing and hp[0] > 0:
                    max_hp = max(50, max_hp - 20)  # Penalty for ignoring
                    print_with_delay(f"Your guilt weakens you. Max HP reduced to {max_hp}!")
                    hp[0] = min(hp[0], max_hp)
            else:
                print_with_delay("You've already dealt with the villager's situation.")
            # Ask to continue
            again = validate_choice("Do you want to continue down this path or turn back? (continue/turn back): ",
                                    ["continue", "turn back"], inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy)
            if again != "continue":
                continue
            print_with_delay("You continue deeper...")
            # Right path chest (always 5 items)
            if not right_chest_opened:
                print_with_delay("You find a treasure chest!")
                open_chest(5, inventory)
                right_chest_opened = True
            else:
                print_with_delay("You already opened the treasure chest here.")
            # Ask to continue to boss
            again = validate_choice("Do you want to continue down this path or turn back? (continue/turn back): ",
                                    ["continue", "turn back"], inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy)
            if again != "continue":
                continue
            # Boss fight!
            print_with_delay("You venture further and find the boss chamber!")
            won = battle_boss(inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy, has_villager_blessing)
            if won:
                if has_villager_blessing:
                    print_with_delay("With the villager's blessing, you defeat the boss and save the village. You are celebrated as their savior!")
                else:
                    print_with_delay("You defeated the boss! Congratulations, you win the game as a brave adventurer!")
                # Secret easter egg
                secret_input = input().strip().lower()
                if secret_input == "hell yea":
                    inventory.append("cursed relic")
                    print_with_delay("A dark energy surges through you, and a cursed relic appears in your inventory!")
                return True
            else:
                print_with_delay("The boss defeated you. Game over!")
                return False

# ========================================
# MAIN GAME FUNCTION
# ========================================

# Starts the game with an intro and main loop
# Initializes game state and handles replay logic (keeps inventory across runs)
def start_game():
    """
    Entry point for the game: sets up state, shows intro, and runs adventure loop.
    """
    # Initial player stats: 100 HP, 200 Energy
    max_hp = 100
    max_energy = max_hp * 2
    hp = [max_hp]
    energy = [max_energy]
    inventory = []
    equipped_weapon = []
    equipped_armor = []
    has_villager_blessing = False
    # Game instructions
    print_with_delay("Actions: Type 'inventory' to see your current items, type 'eat (item_name)' or 'drink (item_name)' to consume a food or drink item, "
                     "type 'equip (item_name)' to equip a weapon or armor. "
                     "During fights, if you have the magic wand equipped, type 'use wand' to freeze the enemy and get a free hit. "
                     "Armor effects: Helmet reduces damage by 25%, Chestplate by 50%, Shield has 50% chance to deflect attacks.")
    # Fun mood check
    print_with_delay("how is your day?")
    choice = validate_choice("(good or bad): ", ["good", "bad"], inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy)
    if choice == "bad":
        print_with_delay("oh no! Well maybe wait to play the game later.")
        exit()  # Exit game if bad day
    print_with_delay("thats great!", delay=0.0005)
    # Character naming
    print_with_delay("make a name for your character:")
    username = input()
    print_with_delay(f"Welcome, {username}! Lets begin!", delay=0.0005)
    # Main game loop - allows replays with persistent inventory
    while True:
        won = explore_paths(inventory, equipped_weapon, equipped_armor, hp, energy, max_hp, max_energy, has_villager_blessing)
        if not won:
            break  # Game over, no replay
        print_with_delay("Would you like to play again with your current inventory? (yes/no)")
        play_again = input().strip().lower()
        if play_again != "yes":
            break
        # Reset HP/Energy for new run, keep gear/inventory/blessing
        hp[0] = max_hp
        energy[0] = max_energy
        print_with_delay("Your adventure begins anew!")

# start game :)
start_game()
