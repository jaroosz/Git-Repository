# pylint: disable=C0116
# pylint: disable=C0115
# pylint: disable=C0114
# pylint: disable=C0301

import time
import random
import os
import json

# create a folder which will contain all the characters created by player
current_directory = os.path.dirname(os.path.abspath(__file__))
folder_name = "chars"
folder_path = os.path.join(current_directory, folder_name)
if not os.path.exists(folder_path):
    os.mkdir(folder_path)
    print(f"Folder '{folder_name}' created.")

class Col:  # text color
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'


stats = {
    "name": 0,
    "exp": 0,
    "next_lvl": 0,
    "min_dmg": 0,
    "max_dmg": 0,
    "str": 0,
    "vit": 0,
    "hp": 0,
    "crit": 0,
    "dodge": 0,
    "lvl": 1,
    "location": None,
    "class": None,
    "weapon": ["None", 0, 0, 0, 0, 0, 0],
    "loot": ["None", 0, 0, 0, 0, 0, 0]
}

weapon_list = {  # name, min_dmg, max_dmg, str, vit, crit, dodge
    0: [
        ["None", 0, 0, 0, 0, 0, 0]
    ],

    1: [
        ["Rusty Dagger", 2, 4, 1, 0, 5, 2],
        ["Wooden Staff", 3, 5, 0, 1, 3, 2],
        ["Iron Sword", 4, 6, 2, 0, 4, 1],
        ["Bronze Mace", 3, 7, 1, 1, 2, 1],
        ["Steel Axe", 5, 8, 3, 1, 3, 1],
        ["Bone Club", 2, 5, 1, 1, 2, 1],
        ["Obsidian Knife", 3, 6, 0, 2, 4, 2],
        ["Wooden Bow", 4, 7, 2, 0, 3, 3],
        ["Stone Sling", 2, 4, 1, 1, 3, 3],
        ["Copper Dagger", 3, 5, 1, 0, 4, 2],
    ],

    2: [
        ["Golden Spear", 6, 9, 3, 2, 6, 3],
        ["Poisoned Blade", 5, 8, 2, 2, 7, 3],
        ["Crystal Wand", 7, 10, 1, 3, 5, 4],
        ["Enchanted Bow", 6, 9, 3, 1, 6, 5],
        ["Sapphire Blade", 8, 12, 4, 2, 8, 4],
        ["Emerald Staff", 7, 11, 2, 3, 6, 4],
        ["Shadow Dagger", 6, 9, 3, 2, 7, 5],
        ["Flame Staff", 8, 12, 1, 4, 9, 3],
        ["Frost Blade", 7, 10, 2, 3, 7, 3],
        ["Arcane Wand", 7, 11, 3, 2, 6, 4],
    ],

    3: [
        ["Sword of Kings", 10, 15, 5, 5, 11, 6],
        ["Hammer of Thor", 12, 18, 6, 4, 13, 5],
        ["Blade of Legends", 11, 16, 7, 3, 12, 6],
        ["Spear of Odin", 13, 20, 8, 4, 14, 4],
        ["Holy Sword", 14, 21, 7, 6, 16, 4],
        ["Sword of Apocalypse", 15, 22, 9, 5, 15, 4],
        ["Wind Bow", 12, 18, 6, 5, 12, 6],
        ["Shield of Zeus", 10, 16, 5, 7, 11, 7],
        ["Sword of Slaying", 13, 19, 8, 6, 13, 5],
        ["Staff of Elders", 14, 20, 7, 8, 15, 5],
    ],

    4: [
        ["*Soul Reaver, the Scythe of Death*", 16, 25, 10, 8, 17, 10],
        ["*Inferno, the Flaming Sword*", 18, 28, 12, 7, 19, 9],
        ["*Frostbite, the Icy Spear*", 17, 26, 11, 9, 18, 9],
        ["*Divine Justice, the Celestial Hammer*", 20, 30, 14, 10, 20, 8],
        ["*Ethereal Bow, the Archer's Dream*", 15, 24, 9, 12, 24, 10],
        ["*Thunderstruck, the Lightning Staff*", 19, 29, 13, 11, 19, 8],
        ["*Phoenix Talon, the Fire Dagger*", 14, 23, 11, 12, 22, 8],
        ["*Void Cleaver, the Dark Blade*", 22, 32, 15, 14, 22, 8],
        ["*Aurora Scepter, the Wand of Light*", 21, 31, 16, 15, 21, 9],
        ["*Time Bender, the Staff of Ages*", 25, 35, 18, 18, 25, 12],
    ]
}

