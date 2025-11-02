import Scripts

WaitTime = 1

Player = {
    "xPos": 2,
    "yPos": 2,
    "mushroom": 0,
    "char": "L",
    "axe": False,
    "flamethrower": False,
}

InitialPlayer = { 
    "xPos": 2,
    "yPos": 2,
    "mushroom": 0,
    "char": "L",
    "axe": False,
    "flamethrower": False,
}


DisplayBoard = [
    ["T", "T", "T", "T", "T", "T", "T"],
    ["T", ".", ".", ".", ".", ".", "T"],
    ["T", ".", ".", "R", ".", "+", "T"],
    ["T", ".", ".", "R", "R", ".", "T"],
    ["T", ".", "R", "+", ".", ".", "T"],
    ["T", ".", ".", ".", ".", ".", "T"],
    ["T", "T", "T", "T", "T", "T", "T"]
]

InitialBoard = [
    ["T", "T", "T", "T", "T", "T", "T"],
    ["T", ".", ".", ".", ".", ".", "T"],
    ["T", ".", ".", "R", ".", "+", "T"],
    ["T", ".", ".", "R", "R", ".", "T"],
    ["T", ".", "R", "+", ".", ".", "T"],
    ["T", ".", ".", ".", ".", ".", "T"],
    ["T", "T", "T", "T", "T", "T", "T"]
]

ToggleBoard = [
    ["T", "T", "T", "T", "T", "T", "T"],
    ["T", ".", ".", ".", ".", ".", "T"],
    ["T", ".", ".", "R", ".", "+", "T"],
    ["T", ".", ".", "R", "R", ".", "T"],
    ["T", ".", "R", "+", ".", ".", "T"],
    ["T", ".", ".", ".", ".", ".", "T"],
    ["T", "T", "T", "T", "T", "T", "T"]
]

while True:
    Scripts.clearConsole()
    Scripts.Position(DisplayBoard, Player)
    Scripts.printBoard(DisplayBoard)
    Scripts.PlayerInput(Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime)