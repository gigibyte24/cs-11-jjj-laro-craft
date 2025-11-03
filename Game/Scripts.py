import os
import time
import copy
from argparse import ArgumentParser

def main():
    parser = ArgumentParser()

    parser.add_argument('-f', '--file')
    parser.add_argument('-m', '--moves')
    parser.add_argument('-o', '--output')

    args = parser.parse_args()

    if args.file and args.moves and args.output:
        with open(args.file, encoding='utf-8') as f:
            stage_data = f.read()
        return stage_data, args.moves, args.output
    elif args.file:
        with open(args.file, encoding='utf-8') as f:
            stage_data = f.read()
        return stage_data, None, None
    else:
        return None, None, None
    

#----------------------Variables-----------------------#

data = main()
if data[0] != None:
    board = data[0].splitlines()
    row = 0
    col = 0
    RowConstuctor = []
    DisplayBoard = []
    WaitTime = 1

    Player = {
        "xPos": 0,
        "yPos": 0,
        "mushroom": 0,
        "win": 0,
        "char": "L",
        "axe": 0,
        "flamethrower": 0,
    }

    for x in board:
        for y in x:
            if y == "L":
                Player["xPos"] = col
                Player["yPos"] = row
            if y == "+":
                Player["win"] += 1
            RowConstuctor.append(y)
            col+= 1
        DisplayBoard.append(RowConstuctor)
        RowConstuctor = []
        row += 1
        col = 0

    InitialPlayer = copy.deepcopy(Player)
    InitialBoard = copy.deepcopy(DisplayBoard)
    ToggleBoard = copy.deepcopy(DisplayBoard)

else:
    WaitTime = 1

    Player = {
        "xPos": 2,
        "yPos": 2,
        "mushroom": 0,
        "win": 1,
        "char": "L",
        "axe": 0,
        "flamethrower": 0,
    }
    
    DisplayBoard = [
    ["T", "T", "T", "T", "T", "T", "T", "T", "T", "T"],
    ["T", ".", ".", ".", ".", ".", ".", ".", ".", "T"],
    ["T", ".", "L", ".", ".", ".", ".", "+", ".", "T"],
    ["T", ".", ".", ".", ".", ".", ".", ".", ".", "T"],
    ["T", "T", "T", "T", "T", "T", "T", "T", "T", "T"]
    ]

    InitialPlayer = copy.deepcopy(Player)
    InitialBoard = copy.deepcopy(DisplayBoard)
    ToggleBoard = copy.deepcopy(DisplayBoard)

#--------------Functions-------------------------#

def printBoard(Board):
    for count in Board:
        print(" ".join(count))

def clearConsole():
    os.system('cls')

def DenyMove(waitTime):
    print("Cannot move!!")
    time.sleep(waitTime)

def Position(Board, Player):
    Board[Player["yPos"]][Player["xPos"]] = Player["char"]

def Restart(Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard):
    Player.clear()
    Player.update(copy.deepcopy(InitialPlayer))
    DisplayBoard[:] = copy.deepcopy(InitialBoard)
    ToggleBoard[:] = copy.deepcopy(InitialBoard)

def Loss(Player, InitialPlayer, DisplayBoard, ToggleBoard, InitialBoard):
    clearConsole()
    Position(DisplayBoard, Player)
    printBoard(DisplayBoard)
    print("\nYou drowned! Game Over.")
    print("Press ! to Restart or Q to quit")
    print("\nMushrooms Collected:", Player["mushroom"], "out of", Player["win"])
    move = input("Enter move:").lower()

    if move == "!":
        Restart(Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard)
    elif move == "q":
        print("Goodbye")
        quit()
    else:
        clearConsole()
        printBoard(DisplayBoard)
        print("\nPlease Input a valid character")
        Loss(Player, InitialPlayer, DisplayBoard, ToggleBoard, InitialBoard)
        
def Win(Player, InitialPlayer, DisplayBoard, ToggleBoard, InitialBoard):
    clearConsole()
    Position(DisplayBoard, Player)
    printBoard(DisplayBoard)
    print("\nYou collected all mushrooms! You win.")
    print("Press ! to Restart or Q to quit")
    print("\nMushrooms Collected:", Player["mushroom"], "out of", Player["win"])
    move = input("Enter move:").lower()

    if move == "!":
        Restart(Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard)
    elif move == "q":
        print("Goodbye")
        quit()
    else:
        clearConsole()
        printBoard(DisplayBoard)
        print("\nPlease Input a valid character")
        Win(Player, InitialPlayer, DisplayBoard, ToggleBoard, InitialBoard)

def PlayerInput(Player, InitialPlayer, DisplayBoard, ToggleBoard, InitialBoard, WaitTime):
    print("\nPress W, A, S, D or I, J, K, L to move")
    print("Press ! to Restart or Q to quit")
    print("\nMushrooms Collected:", Player["mushroom"], "out of", Player["win"])

    if Player["axe"] == True:
        print("\nCurrent item held: Axe")
    elif Player["flamethrower"] == True:
        print("\nCurrent item: Flamethrower")
    else:
        print("\nCurrent item held: None")

    if not (Player["axe"] == False and Player["flamethrower"] == False):
        print("\nInventory Full")
    elif (InitialBoard[Player["yPos"]][Player["xPos"]] == "x") and (ToggleBoard[Player["yPos"]][Player["xPos"]] != "/"):
        print("\nEquippable Item on tile: Axe")
    elif (InitialBoard[Player["yPos"]][Player["xPos"]] == "*") and (ToggleBoard[Player["yPos"]][Player["xPos"]] != "/"):
        print("\nEquippable Item on tile: Flamethrower")
    else:
        print("\nEquippable Item on tile: None")

    moveset = input("Enter move:").lower()
    
    for move in moveset:
        if move not in ("w", "a", "s", "d", "!", "q", "p"):
            break
        try:
            if move == "w" or move == "i":
                movement(-1, 0, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime)

            if move == "a" or move == "j":
                movement(0, -1, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime)

            if move == "s" or move == "k":
                movement(1, 0, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime)

            if move == "d" or move == "l":
                movement(0, 1, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime)
        except IndexError:
            break

        if move == "p":
            if Player["axe"] == False and Player["flamethrower"] == False:
                if InitialBoard[Player["yPos"]][Player["xPos"]] == "x" and ToggleBoard[Player["yPos"]][Player["xPos"]] != "/":
                    ToggleBoard[Player["yPos"]][Player["xPos"]] = "/"
                    Player["axe"] += 1
                if InitialBoard[Player["yPos"]][Player["xPos"]] == "*" and ToggleBoard[Player["yPos"]][Player["xPos"]] != "/":
                    ToggleBoard[Player["yPos"]][Player["xPos"]] = "/"
                    Player["flamethrower"] += 1

        if move == "q":
            print("Goodbye")
            quit()

        if move == "!":
            Restart(Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard)