monster_list = {  # name, health, min_dmg, max_dmg, dodge, crit, exp
    1: [
        ["Goblin", 20, 3, 6, 5, 5, 3],
        ["Skeleton", 25, 2, 5, 8, 8, 3],
        ["Orc", 38, 3, 5, 7, 4, 4],
        ["Spider", 15, 7, 9, 15, 15, 2],
        ["Rat", 35, 4, 6, 12, 4, 3],
        ["Slime", 40, 5, 7, 6, 3, 2],
        ["Bat", 25, 2, 4, 20, 7, 2],
        ["Zombie", 18, 8, 11, 5, 19, 2],
        ["Wraith", 35, 3, 6, 8, 9, 4],
        ["Imp", 30, 3, 8, 9, 11, 3],

    ],
    2: [
        ["Ratling Scavenger", 40, 10, 15, 5, 8, 8],
        ["Goblin Thug", 45, 20, 28, 8, 11, 10],
        ["Skeleton Warrior", 50, 15, 25, 7, 10, 11],
        ["Spiderling Swarm", 35, 14, 16, 10, 20, 8],
        ["Bandit Rogue", 55, 20, 30, 12, 9, 12],
        ["Orc Brute", 60, 19, 29, 6, 14, 14],
        ["Zombie Crawler", 45, 18, 24, 3, 17, 13],
        ["Cave Bat", 38, 10, 16, 25, 15, 9],
        ["Giant Spider", 55, 18, 22, 8, 9, 11],
        ["Dark Cultist", 50, 22, 30, 5, 8, 12],

    ]
}

location_list = {  # number, name, description, difficulty
    0: ["Town"],
    1: ["Forest of Shadows",
        """
        A dense forest shrouded in mist, rumored to be haunted 
        by mysterious creatures and ancient spirits.
        """, "Very Easy"
        ],
    2: ["Crystal Caverns",
        """
        A labyrinthine network of caves adorned with shimmering 
        crystals of all colors, echoing with the whispers of 
        forgotten secrets.
        """, "Easy"
        ],
    3: ["Lost Ruins of Eldoria",
        """
        Crumbling remnants of a once-great civilization, now reclaimed 
        by nature and home to lurking dangers and hidden treasures.
        """, "Normal"
        ],
    4: ["Frostpeak Mountains",
        """
        Majestic snow-capped peaks towering above frozen valleys, 
        inhabited by resilient wildlife and perilous ice monsters.
        """, "Hard"
        ],
    5: ["Sunlit Coastline",
        """
        Golden sands stretch as far as the eye can see, kissed by the 
        gentle waves of the azure sea, offering serene beauty and hidden 
        mysteries beneath the surface.
        """, "Very Hard"
        ]
}


