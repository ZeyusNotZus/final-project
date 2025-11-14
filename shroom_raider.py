import os 
from argparse import ArgumentParser

"""Default world when no world is imported to game"""
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

"""Finds positions of the player and rocks in the world
   player position is returned as r, c while rocks are returned as a list of tuples (r,c)"""
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
        return r, c, world[r][c]
    
    # Checking target tile
    target_tile = world[target_r][target_c]

    # Regular movement
    if target_tile in valid_tiles:
        return target_r, target_c, target_tile
    
    # Chopping trees
    if target_tile == "T" and game_data["inventory"] == "x":
        world[target_r][target_c] = "."
        game_data["inventory"] = "."
        return target_r, target_c, "."
    
    # Burning trees
    elif target_tile == "T" and game_data["inventory"] == "*":
        def burn(r, c):
            if 0 <= r < n_rows and 0 <= c < n_cols and world[r][c] == "T":
                world[r][c] = "."
                for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    burn(r + dr, c + dc)    

        burn(target_r, target_c)
        game_data["inventory"] = "."
        return target_r, target_c, "."
        
    # When pushing rocks
    if (0 <= target_r < n_rows) and (0 <= target_c < n_cols) and world[target_r][target_c] == "R":
        if (0 <= target_r + dr < n_rows) and (0 <= target_c + dc < n_cols) and world[target_r + dr][target_c + dc] in (".", "_", "~"):
            
            # Pushing rock to water
            if world[target_r + dr][target_c + dc] == "~":
                world[target_r + dr][target_c + dc] = "_"
                world[target_r][target_c] = rocks.pop((target_r, target_c))
                return target_r, target_c, world[target_r][target_c]

            # Pushing rock normally
            elif world[target_r + dr][target_c + dc] in (".", "_"):
                rocks[(target_r + dr, target_c + dc)] = world[target_r + dr][target_c + dc]
                world[target_r + dr][target_c + dc] = "R"
                world[target_r][target_c] = rocks.pop((target_r, target_c))
                return target_r, target_c, world[target_r][target_c]
        else:
            return r, c, world[r][c]  

    return r, c, world[r][c]  

# Variables
current_world = [row.copy() for row in world1]
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
       
    # Arg Parse
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", help="Stage file")
    parser.add_argument("-m", "--moves", help="Moves")
    parser.add_argument("-o", "--output", help = "Output file")
    args = parser.parse_args()

    # Checking if a map file was given
    if args.file:
        with open(args.file, encoding='utf-8') as f:
            rows, cols = [int(x) for x in f.readline().strip().split()]
            rest = [line.strip() for line in f if line.strip()]
            world = "".join(rest)
            global world1
            world1 = [list(world[i * cols:(i + 1) * cols]) for i in range(rows)] #  <--------------why is world1 grayed out

            global n_rows, n_cols
            n_rows = rows
            n_cols = cols

    # Checking if moves are used in advance
    if args.moves:
        move_queue = args.moves
    else:
        move_queue = None

    # Game Loop
    while True:

        #C hecking if outputfile given
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

        if game_data["state"] == "gameover":
            if game_data["shrooms"] >= game_data["total_shrooms"]:
                print("You Win!")
            else:
                print("Game Over")

        if game_data["state"] == "playing":
            if move_queue:
                action = move_queue
                move_queue = None
            else:
                action = input("Move (W, A, S, D) \nPickup (P)\nReset (!) \n").lower()
        elif game_data["state"] == "gameover":
            action = input("Reset (!)\n").lower()

        for act in action:
            if act not in player_input:
                break
            elif act == "!":
                reset()
            elif game_data["state"] == "playing":
                if act == "p" and game_data["player_tile"] in pickup and game_data["inventory"] == ".":
                    game_data["inventory"] = game_data["player_tile"]
                    game_data["player_tile"] = "."
                elif act != "p":
                    player_row, player_col = find_object(current_world, "L")
                    current_world[player_row][player_col] = game_data["player_tile"]
                    new_r, new_c, game_data["player_tile"] = player_move((player_row, player_col), player_input[act], current_world)
                    if game_data["player_tile"] == "~":
                        game_data["state"] = "gameover"
                    else:
                        if game_data["player_tile"] == "+":
                            game_data["player_tile"] = "."
                            game_data["shrooms"] += 1
                            if game_data["shrooms"] >= game_data["total_shrooms"]:
                                game_data["state"] = "gameover"
                        current_world[new_r][new_c] = "L"

if __name__ == "__main__":
    main()
