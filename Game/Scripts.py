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
    board = data[0][2:].splitlines()
    row = 0
    col = 0
    RowConstuctor = []
    DisplayBoard = []

    Player = {
        "xPos": 0,
        "yPos": 0,
        "mushroom": 0,
        "win": 0,
        "axe": 0,
        "flamethrower": 0,
    }

    for x in board:
        col = 0
        for y in x:
            if y == "L":
                Player["xPos"] = col
                Player["yPos"] = row
                RowConstuctor.append("🧑")
            if y == "+":
                Player["win"] += 1
                RowConstuctor.append("🍄")
            if y == ".":
                RowConstuctor.append("　")
            if y == "T":
                RowConstuctor.append("🌲")
            if y == "R":
                RowConstuctor.append("🪨 ")
            if y == "~":
                RowConstuctor.append("🟦")
            if y == "-":
                RowConstuctor.append("⬜")
            if y == "x":
                RowConstuctor.append("🪓")
            if y == "*":
                RowConstuctor.append("🔥")
            col+= 1
        DisplayBoard.append(RowConstuctor)
        RowConstuctor = []
        row += 1
        

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
        "axe": 0,
        "flamethrower": 0
    }
    
    DisplayBoard = [
    ["🌲", "🌲", "🌲", "🌲", "🌲", "🌲", "🌲", "🌲", "🌲", "🌲"],
    ["🌲", "　", "　", "　", "　", "　", "　", "　", "　", "🌲"],
    ["🌲", "　", "🧑", "　", "　", "　", "　", "🍄", "　", "🌲"],
    ["🌲", "　", "　", "　", "　", "　", "　", "　", "　", "🌲"],
    ["🌲", "🌲", "🌲", "🌲", "🌲", "🌲", "🌲", "🌲", "🌲", "🌲"]
    ]

    InitialPlayer = copy.deepcopy(Player)
    InitialBoard = copy.deepcopy(DisplayBoard)
    ToggleBoard = copy.deepcopy(DisplayBoard)

#--------------Functions-------------------------#

def printBoard(Board):
    for line in Board:
        print(" ".join(line))

def clearConsole():
    os.system('cls')

def Position(Board, Player):
    Board[Player["yPos"]][Player["xPos"]] = "🧑"

def Restart(Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard):
    Player.clear()
    Player.update(copy.deepcopy(InitialPlayer))
    DisplayBoard[:] = copy.deepcopy(InitialBoard)
    ToggleBoard[:] = copy.deepcopy(InitialBoard)

def Win(Player, DisplayBoard):
    clearConsole()
    Position(DisplayBoard, Player)
    printBoard(DisplayBoard)
    print("\nYou collected all mushrooms! You win.")
    print("Press ! to Restart or Q to quit")
    print("\nMushrooms Collected:", Player["mushroom"], "out of", Player["win"])
    quit()

def Loss(Player, DisplayBoard):
    clearConsole()
    Position(DisplayBoard, Player)
    printBoard(DisplayBoard)
    print("\nYou drowned! Game Over.")
    print("Press ! to Restart or Q to quit")
    print("\nMushrooms Collected:", Player["mushroom"], "out of", Player["win"])
    quit()

def TermWin(Player, DisplayBoard):
    Position(DisplayBoard, Player)
    TermPrint(DisplayBoard, "Clear")
    quit()

def TermLoss(Player, DisplayBoard):
    Position(DisplayBoard, Player)
    TermPrint(DisplayBoard, "No Clear")
    quit()

def NoMoves(Player, DisplayBoard):
    Position(DisplayBoard, Player)
    TermPrint(DisplayBoard, "No Clear")
    quit()

def TermPrint(DisplayBoard, Cleared):
    RowConstuctor = []
    with open("Output.txt", "w", encoding='utf-8') as file:
        row = row
        col = col
        file.write(Cleared)
        file.write("\nr = " + str(row) + "; c = " + str(col))
        for x in DisplayBoard:
            for y in x:
                if y == "🧑":
                    RowConstuctor.append("L")
                if y == "🍄":
                    RowConstuctor.append("+")
                if y == "　":
                    RowConstuctor.append(".")
                if y == "🌲":
                    RowConstuctor.append("T")
                if y == "🪨 ":
                    RowConstuctor.append("R")
                if y == "🟦":
                    RowConstuctor.append("~")
                if y == "⬜":
                    RowConstuctor.append("-")
                if y == "🪓":
                    RowConstuctor.append("x")
                if y == "🔥":
                    RowConstuctor.append("*")
            file.write("\n" + "".join(RowConstuctor))
            RowConstuctor = []