def explore_menu(location):
    "Print Explore Menu"
    def explore():
        print("""
                            ==============================
                                     Exploration
                            ==============================
                  
                  """,
              "You are in:", location_list[stats["location"]][0],
              "|  Difficulty:", location_list[stats["location"]][2],
              """

                            [1] Travel to a new location
                            [2] Hunt
                            [3] Return
                  """
              )
        explore_choice = input("Enter your choice: ")
        if explore_choice == "1":
            print("""
                            ==============================
                                    Exploration
                            ==============================
            
                                Choose a location:
                        [1] Forest of Shadows       [Very Easy]
                        [2] Crystal Caverns         [Easy]
                        [3] Lost Ruins of Eldoria   [Normal]
                        [4] Frostpeak Mountains     [Hard]
                        [5] Sunlit Coastline        [Very Hard]
                """
                  )
            stats["location"] = int(input("Enter your choice: "))
            print("\n"*5, "            You have reached",
                  location_list[stats["location"]][0],
                  "\n", location_list[stats["location"]][1])
            input("Press any key")
            explore()
        elif explore_choice == "2":
            hunt_menu()
            explore()
        elif explore_choice != ("1" and "2" and "3"):
            print("Wrong!")
            explore()
    if location is None:
        print("""
                            ==============================
                                     Exploration
                            ==============================
                           You are in Town. Go on a journey!
              
                                  Choose a location:
                        [1] Forest of Shadows       [Very Easy]
                        [2] Crystal Caverns         [Easy]
                        [3] Lost Ruins of Eldoria   [Normal]
                        [4] Frostpeak Mountains     [Hard]
                        [5] Sunlit Coastline        [Very Hard]
                  """
              )
        stats["location"] = int(input("Enter your choice: "))
        print("\n"*5, "            You have reached",
              location_list[stats["location"]][0], "\n", location_list[stats["location"]][1])
        input("Press any key")
        explore()
    elif location is not None:
        explore()


def hunt_menu():
    "Hunt Menu"
    enemy_random = random.choice(monster_list[stats["location"]])
    player_min_max_damage = f"{stats["min_dmg"] + stats['weapon'][1]} - {stats["max_dmg"] + stats['weapon'][2]}"
    enemy_min_max_damage = f"{enemy_random[2]} - {enemy_random[3]}"
    player_stats = {"Damage Min": stats["min_dmg"] + stats['weapon'][1],
                    "Damage Max": stats["max_dmg"] + stats['weapon'][2],
                    "Damage": player_min_max_damage, "Health": stats["hp"],
                    "Dodge": stats["dodge"] + stats['weapon'][5],
                    "Crit": stats["crit"] + stats['weapon'][6], "Weapon": stats['weapon']}
    enemy_stats = {"Damage Min": enemy_random[2], "Damage Max": enemy_random[3],
                   "Damage": enemy_min_max_damage, "Health": enemy_random[1],
                   "Dodge": enemy_random[4], "Crit": enemy_random[5],
                   "EXP": enemy_random[6]}

    print("""
            ==============================
                   Engage in Combat
            ==============================
          
              You encounter""", enemy_random[0], "\n",
          "Take a moment to size up its abilities before diving into battle.", "\n"
          )

    def display_stats(player_name, player_stats, enemy_name, enemy_stats):
        # Define the width of each column
        column_width = 45
        # Format the player and enemy stats
        player_stats_str = "\n".join(
            [f"{key}: {value}" for key, value in list(player_stats.items())[2:]])
        enemy_stats_str = "\n".join(
            [f"{key}: {value}" for key, value in list(enemy_stats.items())[2:]])

        print(f"{player_name:<{column_width}}{enemy_name}")

        # Split the player and enemy stats into lines
        player_stats_lines = player_stats_str.split("\n")
        enemy_stats_lines = enemy_stats_str.split("\n")
        # Print the formatted output

        for player_line, enemy_line in zip(player_stats_lines, enemy_stats_lines):
            print(f"{player_line:<{column_width}}{enemy_line}")

    display_stats(stats["name"], player_stats, enemy_random[0], enemy_stats)
    choice = input("Attack? [Y]: ")
    if choice == "y" or "Y":
        fight(enemy_stats, enemy_random[0])


