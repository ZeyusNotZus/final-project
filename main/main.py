import os 
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

world1 = [
    ["T", "T", "T", "T", "T", "T", "T", "T", "T"],
    ["T", ".", ".", ".", ".", ".", ".", ".", "T"],
    ["T", "_", "_", ".", ".", ".", ".", ".", "T"],
    ["T", ".", ".", ".", ".", ".", "+", ".", "T"],
    ["T", "x", "*", ".", "L", "T", ".", ".", "T"],
    ["T", ".", ".", ".", ".", ".", ".", ".", "T"],
    ["T", ".", "~", "~", ".", ".", ".", ".", "T"],
    ["T", ".", "~", "~", ".", ".", ".", ".", "T"],
    ["T", "T", "T", "T", "T", "T", "T", "T", "T"]
]

current_world = world1.copy()

player_input = {
    "w": (-1,0),
    "s": (1,0),
    "a": (0,-1),
    "d": (0,1),
    "r": "reset",
    "p": "pickup",
    "q": "quit"
}

valid_tiles = (".", "+", "x", "~", "*", "_")

pickup = ("x", "*")

n_rows = len(current_world)
n_cols = len(current_world[0])

game_data = {
        "on": ".",
        "inventory": [".", "."],
        "shrooms": 0
    }

game_state = "playing"

def reset():
    current_world = world1.copy()
    game_data["on"] = "."
    game_data["inventory"] = [".", "."]
    game_data["shrooms"] = 0


def find_player(world, rep):
    for r, row in enumerate(world):
        for c, tile in enumerate(row):
            if tile == rep:
                return r, c

def player_move(pos, direction, world):
    r, c = pos
    dr, dc = direction
    if (0 <= r + dr < n_rows) and (0 <= c + dc < n_cols) and world[r + dr][c + dc] in valid_tiles:
        return r + dr, c + dc
    return r, c

while True:
    clear_screen()

    if "L" not in (x for y in current_world for x in y):
        print("\n".join("".join(row) for row in current_world))
        print()
        print(f"Player tile: {game_data["on"]}")
        print(f"Inventory: {game_data["inventory"][0]}\n")
        print("Game Over x_x\n")
        break

    print("\n".join("".join(row) for row in current_world))
    print()
    print(f"Player tile: {game_data["on"]}")
    print(f"Inventory: {game_data["inventory"][0]}\n")

    

    action = input("Move (W, A, S, D) \nPickup or Drop (P)\nReset (R) \nQuit (Q): ").lower()
    if "q" in action:
       break


    for act in action:
        if act not in player_input:
            break
        elif act == "r":
            reset()
        elif act == "p" and game_data["on"] in pickup and game_data["inventory"][0] == ".":
            game_data["inventory"][1] = game_data["inventory"][0]
            game_data["inventory"][0] = game_data["on"]
            game_data["on"] = game_data["inventory"][1]
        elif act != "p":
            player_row, player_col = find_player(current_world, "L")
            current_world[player_row][player_col] = game_data["on"]
            new_r, new_c = player_move((player_row, player_col), player_input[act],current_world)
            game_data["on"] = current_world[new_r][new_c]
            if game_data["on"] == "~":
                break
            current_world[new_r][new_c] = "L"