import os
import time
import copy

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
    print("\nYou drowned! Game Over.")
    print("Press ! to Restart or Q to quit")
    print("\nCurrent Mushrooms: ", Player["mushroom"])
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

def PlayerInput(Player, InitialPlayer, DisplayBoard, ToggleBoard, InitialBoard, WaitTime):
    print("\nPress W, A, S, D or I, J, K, L to move")
    print("Press ! to Restart or Q to quit")
    print("\nCurrent Mushrooms: ", Player["mushroom"])
    if Player["axe"] == True:
        print("\nCurrent item: Axe")
    elif Player["flamethrower"] == True:
        print("\nCurrent item: Flamethrower")
    else:
        print("\nCurrent item: None")
    moveset = input("Enter move:").lower()
    
    for move in moveset:
        if move not in ("w", "a", "s", "d", "!", "q", "p"):
            break
        if move == "w" or move == "i":
            movement(-1, 0, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime)

        if move == "a" or move == "j":
            movement(0, -1, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime)

        if move == "s" or move == "k":
            movement(1, 0, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime)

        if move == "d" or move == "l":
            movement(0, 1, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime)

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

def Water(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard):
    Player["yPos"] += yMoveVal
    Player["xPos"] += xMoveVal
    clearConsole()
    Position(DisplayBoard, Player)
    printBoard(DisplayBoard)
    Loss(Player, InitialPlayer, DisplayBoard, ToggleBoard, InitialBoard)

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
    Spacetiles = (".", "+", "T", "R")
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

def movement(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime):
    
#------------------------spaces-------------------------------------------#
    if DisplayBoard[Player["yPos"] + yMoveVal][Player["xPos"] + xMoveVal] == ".":
        Space(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime)

#------------------------mushrooms-------------------------------------------#
    elif DisplayBoard[Player["yPos"] + yMoveVal][Player["xPos"] + xMoveVal] == "+":
        Spacetiles = (".", "+", "T", "R")
        if InitialBoard[Player["yPos"]][Player["xPos"]] in Spacetiles:
            DisplayBoard[Player["yPos"]][Player["xPos"]] = "."
            Player["mushroom"] += 1
            Player["yPos"] += yMoveVal
            Player["xPos"] += xMoveVal
        elif InitialBoard[Player["yPos"]][Player["xPos"]] == "~":
            DisplayBoard[Player["yPos"]][Player["xPos"]] = "-"
            Player["mushroom"] += 1
            Player["yPos"] += yMoveVal
            Player["xPos"] += xMoveVal
        elif InitialBoard[Player["yPos"]][Player["xPos"]] == "x":
            if ToggleBoard[Player["yPos"]][Player["xPos"]] == "/":
                DisplayBoard[Player["yPos"]][Player["xPos"]] = "."
                Player["mushroom"] += 1
                Player["yPos"] += yMoveVal
                Player["xPos"] += xMoveVal
            else:
                DisplayBoard[Player["yPos"]][Player["xPos"]] = "x"
                Player["mushroom"] += 1
                Player["yPos"] += yMoveVal
                Player["xPos"] += xMoveVal
        elif InitialBoard[Player["yPos"]][Player["xPos"]] == "*":
            if ToggleBoard[Player["yPos"]][Player["xPos"]] == "/":
                DisplayBoard[Player["yPos"]][Player["xPos"]] = "."
                Player["mushroom"] += 1
                Player["yPos"] += yMoveVal
                Player["xPos"] += xMoveVal
            else:
                DisplayBoard[Player["yPos"]][Player["xPos"]] = "*"
                Player["mushroom"] += 1
                Player["yPos"] += yMoveVal
                Player["xPos"] += xMoveVal

#------------------------water-------------------------------------------#
    elif DisplayBoard[Player["yPos"] + yMoveVal][Player["xPos"] + xMoveVal] == "~":
        Spacetiles = (".", "+", "T", "R")
        if InitialBoard[Player["yPos"]][Player["xPos"]] in Spacetiles:
            DisplayBoard[Player["yPos"]][Player["xPos"]] = "."
            Water(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard)
        elif InitialBoard[Player["yPos"]][Player["xPos"]] == "~":
            DisplayBoard[Player["yPos"]][Player["xPos"]] = "-"
            Water(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard)
        elif InitialBoard[Player["yPos"]][Player["xPos"]] == "x":
            if ToggleBoard[Player["yPos"]][Player["xPos"]] == "/":
                DisplayBoard[Player["yPos"]][Player["xPos"]] = "."
                Water(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard)
            else:
                DisplayBoard[Player["yPos"]][Player["xPos"]] = "x"
                Water(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard)
        elif InitialBoard[Player["yPos"]][Player["xPos"]] == "*":
            if ToggleBoard[Player["yPos"]][Player["xPos"]] == "/":
                DisplayBoard[Player["yPos"]][Player["xPos"]] = "."
                Water(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard)
            else:
                DisplayBoard[Player["yPos"]][Player["xPos"]] = "*"
                Water(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard)

#------------------------rock-------------------------------------------#
    elif DisplayBoard[Player["yPos"] + yMoveVal][Player["xPos"] + xMoveVal] == "R":
        Avoid = ("+", "R", "A", "F", "T")
        if DisplayBoard[Player["yPos"] + (yMoveVal*2)][Player["xPos"] + (xMoveVal*2)] not in Avoid:
            if DisplayBoard[Player["yPos"] + (yMoveVal*2)][Player["xPos"] + (xMoveVal*2)] == "~":
                DisplayBoard[Player["yPos"] + (yMoveVal*2)][Player["xPos"] + (xMoveVal*2)] = "-"
                Space(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime)
            else:
                DisplayBoard[Player["yPos"] + (yMoveVal*2)][Player["xPos"] + (xMoveVal*2)] = "R"
                Space(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime)

#------------------------Pavement-------------------------------------------#
    elif DisplayBoard[Player["yPos"] + yMoveVal][Player["xPos"] + xMoveVal] == "-":
        Space(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime)

#------------------------Axe-------------------------------------------#
    elif DisplayBoard[Player["yPos"] + yMoveVal][Player["xPos"] + xMoveVal] == "x":
        Space(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime)

#------------------------Flamethrower-------------------------------------------#
    elif DisplayBoard[Player["yPos"] + yMoveVal][Player["xPos"] + xMoveVal] == "*":
        Space(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime)

#------------------------Tree-------------------------------------------#
    elif DisplayBoard[Player["yPos"] + yMoveVal][Player["xPos"] + xMoveVal] == "T":
        if Player["axe"] == True:
            Space(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime)
            Player["axe"] -= 1
        if Player["flamethrower"] == True:
            BurnTree(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, WaitTime)
            Player["flamethrower"] -= 1