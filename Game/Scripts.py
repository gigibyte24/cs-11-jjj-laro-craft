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

def Restart(InitialBoard, Board, InitialPlayer, Player):
    Board[:] = copy.deepcopy(InitialBoard)
    Player.clear()
    Player.update(copy.deepcopy(InitialPlayer))

def PlayerInput(Board, Player, waitTime, InitialPlayer, InitialBoard):
    print("\nPress W, A, S, D or I, J, K, L to move")
    print("Press ! to Restart and Q to quit")
    print("\nCurrent Mushrooms: ", Player["mushrooms"])
    moveset = input("Enter move:")
    for move in moveset: 
        if move.lower() == "w" or move.lower() == "i":
            if Board[Player["yPos"] - 1][Player["xPos"]] == ".":
                if InitialBoard[Player["yPos"]][Player["xPos"]] == "+":
                    Board[Player["yPos"]][Player["xPos"]] = "."
                    Player["yPos"] -= 1
                else:
                    Board[Player["yPos"]][Player["xPos"]] = InitialBoard[Player["yPos"]][Player["xPos"]]
                    Player["yPos"] -= 1
            elif Board[Player["yPos"] - 1][Player["xPos"]] == "+":
                Player["mushrooms"] += 1
                Board[Player["yPos"]][Player["xPos"]] = InitialBoard[Player["yPos"]][Player["xPos"]]
                Player["yPos"] -= 1
            elif Board[Player["yPos"] - 1][Player["xPos"]] == "~":
                Board[Player["yPos"]][Player["xPos"]] = InitialBoard[Player["yPos"]][Player["xPos"]]
                Player["yPos"] -= 1
                Position(Board, Player)
                clearConsole()
                printBoard(Board)
                print("Game Over...")
                quit()
            else:
                DenyMove(waitTime)
            
        if move.lower() == "a" or move.lower() == "j":
            if Board[Player["yPos"]][Player["xPos"] - 1] == ".":
                if InitialBoard[Player["yPos"]][Player["xPos"]] == "+":
                    Board[Player["yPos"]][Player["xPos"]] = "."
                    Player["xPos"] -= 1
                else:
                    Board[Player["yPos"]][Player["xPos"]] = InitialBoard[Player["yPos"]][Player["xPos"]]
                    Player["xPos"] -= 1
            elif Board[Player["yPos"]][Player["xPos"] - 1] == "+":
                Player["mushrooms"] += 1
                Board[Player["yPos"]][Player["xPos"]] = "."
                Player["xPos"] -= 1
            elif Board[Player["yPos"]][Player["xPos"] - 1] == "~":
                Board[Player["yPos"]][Player["xPos"]] = "."
                Player["xPos"] -= 1
                Position(Board, Player)
                clearConsole()
                printBoard(Board)
                print("Game Over...")
                quit()
            else:
                DenyMove(waitTime)

        if move.lower() == "s" or move.lower() == "k":
            if Board[Player["yPos"] + 1][Player["xPos"]] == ".":
                if InitialBoard[Player["yPos"]][Player["xPos"]] == "+":
                    Board[Player["yPos"]][Player["xPos"]] = "."
                    Player["yPos"] += 1
                else:
                    Board[Player["yPos"]][Player["xPos"]] = InitialBoard[Player["yPos"]][Player["xPos"]]
                    Player["yPos"] += 1
            elif Board[Player["yPos"] + 1][Player["xPos"]] == "+":
                Player["mushrooms"] += 1
                Board[Player["yPos"]][Player["xPos"]] = "."
                Player["yPos"] += 1
            elif Board[Player["yPos"] + 1][Player["xPos"]] == "~":
                Board[Player["yPos"]][Player["xPos"]] = "."
                Player["yPos"] += 1
                Position(Board, Player)
                clearConsole()
                printBoard(Board)
                print("Game Over...")
                quit()
            else:
                DenyMove(waitTime)
                
        if move.lower() == "d" or move.lower() == "l":
            if Board[Player["yPos"]][Player["xPos"] + 1] == ".":
                if InitialBoard[Player["yPos"]][Player["xPos"]] == "+":
                    Board[Player["yPos"]][Player["xPos"]] = "."
                    Player["xPos"] += 1
                else:
                    Board[Player["yPos"]][Player["xPos"]] = InitialBoard[Player["yPos"]][Player["xPos"]]
                    Player["xPos"] += 1
                Board[Player["yPos"]][Player["xPos"]] = "."
                Player["xPos"] += 1
            elif Board[Player["yPos"]][Player["xPos"] + 1] == "+":
                Player["mushrooms"] += 1
                Board[Player["yPos"]][Player["xPos"]] = "."
                Player["xPos"] += 1
            elif Board[Player["yPos"]][Player["xPos"] + 1] == "~":
                Board[Player["yPos"]][Player["xPos"]] = "."
                Player["xPos"] += 1
                Position(Board, Player)
                clearConsole()
                printBoard(Board)
                print("Game Over...")
                quit()
            else:
                DenyMove(waitTime)

        if move == "!":
            Restart(InitialBoard, Board, InitialPlayer, Player)
            clearConsole()
            Position(Board, Player)
            printBoard(Board)
            continue

        if move.lower() == "q":
            print("Goodbye")
            quit()