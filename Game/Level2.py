import Scripts

waitTime = 1

Player = {
    "xPos": 5,
    "yPos": 6,
    "mushrooms": 0,
    "char": "L",
}


Board = [
    ["T", "T", "T", "T", "T", "T", "T", "T", "T", "T"],
    ["T", ".", ".", ".", ".", ".", ".", ".", ".", "T"],
    ["T", ".", "+", ".", ".", "R", "~", ".", ".", "T"],
    ["T", ".", "R", "R", ".", "R", "~", "~", "+", "T"],
    ["T", ".", "~", "~", ".", "R", "~", ".", ".", "T"],
    ["T", ".", ".", ".", ".", ".", ".", ".", ".", "T"],
    ["T", ".", ".", ".", ".", ".", ".", ".", ".", "T"],
    ["T", "T", "T", "T", "T", "T", "T", "T", "T", "T"]
]

InitialPlayer = { 
    "xPos": 5,
    "yPos": 6,
    "mushrooms": 0,
    "char": "L",
}

InitialBoard = [  
    ["T", "T", "T", "T", "T", "T", "T", "T", "T", "T"],
    ["T", ".", ".", ".", ".", ".", ".", ".", ".", "T"],
    ["T", ".", "+", ".", ".", "R", "~", ".", ".", "T"],
    ["T", ".", "R", "R", ".", "R", "~", "~", "+", "T"],
    ["T", ".", "~", "~", ".", "R", "~", ".", ".", "T"],
    ["T", ".", ".", ".", ".", ".", ".", ".", ".", "T"],
    ["T", ".", ".", ".", ".", ".", ".", ".", ".", "T"],
    ["T", "T", "T", "T", "T", "T", "T", "T", "T", "T"]
]

while True:
    Scripts.clearConsole()
    Scripts.Position(Board, Player)
    Scripts.printBoard(Board)
    Scripts.PlayerInput(Board, Player, waitTime, InitialPlayer, InitialBoard)