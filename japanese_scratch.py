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
    ["T", ".", "~", "~", "R", ".", "R", ".", "T"],
    ["T", ".", "~", "~", ".", ".", ".", ".", "T"],
    ["T", "T", "T", "T", "T", "T", "T", "T", "T"]
]

#Game Functions
def reset():
    global game_data, current_world
    current_world = [row.copy() for row in world1]
    game_data = {
        "state": "playing",
        "on": ".",
        "inventory": [".", "."],
        "shrooms": 0
    }


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
    else:
        return r, c

#Independent Variales
current_world = [row.copy() for row in world1]
player_input = {
    "w": (-1,0),
    "s": (1,0),
    "a": (0,-1),
    "d": (0,1),
    "p": "pickup",
    "r": "reset",
    "q": "quit"
}
valid_tiles = (".", "+", "x", "~", "*", "_")
pickup = ("x", "*")
pushable = ("R")
n_rows = len(current_world)
n_cols = len(current_world[0])

RESET = "\033[0m"

COLORS = {
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[94m",
    "white": "\033[37m",
    "gray": "\033[90m",
    "light_green": "\033[92m",

}

tile_conversions = {
    "R": COLORS["gray"] + "ロ" + RESET,          #katakana ro
    "T": COLORS["green"] + "木" + RESET,          #kanji tree
    "~": COLORS["blue"] + "ミ" + RESET,          #katakana mi in mizu
    "x": COLORS["white"] + "中" + RESET,          #kanji for inside 
    ".": COLORS["yellow"] + "・" + RESET,
    "_": COLORS["gray"] + "ー" + RESET,
    "L": COLORS["white"] + "六" + RESET,
    "*": COLORS["white"] + "火" + RESET,
    "+": COLORS["red"] + "兄" + RESET,
}

#Dependent Variables
game_data = {
        "state": "playing",
        "on": ".",
        "inventory": ".",
        "shrooms": 0
    }


#Game Loop
while True:
    clear_screen()

    for row in current_world:
        print("".join(tile_conversions.get(tile, tile) for tile in row))

    print()
    print(f"Player tile: {game_data["on"]}")
    print(f"Inventory: {game_data["inventory"][0]}\n")
    if game_data["state"] == "gameover":
        print("Game Over (x_x)")

    
    if game_data["state"] == "playing":
        action = input("Move (W, A, S, D) \nPickup or Drop (P)\nReset (R) \nQuit (Q): ").lower()
    elif game_data["state"] == "gameover":
        action = input("Reset (R) \nQuit (Q):").lower()

    if "q" in action:
       break

    for act in action:
        if act not in player_input:
            break
        elif act == "r":
            reset()
        elif game_data["state"] == "playing":
            if act == "p" and game_data["on"] in pickup and game_data["inventory"] == ".":
                game_data["inventory"] = game_data["on"]
                game_data["on"] = "."
            elif act != "p":
                player_row, player_col = find_player(current_world, "L")
                current_world[player_row][player_col] = game_data["on"]
                new_r, new_c = player_move((player_row, player_col), player_input[act], current_world)
                game_data["on"] = current_world[new_r][new_c]
                if game_data["on"] == "~":
                    game_data["state"] = "gameover"
                else:
                    current_world[new_r][new_c] = "L"