def PlayerInput(Player, InitialPlayer, DisplayBoard, ToggleBoard, InitialBoard):
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
    elif (InitialBoard[Player["yPos"]][Player["xPos"]] == "🪓") and (ToggleBoard[Player["yPos"]][Player["xPos"]] != "/"):
        print("\nEquippable Item on tile: Axe")
    elif (InitialBoard[Player["yPos"]][Player["xPos"]] == "🔥") and (ToggleBoard[Player["yPos"]][Player["xPos"]] != "/"):
        print("\nEquippable Item on tile: Flamethrower")
    else:
        print("\nEquippable Item on tile: None")

    moveset = input("Enter move:").lower()
    
    for move in moveset:
        if move not in ("w", "a", "s", "d", "!", "q", "p"):
            break
        try:
            if move == "w" or move == "i":
                movement(-1, 0, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, False)

            if move == "a" or move == "j":
                movement(0, -1, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, False)

            if move == "s" or move == "k":
                movement(1, 0, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, False)

            if move == "d" or move == "l":
                movement(0, 1, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, False)
        except IndexError:
            break

        if move == "p":
            if Player["axe"] == False and Player["flamethrower"] == False:
                if InitialBoard[Player["yPos"]][Player["xPos"]] == "🪓" and ToggleBoard[Player["yPos"]][Player["xPos"]] != "/":
                    ToggleBoard[Player["yPos"]][Player["xPos"]] = "/"
                    Player["axe"] += 1
                if InitialBoard[Player["yPos"]][Player["xPos"]] == "🔥" and ToggleBoard[Player["yPos"]][Player["xPos"]] != "/":
                    ToggleBoard[Player["yPos"]][Player["xPos"]] = "/"
                    Player["flamethrower"] += 1

        if move == "q":
            print("Goodbye")
            quit()

        if move == "!":
            Restart(Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard)

def TerminalInput(Player, InitialPlayer, DisplayBoard, ToggleBoard, InitialBoard):
    moveset = data[1]
    
    for move in moveset:
        if move not in ("w", "a", "s", "d", "!", "q", "p"):
            break
        try:
            if move == "w" or move == "i":
                movement(-1, 0, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, True)

            if move == "a" or move == "j":
                movement(0, -1, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, True)

            if move == "s" or move == "k":
                movement(1, 0, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, True)

            if move == "d" or move == "l":
                movement(0, 1, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, True)
            Position(DisplayBoard, Player)
        except IndexError:
            break

        if move == "p":
            if Player["axe"] == False and Player["flamethrower"] == False:
                if InitialBoard[Player["yPos"]][Player["xPos"]] == "🪓" and ToggleBoard[Player["yPos"]][Player["xPos"]] != "/":
                    ToggleBoard[Player["yPos"]][Player["xPos"]] = "/"
                    Player["axe"] += 1
                if InitialBoard[Player["yPos"]][Player["xPos"]] == "🔥" and ToggleBoard[Player["yPos"]][Player["xPos"]] != "/":
                    ToggleBoard[Player["yPos"]][Player["xPos"]] = "/"
                    Player["flamethrower"] += 1

        if move == "q":
            print("Goodbye")
            quit()

        if move == "!":
            Restart(Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard)

def TerminalInput(Player, InitialPlayer, DisplayBoard, ToggleBoard, InitialBoard):
    moveset = data[1]
    
    for move in moveset:
        if move not in ("w", "a", "s", "d", "!", "q", "p"):
            break
        try:
            if move == "w" or move == "i":
                movement(-1, 0, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, True)

            if move == "a" or move == "j":
                movement(0, -1, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, True)

            if move == "s" or move == "k":
                movement(1, 0, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, True)

            if move == "d" or move == "l":
                movement(0, 1, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, True)
            Position(DisplayBoard, Player)
        except IndexError:
            break

        if move == "p":
            if Player["axe"] == False and Player["flamethrower"] == False:
                if InitialBoard[Player["yPos"]][Player["xPos"]] == "🪓" and ToggleBoard[Player["yPos"]][Player["xPos"]] != "/":
                    ToggleBoard[Player["yPos"]][Player["xPos"]] = "/"
                    Player["axe"] += 1
                if InitialBoard[Player["yPos"]][Player["xPos"]] == "🔥" and ToggleBoard[Player["yPos"]][Player["xPos"]] != "/":
                    ToggleBoard[Player["yPos"]][Player["xPos"]] = "/"
                    Player["flamethrower"] += 1

        if move == "q":
            print("Goodbye")
            quit()

        if move == "!":
            Restart(Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard)

    NoMoves(Player, DisplayBoard)


