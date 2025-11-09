# Resets world to its original state
def reset(world1): #<------ Using world 1 as default world? Idk how to implement with world import
    current_world = [row.copy() for row in world1]
    game_data = {
        "state": "playing",
        "on": ".",
        "inventory": ".",
        "total_shrooms":  "".join(x for y in world1 for x in y).count("+"),
        "shrooms": 0
    }
    rocks = {(r, c): "." for r, c in find_object(current_world, "R")}
    return current_world, game_data, rocks

# Returns positions of Laro and Rocks
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
    
# Player movement, chopping, burning, and rock pushing logic
def player_move(pos, direction, world, game_data, rocks, valid_tiles):
    current_world = world
    r, c = pos
    dr, dc = direction
    n_rows, n_cols = len(current_world), len(current_world[0])
    target_r, target_c = r + dr, c + dc

    #Out of bounds
    if not (0 <= target_r < n_rows and 0 <= target_c < n_cols):
        return r, c, current_world[r][c]
    
    #Checking Target Tile
    target_tile = current_world[target_r][target_c]

    #Regular Movement
    if target_tile in valid_tiles:
        return target_r, target_c, target_tile
    
    #Chopping Trees
    if target_tile == "T" and game_data["inventory"] == "x":
        current_world[target_r][target_c] = "."
        game_data["inventory"] = "."
        return target_r, target_c, "."
    
    #Burning Trees
    elif target_tile == "T" and game_data["inventory"] == "*":
        def burn(r, c):
            if 0 <= r < n_rows and 0 <= c < n_cols and world[r][c] == "T":
                world[r][c] = "."
                for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    burn(r + dr, c + dc)    

        burn(target_r, target_c)
        game_data["inventory"] = "."
        return target_r, target_c, "."
        
    #When pushing rocks
    if (0 <= target_r < n_rows) and (0 <= target_c < n_cols) and world[target_r][target_c] == "R":
        if (0 <= target_r + dr < n_rows) and (0 <= target_c + dc < n_cols) and world[target_r + dr][target_c + dc] in (".", "_", "~"):
            
            #Pushing rock to water
            if world[target_r + dr][target_c + dc] == "~":
                current_world[target_r + dr][target_c + dc] = "_"
                current_world[target_r][target_c] = rocks.pop((target_r, target_c))
                return target_r, target_c, current_world[target_r][target_c]

            #Pushing rock normally
            elif world[target_r + dr][target_c + dc] in (".", "_"):
                rocks[(target_r + dr, target_c + dc)] = current_world[target_r + dr][target_c + dc]
                current_world[target_r + dr][target_c + dc] = "R"
                current_world[target_r][target_c] = rocks.pop((target_r, target_c))
                return target_r, target_c, current_world[target_r][target_c]
        else:
            return r, c, current_world[r][c]  

    return r, c, current_world[r][c]