def BurnTree(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime):
    Space(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime)
    i, j = Player["yPos"], Player["xPos"]
    adjacent = ((0,1), (0, -1), (1,0), (-1, 0))
    def Burn(i, j):
        for adj in adjacent:
            new_i, new_j = i+adj[0], j+adj[1]
            if not (new_i < 0 or new_j < 0 or new_i >= len(DisplayBoard) or new_j >= len(DisplayBoard[0])):
                if DisplayBoard[new_i][new_j] == "T":
                    DisplayBoard[new_i][new_j] = "."
                    Burn(new_i, j+adj[1])
    Burn(i, j)


def Space(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime):
    Spacetiles = (".", "+", "T", "R", "L")
    if InitialBoard[Player["yPos"]][Player["xPos"]] in Spacetiles:
        DisplayBoard[Player["yPos"]][Player["xPos"]] = "."
        Player["yPos"] += yMoveVal
        Player["xPos"] += xMoveVal
    elif InitialBoard[Player["yPos"]][Player["xPos"]] == "~":
        DisplayBoard[Player["yPos"]][Player["xPos"]] = "-"
        Player["yPos"] += yMoveVal
        Player["xPos"] += xMoveVal
    elif InitialBoard[Player["yPos"]][Player["xPos"]] == "x":
        if ToggleBoard[Player["yPos"]][Player["xPos"]] == "/": 
            DisplayBoard[Player["yPos"]][Player["xPos"]] = "."
            Player["yPos"] += yMoveVal
            Player["xPos"] += xMoveVal
        else:
            DisplayBoard[Player["yPos"]][Player["xPos"]] = "x"
            Player["yPos"] += yMoveVal
            Player["xPos"] += xMoveVal
    elif InitialBoard[Player["yPos"]][Player["xPos"]] == "*":
        if ToggleBoard[Player["yPos"]][Player["xPos"]] == "/":
            DisplayBoard[Player["yPos"]][Player["xPos"]] = "."
            Player["yPos"] += yMoveVal
            Player["xPos"] += xMoveVal
        else:
            DisplayBoard[Player["yPos"]][Player["xPos"]] = "*"
            Player["yPos"] += yMoveVal
            Player["xPos"] += xMoveVal

    if (Player["yPos"] < 0):
        Player["yPos"] += 1
    if (Player["xPos"] < 0):
        Player["xPos"] += 1
    

def movement(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime):
    #------------------------spaces-------------------------------------------#
    SkipTiles = (".", "-", "x", "*")
    if DisplayBoard[Player["yPos"] + yMoveVal][Player["xPos"] + xMoveVal] in SkipTiles:
        Space(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime)

    #------------------------mushrooms-------------------------------------------#
    elif DisplayBoard[Player["yPos"] + yMoveVal][Player["xPos"] + xMoveVal] == "+":
        Player["mushroom"] += 1
        Space(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime)
        if Player["mushroom"] == Player["win"]:
            Win(Player, InitialPlayer, DisplayBoard, ToggleBoard, InitialBoard)

    #------------------------water-------------------------------------------#
    elif DisplayBoard[Player["yPos"] + yMoveVal][Player["xPos"] + xMoveVal] == "~":
        Space(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime)
        Loss(Player, InitialPlayer, DisplayBoard, ToggleBoard, InitialBoard)

    #------------------------rock-------------------------------------------#
    elif DisplayBoard[Player["yPos"] + yMoveVal][Player["xPos"] + xMoveVal] == "R":
        Avoid = ("+", "R", "x", "*", "T")
        if DisplayBoard[Player["yPos"] + (yMoveVal*2)][Player["xPos"] + (xMoveVal*2)] not in Avoid:
            if DisplayBoard[Player["yPos"] + (yMoveVal*2)][Player["xPos"] + (xMoveVal*2)] == "~":
                DisplayBoard[Player["yPos"] + (yMoveVal*2)][Player["xPos"] + (xMoveVal*2)] = "-"
                Space(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime)
            else:
                DisplayBoard[Player["yPos"] + (yMoveVal*2)][Player["xPos"] + (xMoveVal*2)] = "R"
                Space(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime)

    #------------------------Tree-------------------------------------------#
    elif DisplayBoard[Player["yPos"] + yMoveVal][Player["xPos"] + xMoveVal] == "T":
        if Player["axe"] == True:
            Space(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime)
            Player["axe"] -= 1
        if Player["flamethrower"] == True:
            BurnTree(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime)
            Player["flamethrower"] -= 1

while True:
    clearConsole()
    Position(DisplayBoard, Player)
    printBoard(DisplayBoard)
    PlayerInput(Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime)