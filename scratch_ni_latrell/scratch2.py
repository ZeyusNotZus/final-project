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
    ["T", ".", "~", "~", "R", ".", "R", ".", "."],
    ["T", ".", "~", "~", ".", ".", ".", ".", "T"],
    ["T", "T", "T", "T", "T", "T", "T", "T", "T"]
]

#Game Functions
def reset():
    global game_data, current_world, rocks
    current_world = [row.copy() for row in world1]
    game_data = {
        "state": "playing",
        "on": ".",
        "inventory": ".",
        "shrooms": 0
    }
    rocks = {(r, c): "." for r, c in find_object(current_world, "R")}


def find_object(world, rep):
    positions = []
    for r, row in enumerate(world):
        for c, tile in enumerate(row):
            if tile == rep:
                if rep == "L":
                    return r, c
                elif rep == "R":
                    positions.append((r, c))
    if rep == "R":
        return positions

def player_move(pos, direction, world):
    r, c = pos
    dr, dc = direction


    #When pushing rocks
    if (0 <= r + dr < n_rows) and (0 <= c + dc < n_cols) and world[r + dr][c + dc] == "R":
        if (0 <= r + 2*dr < n_rows) and (0 <= c + 2*dc < n_cols) and world[r + 2*dr][c + 2*dc] in (".", "_", "~"):
            
            #Pushing rock to water
            if world[r + 2*dr][c + 2*dc] == "~":
                current_world[r + 2*dr][c + 2*dc] = "_"
                current_world[r + dr][c + dc] = rocks.pop((r + dr, c + dc))
                return r + dr, c + dc, current_world[r + dr][c + dc]

            #Pushing rock normally
            elif world[r + 2*dr][c + 2*dc] in (".", "_"):
                rocks[(r + 2*dr, c + 2*dc)] = current_world[r + 2*dr][c + 2*dc]
                current_world[r + 2*dr][c + 2*dc] = "R"
                current_world[r + dr][c + dc] = rocks.pop((r + dr, c + dc))
                return r + dr, c + dc, current_world[r + dr][c + dc]
        else:
            return r, c, current_world[r][c]  


    #Regular Movement
    elif (0 <= r + dr < n_rows) and (0 <= c + dc < n_cols) and world[r + dr][c + dc] in valid_tiles:
        return r + dr, c + dc, current_world[r + dr][c + dc]
    else:
        return r, c, current_world[r][c] 

#Independent Variables
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

#Create World
reset()
#Quit condition. Should be placed somewhere else
quit = False


#Game Loop
while True:
    clear_screen()

    print("\n".join("".join(row) for row in current_world))
    print()
    print(f"Player tile: {game_data["on"]}")
    print(f"Inventory: {game_data["inventory"]}\n")
    if game_data["state"] == "gameover":
        print("Game Over (x_x)")
    
    if game_data["state"] == "playing":
        action = input("Move (W, A, S, D) \nPickup (P)\nReset (R) \nQuit (Q): \n").lower()
    elif game_data["state"] == "gameover":
        action = input("Reset (R) \nQuit (Q): \n").lower()

    for act in action:
        if act not in player_input:
            break
        elif act == "q":
            quit = True
        elif act == "r":
            reset()
        elif game_data["state"] == "playing":
            if act == "p" and game_data["on"] in pickup and game_data["inventory"] == ".":
                game_data["inventory"] = game_data["on"]
                game_data["on"] = "."
            elif act != "p":
                player_row, player_col = find_object(current_world, "L")
                current_world[player_row][player_col] = game_data["on"]
                new_r, new_c, game_data["on"] = player_move((player_row, player_col), player_input[act], current_world)
                if game_data["on"] == "~":
                    game_data["state"] = "gameover"
                else:
                    current_world[new_r][new_c] = "L"

    if quit:
        break