def fight(enemy_stats, enemy_name):
    "Fighting"
    player_health = stats["hp"]
    enemy_health = enemy_stats["Health"]
    print("\n", "               Battle started!")
    print(
        stats["name"], "health:", player_health,
        enemy_name, "health:", enemy_health, "\n"
    )
    input("Press any key ")
    while player_health > 0 and enemy_health > 0:
        enemy_dmg = random.randrange(
            enemy_stats["Damage Min"], enemy_stats["Damage Max"] + 1)
        player_dmg = random.randrange(stats["min_dmg"] + stats['weapon'][1],
                                      stats["max_dmg"] + stats['weapon'][2] + 1)

        if random.randrange(0, 101) <= stats["dodge"] + stats['weapon'][6]:
            print("\n"*6)
            print(f"{Col.GREEN}Player dodged the attack!{Col.RESET}")
            input("Press any key ")
        else:
            player_health -= enemy_dmg
            if random.randrange(0, 101) <= enemy_stats["Crit"]:
                print(f"{Col.RED}Enemy critical hit!{Col.RESET}")
                player_health -= enemy_dmg
                print(enemy_name, "deals", enemy_dmg *
                      2, "critical damage!", "\n"*2)
                print(stats["name"], "health:", player_health,
                      enemy_name, "health:", enemy_health)
                input("Press any key ")
            else:
                print("\n"*5)
                print(enemy_name, "deals", enemy_dmg, "damage!", "\n"*2)
                print(stats["name"], "health:", player_health,
                      enemy_name, "health:", enemy_health)
                input("Press any key ")

        if player_health <= 0:
            print("\n"*6, "You died!", "\n")
            input("Press any key ")
            break

        if random.randrange(0, 101) <= enemy_stats["Dodge"]:
            print("\n"*6)
            print(f"{Col.RED}Enemy dodged the attack!{Col.RESET}")
            input("Press any key ")
        else:
            enemy_health -= player_dmg
            if random.randrange(0, 101) <= stats["crit"] + stats['weapon'][5]:
                print(f"{Col.GREEN}Critical hit!{Col.RESET}")
                enemy_health -= player_dmg
                print("\n"*5)
                print(stats["name"], "deals", player_dmg *
                      2, "critical damage!", "\n"*2)
                print(stats["name"], "health:", player_health,
                      enemy_name, "health:", enemy_health)
                input("Press any key ")
            else:
                print("\n"*5)
                print(stats["name"], "deals", player_dmg, "damage!", "\n"*2)
                print(stats["name"], "health:", player_health,
                      enemy_name, "health:", enemy_health)
                input("Press any key ")

        if enemy_health <= 0:
            stats_update(enemy_stats["EXP"])
            loot(stats['location'])
            input("Press any key")


def character_creation():
    "Create a character"

    clear_stats()

    print("""
                            ==============================
                                 Start a new journey!
                            ==============================
          
                    Create your character and begin your adventure!
                    Let's start by creating your character and adding
                    some stat points.
                  """
          )
    while True:
        stats["name"] = input("Enter the character name: ")
        if check_existing_character(stats["name"]):
            print("Character with that name already exists. Please choose a different name.")
        else:
            print("Character name is available.")
            break


    print("""
                    Customize your strength and vitality points to 
                    better tailor your character's abilities for the 
                    challenges ahead!
                  """
          )

    i = 5
    while i > 0:
        print("\n"*2)
        print("                             STR:",
              stats["str"], "    |    ", "VIT:", stats["vit"])
        print("""
                      [1] Add 1 STR     |    [2] Add 1 VIT
            """
              )
        print("                         Available stat points:", i)
        skill = input("Choose stat: ")
        if skill == "1":
            stats["str"] += 1
            i -= 1
            skill = None
        elif skill == "2":
            stats["vit"] += 1
            i -= 1
            skill = None
        else:
            print("Wrong!")
            skill = None

    if i == 0:
        print("\n"*4)
        print("                             STR:",
              stats["str"], "    |    ", "VIT:", stats["vit"])
        input("Press any key")
        return game_menu()


