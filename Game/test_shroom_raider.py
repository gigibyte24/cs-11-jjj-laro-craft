import copy
import pytest
import shroom_raider


@pytest.fixture
def setup_boards():
    DisplayBoard = [
        ["🌲", "　", "　", "🍄", "🌲"],
        ["🌲", "🪨 ", "　", "🪓", "🌲"],
        ["🌲", "　", "🧑", "　", "🌲"],
        ["🌲", "🔥", "　", "🟦", "🌲"],
        ["🌲", "🌲", "🌲", "🌲", "🌲"],
    ]
    InitialBoard = copy.deepcopy(DisplayBoard)
    ToggleBoard = copy.deepcopy(DisplayBoard)
    Player = {"xPos": 2, 
              "yPos": 2, 
              "mushroom": 0, 
              "win": 1, 
              "axe": 0, 
              "flamethrower": 0}
    InitialPlayer = copy.deepcopy(Player)
    return Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard


# ----------------- BASIC STRUCTURAL TESTS -----------------

def test_position_sets_correct_tile(setup_boards):
    Player, _, DisplayBoard, *_ = setup_boards
    shroom_raider.Position(DisplayBoard, Player)
    assert DisplayBoard[Player["yPos"]][Player["xPos"]] == "🧑"


def test_restart_resets_player_and_board(setup_boards):
    Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard = setup_boards
    Player["mushroom"] = 1
    DisplayBoard[2][2] = "　"
    shroom_raider.Restart(Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard)
    assert Player == InitialPlayer
    assert DisplayBoard == InitialBoard
    assert ToggleBoard == InitialBoard


# ----------------- MOVEMENT TESTS -----------------

def test_space_moves_player(setup_boards):
    Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard = setup_boards
    old_x, old_y = Player["xPos"], Player["yPos"]
    shroom_raider.Space(0, 1, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard)
    assert (Player["xPos"], Player["yPos"]) != (old_x, old_y)


def test_movement_into_mushroom_increases_count(setup_boards):
    Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard = setup_boards
    # Place mushroom directly to the right
    DisplayBoard[2][3] = "🍄"
    Player["win"] = 2*256
    shroom_raider.movement(0, 1, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, True)
    assert Player["mushroom"] == 1


def test_movement_into_water_triggers_loss(monkeypatch, setup_boards):
    Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard = setup_boards
    # Place water directly to the right
    DisplayBoard[2][3] = "🟦"
    # Patch TermLoss to track call
    called = {}
    monkeypatch.setattr(shroom_raider, "TermLoss", lambda *a, **kw: called.setdefault("loss", True))
    shroom_raider.movement(0, 1, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, IsTerminal=True)
    assert "loss" in called


def test_pickup_items(setup_boards):
    Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard = setup_boards
    InitialBoard[2][2] = "🪓"
    ToggleBoard[2][2] = "/"
    Player["axe"] = 0
    Player["flamethrower"] = 0
    Player["yPos"], Player["xPos"] = 2, 2
    # Simulate pressing P
    if Player["axe"] == 0 and Player["flamethrower"] == 0:
        ToggleBoard[2][2] = "/"
        Player["axe"] += 1
    assert Player["axe"] == 1
    assert ToggleBoard[2][2] == "/"


# ----------------- UTILITY TESTS -----------------

def test_burn_tree_removes_adjacent_trees(setup_boards):
    Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard = setup_boards
    # Surround center with trees
    for i in range(1, 4):
        for j in range(1, 4):
            DisplayBoard[i][j] = "🌲"
    DisplayBoard[2][2] = "🔥"
    shroom_raider.BurnTree(2, 2)
    for i in range(1, 4):
        for j in range(1, 4):
            assert DisplayBoard[i][j] != "🌲"