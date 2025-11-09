# 🖐️ Welcome to LaroCraft! 🧑 🏕️ 🥾

## USER MANUAL 📖
### I. How to download and run the game ⬇️
0. ‼️ Ensure that you have Python installed on your device ‼️
1. To run LaroCraft, first download this repository on your device (Go to the green "Code" button on the top right, click on the arrow down, click download zip)
2. Extract the zip file
3. Go to your device's terminal 
    - Windows: Command Prompt / Powershell
    - MacOS: Terminal
    - Linux: Terminal / Terminal Emulator
4. Access the game folder through the terminal (Tutorial: https://www.youtube.com/watch?v=DsAdxr5yLxQ )
5. Run the command 'python3 -m Scripts.py' to launch the game with a base map
6. To access different Levels, add '-f Level(number).txt' to the previous command (Example: 'python3 -m Scripts.py -f Level3.txt)

### II. Objective: 🔍
Your objective in LaroCraft is to collect all mushrooms present in the map!

### III. Controls: 🎮
To move around, kindly enter any combination of the following movement characters:
- W/I: Move up
- D/L: Move right
- S:K: Move down
- A/J: Move left

You can enter either one character ('a' or 'i'), or a string of characters ('ddwwa' or 'jjiili')

To **PICKUP** an item, **enter 'P'** (your character must be on top of the item)

To **RESTART** a level, **enter '!'**

To **QUIT** the game, **enter 'Q'**


## ABOUT THE CODE 🤓
### I. File Organization 📂
    Game                        #GAME FOLDER !!
        __pycache__             #dont mind!
        Levels                  #Folder containing text files for Levels 1-11
            Level(1-11).txt
        Output.txt              #the output if moves are done in the terminal commmand
        Scripts.py              #MAIN GAME PROGRAM !!
        test_Scripts.py         #for pytests
    .gitignore                  #ignore!
### II. Algorithm
I. Interactive Mode (moves are not pre-inputted via the terminal command)
1. The Map 🗺️
- accesses the map for the chosen level (default map if no level is chosen)
- turns the map into a list of lists (DisplayBoard)
- 2 more copies of the board are created: RestartBoard (for restarting) and ToggleBoard? (?)

2. Laro 👤
- The player, Laro (L), is located
- Laro's inventory and mushroom counters are set to 0
- The player's win condition is asssessed

3. Main Loop (For Interactive Mode) 🔁
- The map/board is printed with the letters replaced with emojis
- The game asks for the player's input
- The board is updated accordingly, win conditions are checked to see if the game has ended or not
- if game is won, program ends, else the loop repeats
- if a player dies, program ends

II. Terminal Mode (pre-moves are inputted)
- In the terminal mode, instead of the user being asked for moves to update the map live, pre-moves are inputted and the output is the final state of the board.

### III. Important Game Functions 🤓
The algorithm was possible thanks to these functions/function blocks:

#### 1. Board Functions
- DisplayBoard: The board that is updated per move
- InitialBoard: The board that is not mutated; used for Restart() and used as a reference for movement and items
- ToggleBoard: The board of items that is updated when an item is picked up
#### 2. Player Functions
- PlayerInput: Asks for the action/s
- The Player Dictionary: Contains the players position, items, mushrooms, and win condition
#### 3. Movement Functions
- In charge of updating the players location and the board
- Space(): Restores/Updates the player's previous location using InitialBoard and ToggleBoard as a reference
#### 4. Game Mechanics Functions
- Restart(): Restores the map and player with InitalBoard and InitialPlayer
- Rocks and Water: If a rock is on top of a water block, the water block turns into paved tile
- Axe/Flamethrower: If you run into a tree, it checks if the player has an axe or a flamethrower to determine if tree/s can be cut/burned or not
- BurnTree: Burns all connected trees if player has a flamethrower
#### 5. Conditional Functions
- Win/Loss: Checks mushrooms obtained and if player is not on water


## UNIT TESTING 🤖
### I. Current Unit Tests
The following unit tests can be seen in the test_Scripts.py file:

**1. Structural Tests**

    Test 1: test_position_sets_correct_tile
    - checks if player (emoji) is properly placed in the coordinates

    Test 2: test_restart_resets_player_and_board
    - in the case of a restart, it checks if the player and the map are set to the inital player and map


**2. Movement Tests**

    Test 3: test_space_moves_player
    - checks if moving actual makes the character move

    Test 4: test_movement_into_mushroom_increases_count
    - checks if moving into a mushroom consumes it and adds to the counter

    Test 5: test_movement_into_water_triggers_loss
    - checks if water actually causes death

    Test 6: test_pickup_items
    - checks if an item can be picked up and properly used

**3. Utility Tests**

    Test 7: def test_burn_tree_removes_adjacent_trees
    - checks if the flamethrower burns all connected trees


We feel that these tests cover enough of the features of the game to ensure that the game works as intended. Board copying and printing is checked, Player printing and movemenet is checked, mushroom and item features are checked, flamethrower mechanics are checked, and win/loss conditions are checked even on edge cases. 

However, in the case that you would like to add more tests for the game, you may use the following format as a guide in creating them:

    def new_test(setup_boards):
        Player, InitialPlayer, DisplayBoard, InitialBoard, ToggleBoard = setup_boards
        ###
        #conditions and the like
        #blah blah blah
        #more test stuff!
        ###
        assert ... #place here what you want to check (blank == blank)

You can test your added case by running this command in your terminal:

    pytest -v test_file.py::new_test

## BONUS FEATURES 🔥😲
For our project, the following bonus features were added on top of the base game:
#### 1. Main Menu
#### 2. Exit function
#### 3. Leaderboard
#### 4. User Interface
#### 5. 2nd Character