def stats_update(gained_exp=0):

    if gained_exp != 0:
        stats["exp"] += gained_exp
        print(f"""Player gained {Col.YELLOW}{gained_exp}{
              Col.RESET} experience points. [{stats["exp"]}/{stats["next_lvl"]}]""")

        while stats["exp"] >= stats["next_lvl"]:
            stats["lvl"] += 1
            stats["exp"] -= stats["next_lvl"]
            print(f"You leveled up to level {
                  stats["lvl"]}! Press [1] + STR | [2] + VIT")
            choice = input("Choose stat: ")
            if choice == "1":
                stats["str"] += 1
            elif choice == "2":
                stats["vit"] += 1
            else:
                print("Error")

    stats["next_lvl"] = round(stats["lvl"] ** 1 * 5)  # next lvl



    stats["min_dmg"] = round(1 + stats["str"] + (stats["lvl"]*1.1))

    stats["max_dmg"] = round((4 + stats["str"] + stats["lvl"])*1.15)

    stats["hp"] = round(23 + (stats["lvl"]*1.5) + (stats["vit"]*2.5))

    stats["crit"] = round((stats["str"]*0.3), 1)
    stats["dodge"] = round((stats["vit"]*0.3), 1)


def loot(difficulty):
    weights = {
        1: [50, 30, 15, 4, 1],
        2: [40, 34, 18, 6, 2],
        3: [30, 38, 21, 8, 3],
        4: [20, 42, 24, 10, 4],
        5: [10, 46, 27, 12, 5]
    }
    tier = random.choices(list(weapon_list.keys()), weights[difficulty])
    int_tier = int(''.join(map(str, tier)))
    random_loot = random.choices(weapon_list[int_tier])
    stats['loot'] = random_loot[0]
    weapon_stats = {"Damage": f"{stats["weapon"][1]} - {stats['weapon'][2]}",
                    "STR": stats["weapon"][3], "VIT": stats["weapon"][4],
                    "Dodge": stats["weapon"][5], "Crit": stats["weapon"][6]}
    loot_stats = {"Damage": f"{stats["loot"][1]} - {stats['loot'][2]}",
                  "STR": stats["loot"][3], "VIT": stats["loot"][4],
                   "Dodge": stats["loot"][5], "Crit": stats["loot"][6],}

    def weapons_stats(weapon_name, weapon_stats, loot_name, loot_stats, color):

        # Define the width of each column
        column_width = 45

        # Format the player and enemy stats
        loot_str = "\n".join(
            [f"{key}: {value}" for key, value in list(weapon_stats.items())])
        weapon_str = "\n".join(
            [f"{key}: {value}" for key, value in list(loot_stats.items())])

        # Split the player and enemy stats into lines
        weapon_stats_lines = loot_str.split("\n")
        loot_stats_lines = weapon_str.split("\n")

        # Print the formatted output
        if color == 1:
            print(f"{weapon_name:<{column_width}}{Col.GREEN}{loot_name}{Col.RESET}")
            for weapon_line, loot_line in zip(weapon_stats_lines, loot_stats_lines):
                print(f"{weapon_line:<{column_width}}{loot_line}")

        if color == 2:
            print(f"{weapon_name:<{column_width}}{Col.BLUE}{loot_name}{Col.RESET}")
            for weapon_line, loot_line in zip(weapon_stats_lines, loot_stats_lines):
                print(f"{weapon_line:<{column_width}}{loot_line}")

        if color == 3:
            print(f"{weapon_name:<{column_width}}{Col.RED}{loot_name}{Col.RESET}")
            for weapon_line, loot_line in zip(weapon_stats_lines, loot_stats_lines):
                print(f"{weapon_line:<{column_width}}{loot_line}")

        if color == 4:
            print(f"{weapon_name:<{column_width}}{Col.MAGENTA}{loot_name}{Col.RESET}")
            for weapon_line, loot_line in zip(weapon_stats_lines, loot_stats_lines):
                print(f"{weapon_line:<{column_width}}{loot_line}")

    weapons_stats(stats["weapon"][0], weapon_stats,  stats["loot"][0], loot_stats, int_tier)


    if int_tier != 0:
        equip = input("Do you want to equip the weapon? [Y]")
        if equip == 'Y':
            stats['weapon'] = stats['loot']
            stats['loot'] = weapon_list[0]
            equip = None

    stats['loot'] = weapon_list[0]


