import pytest
import os
import sys
from shroom_raider import find_object, player_move, reset, clear_screen

"""Different world set ups for tests"""
@pytest.fixture
def basic_world():
    return [
        ["T", "T", "T", "T", "T",],
        ["T", ".", ".", ".", "T",],    
        ["T", ".", "L", ".", "T",],    
        ["T", ".", ".", ".", "T",],    
        ["T", "T", "T", "T", "T",],
    ]

@pytest.fixture
def default_world():
    return [
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

"""Reset() creates game_data, current_world, rocks for every test case"""
@pytest.fixture(autouse=True)
def global_variables():
    reset()
    yield

"""Testing find_object function"""

def test_find_laro(basic_world):
    r, c = find_object(basic_world, "L")
    assert r == 2
    assert c == 2
    assert basic_world[r][c] == "L"

def test_find_rock():
    world = [
        ["T", "T", "T", "T", "T",],
        ["T", ".", ".", ".", "T",],    
        ["T", ".", "R", ".", "T",],    
        ["T", ".", ".", ".", "T",],    
        ["T", "T", "T", "T", "T",],    
    ]
    """Since find_object returns a list of tuples like [(r1, c1), (r2, c2), ...] when it finds rock positions,
    we will take the first result (r, c) since it it the only result in the list in this world"""
    r, c = find_object(world, "R")[0]
    assert r == 2
    assert c == 2
    assert world[r][c] == "R"

def test_find_four_rocks():
    world = [
        ["T", "T", "T", "R", "T",],
        ["T", "R", ".", ".", "T",],    
        ["T", ".", ".", ".", "T",],    
        ["T", ".", ".", ".", "T",],    
        ["R", "T", "T", "T", "R",],    
    ]
    rocks = find_object(world, "R")
    assert len(rocks) == 4
    assert (1, 1) in rocks
    assert (4, 0) in rocks
    assert (4, 4) in rocks
    assert (0, 3) in rocks

def test_find_something_that_does_not_exist(default_world):
    symbols = ["H", "9", "b", "!", " ", "@", "♥"]
    for s in symbols:
        position = find_object(default_world, s)
        assert position is None

"""World without a player"""
def test_find_missing_player():
    world = [
        ["T", "T", "T"],
        ["T", ".", "T"],
        ["T", ".", "T"],
        ["T", "T", "T"]
    ]
    player_position = find_object(world, "L")
    assert player_position is None

# """World with multiple players""" <------------------------------------- Will fix either find_object function or this test since player position only returns the first instance of L
# def test_find_multiple_players():
#     world = [
#         ["T", "T", "T"],
#         ["T", "L", "T"],
#         ["T", "L", "T"],
#         ["T", "T", "T"]
#     ]
#     player_position = find_object(world, "L")
#     assert player_position is list or len(player_position) > 1

"""Empty world"""
def test_find_missing_player():
    world = []
    assert find_object(world, "L") == None
    assert find_object(world, "R") == []


"""Testing player_move function"""

"""Move to an empty tile to the right"""
def test_move_to_empty_tile(basic_world):
    world = [row.copy() for row in basic_world]
    new_r, new_c, new_tile = player_move((2, 2), (0, 1), world)
    assert new_r == 2
    assert new_c == 3
    assert new_tile == "."

"""Move to out of bounds"""
def test_move_to_oob(basic_world):
    world = [row.copy() for row in basic_world]

    """Move to out of bounds on top"""
    new_r, new_c, new_tile = player_move((0, 2), (-1, 0), world)
    assert new_r == 0
    assert new_c == 2

    """Move to out of bounds on left"""
    new_r, new_c, new_tile = player_move((2, 0), (0, -1), world)
    assert new_r == 2
    assert new_c == 0

    """Move to out of bounds on right"""
    new_r, new_c, new_tile = player_move((2, 4), (0, 1), world)
    assert new_r == 2
    assert new_c == 4

    """Move to out of bounds on bottom"""
    new_r, new_c, new_tile = player_move((4, 2), (1, 0), world)
    assert new_r == 4
    assert new_c == 2

"""Move to tree tile"""
def test_move_to_tree_tile(basic_world):
    world = [row.copy() for row in basic_world]
    new_r, new_c, new_tile = player_move((3, 3), (0, 1), world)
    """Laro does not move and stays on the empty tile"""
    assert new_r == 3
    assert new_c == 3
    assert new_tile == "."

"""Move in a 1x1 world"""
def test_move_in_single_tile_world():
    world = [
        ["L"] 
    ]
    assert player_move((0, 0), (-1, 0), world) == (0, 0, "L")
    assert player_move((0, 0), (1, 0), world) == (0, 0, "L")
    assert player_move((0, 0), (0, -1), world) == (0, 0, "L")
    assert player_move((0, 0), (0, 1), world) == (0, 0, "L")

"""Testing player interactions with world"""

"""Burn connected trees"""
def test_burn_connected():
    from shroom_raider import game_data
    world = [
        ["T", "T", "T", "T", "T",],
        ["T", ".", ".", ".", "T",],    
        ["T", ".", "L", "T", "T",],    
        ["T", ".", ".", ".", "T",],    
        ["T", "T", "T", "T", "T",],
    ]
    game_data["inventory"] = "*"
    new_r, new_c, new_tile = player_move((2, 2), (0, 1), world)
    assert new_r == 2
    assert new_c == 3
    assert new_tile == "."
    # Check if target tree and connected trees were burnt
    burnt_trees = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                   (1, 0), (1, 4),
                   (2, 0), (2, 3), (2, 4),
                   (3, 0), (3, 4),
                   (4, 0), (4, 1), (4, 2), (4, 3), (4, 4)]
    for r, c in burnt_trees:
        assert world[r][c] == "."


"""Don't burn unconnected trees"""
def test_do_not_burn_unconnected():
    from shroom_raider import game_data
    world = [
        ["T", ".", "T"],
        [".", "L", "T"],
        ["T", ".", "T"],
        [".", "T", "T"],
    ]
    game_data["inventory"] = "*"
    new_r, new_c, new_tile = player_move((1, 1), (0, 1), world)
    assert new_r == 1
    assert new_c == 2
    assert new_tile == "."

    unburnt_trees = [(0, 0), (2, 0)]
    for r, c in unburnt_trees:
        assert world[r][c] == "T"