def BurnTree(i, j):
    adjacent = ((0,1), (0, -1), (1,0), (-1, 0))
    for adj in adjacent:
        new_i, new_j = i+adj[0], j+adj[1]
        if not (new_i < 0 or new_j < 0 or new_i >= len(DisplayBoard) or new_j >= len(DisplayBoard[0])):
            if DisplayBoard[new_i][new_j] == "🌲":
                DisplayBoard[new_i][new_j] = "　"
                BurnTree(i+adj[0], j+adj[1])

def Space(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard):
    Spacetiles = ("　", "🍄", "🌲", "🪨 ", "🧑")
    if InitialBoard[Player["yPos"]][Player["xPos"]] in Spacetiles:
        DisplayBoard[Player["yPos"]][Player["xPos"]] = "　"
         
    elif InitialBoard[Player["yPos"]][Player["xPos"]] == "🟦":
        DisplayBoard[Player["yPos"]][Player["xPos"]] = "⬜"
         
    elif InitialBoard[Player["yPos"]][Player["xPos"]] == "🪓":
        if ToggleBoard[Player["yPos"]][Player["xPos"]] == "/": 
            DisplayBoard[Player["yPos"]][Player["xPos"]] = "　"
        else:
            DisplayBoard[Player["yPos"]][Player["xPos"]] = "🪓"
             
    elif InitialBoard[Player["yPos"]][Player["xPos"]] == "🔥":
        if ToggleBoard[Player["yPos"]][Player["xPos"]] == "/":
            DisplayBoard[Player["yPos"]][Player["xPos"]] = "　"
        else:
            DisplayBoard[Player["yPos"]][Player["xPos"]] = "🔥"
             
    Player["yPos"] += yMoveVal
    Player["xPos"] += xMoveVal

    if (Player["yPos"] < 0):
        Player["yPos"] += 1
    if (Player["xPos"] < 0):
        Player["xPos"] += 1
    

def movement(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard, IsTerminal):
    #------------------------spaces-------------------------------------------#
    SkipTiles = ("　", "⬜", "🪓", "🔥")
    if DisplayBoard[Player["yPos"] + yMoveVal][Player["xPos"] + xMoveVal] in SkipTiles:
        Space(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard)

    #------------------------mushrooms-------------------------------------------#
    elif DisplayBoard[Player["yPos"] + yMoveVal][Player["xPos"] + xMoveVal] == "🍄":
        Player["mushroom"] += 1
        Space(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard)
        if Player["mushroom"] == Player["win"]:
            if IsTerminal == True:
                TermWin(Player, DisplayBoard)
            else:
                Win(Player, DisplayBoard)

    #------------------------water-------------------------------------------#
    elif DisplayBoard[Player["yPos"] + yMoveVal][Player["xPos"] + xMoveVal] == "🟦":
        Space(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard)
        if IsTerminal == True:
                TermLoss(Player, DisplayBoard)
        else:
            Loss(Player, DisplayBoard)

    #------------------------rock-------------------------------------------#
    elif DisplayBoard[Player["yPos"] + yMoveVal][Player["xPos"] + xMoveVal] == "🪨 ":
        Avoid = ("🍄", "🪨 ", "🪓", "🔥", "🌲")
        if DisplayBoard[Player["yPos"] + (yMoveVal*2)][Player["xPos"] + (xMoveVal*2)] not in Avoid:
            if DisplayBoard[Player["yPos"] + (yMoveVal*2)][Player["xPos"] + (xMoveVal*2)] == "🟦":
                DisplayBoard[Player["yPos"] + (yMoveVal*2)][Player["xPos"] + (xMoveVal*2)] = "⬜"
                Space(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard)
            else:
                DisplayBoard[Player["yPos"] + (yMoveVal*2)][Player["xPos"] + (xMoveVal*2)] = "🪨 "
                Space(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard)

    #------------------------Tree-------------------------------------------#
    elif DisplayBoard[Player["yPos"] + yMoveVal][Player["xPos"] + xMoveVal] == "🌲":
        if Player["axe"] == True:
            Space(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard)
            Player["axe"] -= 1
        if Player["flamethrower"] == True:
            i, j = Player["yPos"], Player["xPos"]
            BurnTree(i, j)
            Space(yMoveVal, xMoveVal, Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard)
            Player["flamethrower"] -= 1

if __name__ == "__main__":
    while not data[1]:
        clearConsole()
        Position(DisplayBoard, Player)
        printBoard(DisplayBoard)
        PlayerInput(Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard)

    while data[1]:
        TerminalInput(Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard)