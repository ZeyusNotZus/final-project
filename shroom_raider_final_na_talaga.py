import os 
from argparse import ArgumentParser

# Game Functions

"""Clears the terminal screen"""
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

"""Resets game to initial state of world and initial game data values"""
def reset():
    global game_data, current_world, rocks
    current_world = [row.copy() for row in world1]
    game_data = {
        "state": "playing",
        "player_tile": ".",
        "inventory": ".",
        "total_shrooms":  "".join(x for y in world1 for x in y).count("+"),
        "shrooms": 0
    }
    rocks = {(r, c): "." for r, c in find_object(current_world, "R")}

"""Finds positions of the object in the world"""
def find_object(world, rep):
    for r, row in enumerate(world):
        for c, tile in enumerate(row):
            if tile == rep:
                yield r, c

"""Movement of player in given direction and player interactions with game world"""
def player_move(pos, direction, world):
    global game_data, rocks, valid_tiles
    r, c = pos
    dr, dc = direction
    target_r, target_c = r + dr, c + dc
    n_rows = len(world)
    n_cols = len(world[0])

    # Out of bounds
    if not (0 <= target_r < n_rows and 0 <= target_c < n_cols):
        return

    #Checking target tile
    target_tile = world[target_r][target_c]

    # Regular movement
    if target_tile in valid_tiles:
        if target_tile == "~":
            world[r][c] = game_data["player_tile"]
            game_data["player_tile"] = world[target_r][target_c]
            game_data["state"] = "gameover"
        elif target_tile == "+":
            world[r][c] = game_data["player_tile"]
            game_data["player_tile"] = "."
            world[target_r][target_c] = "L"
            game_data["shrooms"] += 1
            if game_data["shrooms"] >= game_data["total_shrooms"]:
                game_data["state"] = "gameover"
        else:
            world[r][c] = game_data["player_tile"]
            game_data["player_tile"] = world[target_r][target_c]
            world[target_r][target_c] = "L"
    
    # Chopping trees
    if target_tile == "T" and game_data["inventory"] == "x":
        game_data["inventory"] = "."
        world[r][c] = game_data["player_tile"]
        game_data["player_tile"] = "."
        world[target_r][target_c] = "L"
    
    # Burning trees
    elif target_tile == "T" and game_data["inventory"] == "*":
        def burn(r, c):
            if 0 <= r < n_rows and 0 <= c < n_cols and world[r][c] == "T":
                world[r][c] = "."
                for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    burn(r + dr, c + dc)    

        burn(target_r, target_c)
        game_data["inventory"] = "."
        world[r][c] = game_data["player_tile"]
        game_data["player_tile"] = "."
        world[target_r][target_c] = "L"
        
    # When pushing rocks
    if world[target_r][target_c] == "R":
        if (0 <= target_r + dr < n_rows) and (0 <= target_c + dc < n_cols) and world[target_r + dr][target_c + dc] in (".", "_", "~"):
            
            # Pushing rock to water
            if world[target_r + dr][target_c + dc] == "~":
                world[target_r + dr][target_c + dc] = "_"
                world[r][c] = game_data["player_tile"]
                game_data["player_tile"] = rocks.pop((target_r, target_c))
                world[target_r][target_c] = "L"

            # Pushing rock normally
            elif world[target_r + dr][target_c + dc] in (".", "_"):
                rocks[(target_r + dr, target_c + dc)] = world[target_r + dr][target_c + dc]
                world[target_r + dr][target_c + dc] = "R"
                world[r][c] = game_data["player_tile"]
                game_data["player_tile"] = rocks.pop((target_r, target_c))
                world[target_r][target_c] = "L"

        else:
            pass   

"""Picking up items"""
def pick_up():
    if game_data["player_tile"] in pickup and game_data["inventory"] == ".":
        game_data["inventory"] = game_data["player_tile"]
        game_data["player_tile"] = "."

