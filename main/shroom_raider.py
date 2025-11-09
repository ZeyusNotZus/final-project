import os
from game_logic import find_object, reset, player_move

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# World map
world1 = [
    ["+", "T", "T", "T", "T", "T", "T", "T", "T"],
    ["T", ".", ".", ".", ".", ".", ".", ".", "T"],
    ["T", "_", "_", ".", ".", ".", ".", ".", "T"],
    ["T", ".", ".", ".", ".", ".", "+", ".", "T"],
    ["T", "x", "*", ".", "L", "T", ".", ".", "T"],
    ["T", ".", ".", ".", ".", ".", ".", ".", "T"],
    ["T", ".", "~", "~", "R", ".", "R", ".", "."],
    ["T", ".", "~", "~", ".", ".", ".", ".", "T"],
    ["T", "T", "T", "T", "T", "T", "T", "T", "T"]
]

# Initialization
current_world, game_data, rocks = reset(world1)

player_input = {
    "w": (-1,0),
    "s": (1,0),
    "a": (0,-1),
    "d": (0,1),
    "p": "pickup",
    "!": "reset",
    "q": "quit"
}
valid_tiles = (".", "+", "x", "~", "*", "_")
pickup = ("x", "*")

quit = False

# Game Loop
while True:
    clear_screen()

    print("\n".join("".join(row) for row in current_world))
    print()
    print(f"Shrooms: {game_data["shrooms"]}/{game_data["total_shrooms"]}")
    print(f"Inventory: {game_data["inventory"]}")
    print(f"Player tile: {game_data["on"]}\n")

    if game_data["state"] == "gameover":
        if game_data["shrooms"] >= game_data["total_shrooms"]:
            print("You Win!")
        else:
            print("Game Over\n")

    if game_data["state"] == "playing":
        action = input("Move (W, A, S, D) \nPickup (P)\nReset (!) \nQuit (Q): \n").lower()
    elif game_data["state"] == "gameover":
        action = input("Reset (!) \nQuit (Q): \n").lower()

    for act in action:
        if act not in player_input:
            break
        elif act == "q":
            quit = True
        elif act == "!":
            current_world, game_data, rocks = reset(world1)
        elif game_data["state"] == "playing":
            if act == "p" and game_data["on"] in pickup and game_data["inventory"] == ".":
                game_data["inventory"] = game_data["on"]
                game_data["on"] = "."
            elif act != "p":
                #This part can probably be but under the player move function
                player_row, player_col = find_object(current_world, "L")
                current_world[player_row][player_col] = game_data["on"]
                new_r, new_c, game_data["on"] = player_move(
                    (player_row, player_col),
                    player_input[act],
                    current_world,
                    game_data,
                    rocks,
                    valid_tiles
                    )
                
                if game_data["on"] == "~":
                    game_data["state"] = "gameover"
                else:
                    if game_data["on"] == "+":
                        game_data["on"] = "."
                        game_data["shrooms"] += 1
                        if game_data["shrooms"] >= game_data["total_shrooms"]:
                            game_data["state"] = "gameover"
                    current_world[new_r][new_c] = "L"
    
    if quit:
        break