def stats_check():
    "Check statistics"

    stat_check = {"Name": stats["name"],
                  "Damage": f"{stats["min_dmg"] + stats["weapon"][1]} - {stats["max_dmg"] + stats['weapon'][2]}",
                    "Health": stats["hp"],
                    "STR": f"{stats["str"] + stats["weapon"][3]}    |    VIT: {stats["vit"] + stats["weapon"][5]}",
                    "Dodge": f"{stats["dodge"] + stats["weapon"][5]}    |    Crit: {stats["crit"] + stats["weapon"][6]}",
                    "Lvl": f"{stats["lvl"]}     |     Exp {stats["exp"]} / {stats["next_lvl"]} ",
                    "Weapon": stats["weapon"][0]}

    stat_check_str = "\n".join(
        [f"{key}: {value}" for key, value in list(stat_check.items())])

    print(stat_check_str)
    input("Press any key")


def main():
    "Main Menu"
    while True:
        print(  # print main menu
            """
                                ==============================
                                        Main Menu
                                ==============================
                                        
                                [1] New Game
                                [2] Load Game
                                [3] Options
                                [0] Exit Game      
                                """
        )
        main_choice = input("Choose: ")
        if main_choice == "1":  # start game
            return character_creation()
        elif main_choice == "2":  # load game
            while True:
                load_name = input("Enter the character name: ")
                if check_existing_character(load_name):
                    game_menu(False, load_name)
                else:
                    print("Player do not exist")
                    input("Press any key")
                    break
        elif main_choice == "3":  # options
            print("RPG Game v 0.0.1")
            time.sleep(1.2)
        elif main_choice == "9":  # exit
            print("Exiting the game. Goodbye!")
            break
        else:
            print(f"{Col.RED}Invalid choice.{Col.RESET}")


def game_menu(char_is_new=True, name=None):
    global stats
    if char_is_new is False:
        try:
            char_file_path = f"{folder_path}\\" + name + ".json"
            with open(char_file_path, "r", encoding="utf-8") as json_file:
                stats = json.load(json_file)
        except FileNotFoundError:
            print(f"File '{char_file_path}' not found.")
            return main()
        except json.JSONDecodeError:
            print(f"Error decoding player data in '{char_file_path}'.")
            return main()
    while True:
        stats_update()
        print(  # printed game menu
            """
                    ==============================
                                Game Menu
                    ==============================
                            
                    [1] Explore
                    [2] Inventory/Stats
                    [3] Quests
                    [4] Shop
                    [5] Save Game
                    [9] Exit to Main Menu   
                    """
        )
        game_choice = input("Enter your choice: ")
        if game_choice == "1":  # explore
            explore_menu(stats["location"])
        elif game_choice == "2":  # stats
            stats_update()
            stats_check()
        elif game_choice == "5":  # save game
            return save_game(stats['name'])
        elif game_choice == "9":  # back to menu
            clear_stats()
            return main()
        else:
            print(f"{Col.RED}Invalid choice.{Col.RESET}")


def save_game(name):
    file_path = os.path.join(folder_path, f"{name}.json")
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(stats, json_file)
    return main()

def clear_stats():
    for key in list(stats)[:9]:
        stats[key] = 0
    stats["lvl"] = 1
    stats["location"] = None
    stats["class"] = None
    stats["weapon"] = ["None", 0, 0, 0, 0, 0, 0]
    stats["loot"] = ["None", 0, 0, 0, 0, 0, 0]

def check_existing_character(name):
    # Check if a file with the given character name already exists
    file_name = name + ".json"
    file_path = os.path.join(folder_name, file_name)
    return os.path.exists(file_path)


main()
