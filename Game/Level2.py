import Scripts

waitTime = 1

Player = {
    "xPos": 2,
    "yPos": 2,
    "mushrooms": 0,
    "char": "L",
}


Board = [
    ["T", "T", "T", "T", "T", "T", "T", "T", "T", "T"],
    ["T", ".", ".", ".", ".", ".", ".", ".", ".", "T"],
    ["T", ".", ".", "+", "+", "~", "~", "~", "+", "T"],
    ["T", ".", ".", ".", ".", ".", ".", ".", ".", "T"],
    ["T", "T", "T", "T", "T", "T", "T", "T", "T", "T"]
]

Initial = ([
    ["T", "T", "T", "T", "T", "T", "T", "T", "T", "T"],
    ["T", ".", ".", ".", ".", ".", ".", ".", ".", "T"],
    ["T", ".", ".", ".", ".", ".", ".", ".", ".", "T"],
    ["T", ".", ".", ".", ".", ".", ".", ".", ".", "T"],
    ["T", "T", "T", "T", "T", "T", "T", "T", "T", "T"]
], Player["xPos"], Player["yPos"])


while True:
    Scripts.Position(Board, Player)
    Scripts.printBoard(Board)
    Scripts.PlayerInput(Board, Player, waitTime, Initial)
    Scripts.clearConsole()