# Variables
world1 = [
    ["R", "R", "R", "T", "T", "T", "T", "T", "T"],
    ["R", "+", "R", ".", ".", ".", ".", "L", "T"],
    ["R", "T", "R", ".", ".", ".", "+", ".", "T"],
    ["T", ".", ".", ".", ".", ".", ".", ".", "T"],
    ["T", "x", ".", ".", "T", "T", "T", ".", "T"],
    ["T", ".", ".", ".", "T", "R", "T", ".", "T"],
    ["T", "~", "*", ".", "T", "T", "T", ".", "T"],
    ["T", "+", "~", ".", ".", ".", ".", ".", "T"],
    ["T", "T", "T", "T", "T", "T", "T", "T", "T"]
    ]
player_input = {
    "w": (-1,0),
    "s": (1,0),
    "a": (0,-1),
    "d": (0,1),
    "p": "pickup",
    "!": "reset",
}
valid_tiles = (".", "+", "x", "~", "*", "_")
pickup = ("x", "*")
pushable = ("R")

# Convert ASCII to emoji
tile_conversions = {
    "R": "🪨",
    "T": "🌲",
    "~": "🟦",
    "x": "🪓",
    ".": "  ",
    "_": "⬜",
    "L": "🧑",
    "*": "🔥",
    "+": "🍄",
}

"""Main game function"""
def main():
    global world1, current_world

    # Arg Parse
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", help="Stage file")
    parser.add_argument("-m", "--moves", help="Moves")
    parser.add_argument("-o", "--output", help = "Output file")
    args = parser.parse_args()

    # Checking if a map file was given
    if args.file:
        with open(args.file, encoding='utf-8') as f:
            n_rows, n_cols = [int(x) for x in f.readline().strip().split()]
            rest = [line.strip() for line in f if line.strip()]
            world = "".join(rest)
            world1 = [list(world[i * n_cols:(i + 1) * n_cols]) for i in range(n_rows)]
    else:
        current_world = world1
        n_rows = len(current_world)
        n_cols = len(current_world[0])

    # Checking if moves are used in advance
    if args.moves:
        move_queue = args.moves.lower()
    else:
        move_queue = None

    # Create World
    reset()

    # Check if there is exactly one Laro in the game world
    player_position = find_object(current_world, "L")
    if player_position is None:
        print("Error: No player \"L\" was found in this world!")
        return
    elif isinstance(player_position, list) and len(player_position) > 1:
        print("Error: Multiple player \"L\"s were found in this world!")
        return

    # Game Loop
    while True:

        #Checking if outputfile given
        if args.output and move_queue == None:
            with open(args.output, "w", encoding='utf-8') as f:
                if game_data["shrooms"] >= game_data["total_shrooms"]:
                    f.write("CLEAR\n")
                else:
                    f.write("NO CLEAR\n")
                f.write(f"{n_rows} {n_cols}\n")
                f.write("\n".join("".join(row) for row in current_world))
                f.close()
            break

        elif not args.output:
            clear_screen()
            for row in current_world:
                print("".join(tile_conversions.get(tile, tile) for tile in row))
            print()
            print(f"Shrooms: {game_data["shrooms"]}/{game_data["total_shrooms"]}")
            print(f"Inventory: {tile_conversions[game_data["inventory"]]}")
            print(f"Player tile: {tile_conversions[game_data["player_tile"]]}\n")

        if game_data["state"] == "playing":
            if move_queue:
                action = move_queue
                move_queue = None
            else:
                action = input("Move Up    [W]\nMove Down  [S]\nMove Left  [A]\nMove Right [D]\nPickup     [P]\nReset      [!] \n").lower()
        elif game_data["state"] == "gameover":
            if game_data["shrooms"] >= game_data["total_shrooms"]:
                print("You Win!\n")
            else:
                print("Game Over\n")
            break

        for act in action:
            if act not in player_input:
                break
            elif game_data["state"] == "playing":
                if act == "!":
                    reset()
                elif act == "p":
                    pick_up()
                else:
                    player_row, player_col = next(find_object(current_world, "L"))
                    player_move((player_row, player_col), player_input[act], current_world)

if __name__ == "__main__":
    main()