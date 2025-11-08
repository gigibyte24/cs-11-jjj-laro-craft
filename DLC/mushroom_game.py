import os
import copy
import json
from pathlib import Path
from datetime import datetime
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button, Label, Header, Footer, Input
from textual.containers import Container, Vertical, Horizontal, Grid, Center
from textual.binding import Binding
from rich.text import Text
from rich.panel import Panel
from rich.table import Table


class LeaderboardManager:
    """Manages the leaderboard system"""
    def __init__(self, leaderboard_file="leaderboard/leaderboard.json"):
        self.leaderboard_file = Path(leaderboard_file)
        self.leaderboard_file.parent.mkdir(exist_ok=True)
        self.load_leaderboard()
    
    def load_leaderboard(self):
        """Load leaderboard from file"""
        if self.leaderboard_file.exists():
            with open(self.leaderboard_file, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {}
    
    def save_leaderboard(self):
        """Save leaderboard to file"""
        with open(self.leaderboard_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add_score(self, username, level_name, moves):
        """Add a score to the leaderboard"""
        if level_name not in self.data:
            self.data[level_name] = []
        
        entry = {
            "username": username,
            "moves": moves,
            "timestamp": datetime.now().isoformat()
        }
        
        self.data[level_name].append(entry)
        # Sort by moves (ascending - fewer is better)
        self.data[level_name].sort(key=lambda x: x["moves"])
        # Keep only top 10
        self.data[level_name] = self.data[level_name][:10]
        
        self.save_leaderboard()
    
    def get_leaderboard(self, level_name):
        """Get leaderboard for a specific level"""
        return self.data.get(level_name, [])


class GameState:
    """Manages the game state and logic"""
    def __init__(self, level_data=None):
        self.move_count = 0
        if level_data:
            self.load_level(level_data)
        else:
            self.load_default_level()
        
        self.initial_player = copy.deepcopy(self.player)
        self.initial_board = copy.deepcopy(self.display_board)
        self.toggle_board = copy.deepcopy(self.display_board)
    
    def load_default_level(self):
        """Load the default level"""
        self.player = {
            "xPos": 2,
            "yPos": 2,
            "mushroom": 0,
            "win": 1,
            "axe": 0,
            "flamethrower": 0
        }
        
        self.display_board = [
            ["🌲", "🌲", "🌲", "🌲", "🌲", "🌲", "🌲", "🌲", "🌲", "🌲"],
            ["🌲", "　", "　", "　", "　", "　", "　", "　", "　", "🌲"],
            ["🌲", "　", "🧑", "　", "　", "　", "　", "🍄", "　", "🌲"],
            ["🌲", "　", "　", "　", "　", "　", "　", "　", "　", "🌲"],
            ["🌲", "🌲", "🌲", "🌲", "🌲", "🌲", "🌲", "🌲", "🌲", "🌲"]
        ]
    
    def load_level(self, level_data):
        """Load a level from string data"""
        lines = level_data.strip().split('\n')
        # Skip the first line (r = x; c = y) and empty line
        board_lines = [line for line in lines[1:] if line.strip()]
        
        row = 0
        display_board = []
        
        self.player = {
            "xPos": 0,
            "yPos": 0,
            "mushroom": 0,
            "win": 0,
            "axe": 0,
            "flamethrower": 0,
        }
        
        for line in board_lines:
            col = 0
            row_constructor = []
            for char in line:
                if char == "L":
                    self.player["xPos"] = col
                    self.player["yPos"] = row
                    row_constructor.append("🧑")
                elif char == "+":
                    self.player["win"] += 1
                    row_constructor.append("🍄")
                elif char == ".":
                    row_constructor.append("　")
                elif char == "T":
                    row_constructor.append("🌲")
                elif char == "R":
                    row_constructor.append("🪨")
                elif char == "~":
                    row_constructor.append("🟦")
                elif char == "-":
                    row_constructor.append("⬜")
                elif char == "x":
                    row_constructor.append("🪓")
                elif char == "*":
                    row_constructor.append("🔥")
                col += 1
            if row_constructor:
                display_board.append(row_constructor)
                row += 1
        
        self.display_board = display_board
    
    def restart(self):
        """Reset the game to initial state"""
        self.move_count = 0
        self.player = copy.deepcopy(self.initial_player)
        self.display_board = copy.deepcopy(self.initial_board)
        self.toggle_board = copy.deepcopy(self.initial_board)
    
    def burn_tree(self, i, j):
        """Recursively burn adjacent trees"""
        # Check bounds first
        if i < 0 or j < 0 or i >= len(self.display_board) or j >= len(self.display_board[0]):
            return
        
        # Only burn if it's a tree
        if self.display_board[i][j] != "🌲":
            return
        
        # Burn this tree
        self.display_board[i][j] = "　"
        
        # Recursively burn adjacent trees
        adjacent = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dy, dx in adjacent:
            self.burn_tree(i + dy, j + dx)
    
    def clear_space(self, y_move, x_move):
        """Clear the current space before moving"""
        space_tiles = ("　", "🍄", "🌲", "🪨", "🧑")
        if self.initial_board[self.player["yPos"]][self.player["xPos"]] in space_tiles:
            self.display_board[self.player["yPos"]][self.player["xPos"]] = "　"
        elif self.initial_board[self.player["yPos"]][self.player["xPos"]] == "🟦":
            self.display_board[self.player["yPos"]][self.player["xPos"]] = "⬜"
        elif self.initial_board[self.player["yPos"]][self.player["xPos"]] == "🪓":
            if self.toggle_board[self.player["yPos"]][self.player["xPos"]] == "/":
                self.display_board[self.player["yPos"]][self.player["xPos"]] = "　"
            else:
                self.display_board[self.player["yPos"]][self.player["xPos"]] = "🪓"
        elif self.initial_board[self.player["yPos"]][self.player["xPos"]] == "🔥":
            if self.toggle_board[self.player["yPos"]][self.player["xPos"]] == "/":
                self.display_board[self.player["yPos"]][self.player["xPos"]] = "　"
            else:
                self.display_board[self.player["yPos"]][self.player["xPos"]] = "🔥"
        
        self.player["yPos"] += y_move
        self.player["xPos"] += x_move
        
        if self.player["yPos"] < 0:
            self.player["yPos"] = 0
        if self.player["xPos"] < 0:
            self.player["xPos"] = 0
    
    def move(self, y_move, x_move):
        """
        Execute a move. Returns:
        - 'win' if player collected all mushrooms
        - 'loss' if player drowned
        - 'moved' if move was successful
        - 'blocked' if move was blocked
        """
        try:
            next_tile = self.display_board[self.player["yPos"] + y_move][self.player["xPos"] + x_move]
        except IndexError:
            return 'blocked'
        
        skip_tiles = ("　", "⬜", "🪓", "🔥")
        
        # Empty spaces
        if next_tile in skip_tiles:
            self.clear_space(y_move, x_move)
            self.move_count += 1
            return 'moved'
        
        # Mushrooms
        elif next_tile == "🍄":
            self.player["mushroom"] += 1
            self.clear_space(y_move, x_move)
            self.move_count += 1
            if self.player["mushroom"] == self.player["win"]:
                return 'win'
            return 'moved'
        
        # Water
        elif next_tile == "🟦":
            self.clear_space(y_move, x_move)
            self.move_count += 1
            return 'loss'
        
        # Rocks
        elif next_tile == "🪨":
            avoid = ("🍄", "🪨", "🪓", "🔥", "🌲")
            try:
                beyond_tile = self.display_board[self.player["yPos"] + (y_move * 2)][self.player["xPos"] + (x_move * 2)]
                if beyond_tile not in avoid:
                    if beyond_tile == "🟦":
                        self.display_board[self.player["yPos"] + (y_move * 2)][self.player["xPos"] + (x_move * 2)] = "⬜"
                    else:
                        self.display_board[self.player["yPos"] + (y_move * 2)][self.player["xPos"] + (x_move * 2)] = "🪨"
                    self.clear_space(y_move, x_move)
                    self.move_count += 1
                    return 'moved'
            except IndexError:
                pass
            return 'blocked'
        
        # Trees
        elif next_tile == "🌲":
            if self.player["axe"] > 0:
                self.clear_space(y_move, x_move)
                self.move_count += 1
                self.player["axe"] -= 1
                return 'moved'
            elif self.player["flamethrower"] > 0:
                # Burn the tree at the next position and all adjacent trees
                next_y = self.player["yPos"] + y_move
                next_x = self.player["xPos"] + x_move
                self.burn_tree(next_y, next_x)
                self.clear_space(y_move, x_move)
                self.move_count += 1
                self.player["flamethrower"] -= 1
                return 'moved'
            return 'blocked'
        
        return 'blocked'
    
    def pickup_item(self):
        """Try to pick up an item at current position"""
        if self.player["axe"] == 0 and self.player["flamethrower"] == 0:
            if self.initial_board[self.player["yPos"]][self.player["xPos"]] == "🪓" and \
               self.toggle_board[self.player["yPos"]][self.player["xPos"]] != "/":
                self.toggle_board[self.player["yPos"]][self.player["xPos"]] = "/"
                self.player["axe"] += 1
                return True
            elif self.initial_board[self.player["yPos"]][self.player["xPos"]] == "🔥" and \
                 self.toggle_board[self.player["yPos"]][self.player["xPos"]] != "/":
                self.toggle_board[self.player["yPos"]][self.player["xPos"]] = "/"
                self.player["flamethrower"] += 1
                return True
        return False
    
    def position_player(self):
        """Place player on the board"""
        self.display_board[self.player["yPos"]][self.player["xPos"]] = "🧑"
    
    def get_board_string(self):
        """Get the board as a formatted string"""
        self.position_player()
        return "\n".join(" ".join(line) for line in self.display_board)


class GameScreen(Screen):
    """The main game screen"""
    
    BINDINGS = [
        Binding("w,up", "move_up", "Move Up", show=False),
        Binding("s,down", "move_down", "Move Down", show=False),
        Binding("a,left", "move_left", "Move Left", show=False),
        Binding("d,right", "move_right", "Move Right", show=False),
        Binding("p", "pickup", "Pickup Item", show=True),
        Binding("r", "restart", "Restart", show=True),
        Binding("escape", "back_to_menu", "Menu", show=True),
    ]
    
    def __init__(self, level_data=None, level_name="Level 1"):
        super().__init__()
        self.game_state = GameState(level_data)
        self.level_name = level_name
        self.game_over = False
    
    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="game_container"):
            yield Label(self.level_name, id="level_title")
            yield Static(id="game_board")
            yield Static(id="game_info")
        yield Footer()
    
    def on_mount(self) -> None:
        self.update_display()
    
    def update_display(self):
        """Update the game board and info display"""
        board_widget = self.query_one("#game_board", Static)
        info_widget = self.query_one("#game_info", Static)
        
        # Update board
        board_text = Text(self.game_state.get_board_string(), justify="center")
        board_widget.update(Panel(board_text, border_style="cyan", title="🍄 Mushroom Collector 🍄"))
        
        # Update info
        info_lines = [
            f"Mushrooms: {self.game_state.player['mushroom']}/{self.game_state.player['win']}",
            f"Moves: {self.game_state.move_count}",
            "",
        ]
        
        if self.game_state.player["axe"] > 0:
            info_lines.append("Item: 🪓 Axe")
        elif self.game_state.player["flamethrower"] > 0:
            info_lines.append("Item: 🔥 Flamethrower")
        else:
            info_lines.append("Item: None")
            
            # Check for pickupable items
            y, x = self.game_state.player["yPos"], self.game_state.player["xPos"]
            if self.game_state.initial_board[y][x] == "🪓" and \
               self.game_state.toggle_board[y][x] != "/":
                info_lines.append("Press P to pick up Axe")
            elif self.game_state.initial_board[y][x] == "🔥" and \
                 self.game_state.toggle_board[y][x] != "/":
                info_lines.append("Press P to pick up Flamethrower")
        
        info_widget.update("\n".join(info_lines))
    
    def action_move_up(self):
        if not self.game_over:
            result = self.game_state.move(-1, 0)
            self.handle_move_result(result)
    
    def action_move_down(self):
        if not self.game_over:
            result = self.game_state.move(1, 0)
            self.handle_move_result(result)
    
    def action_move_left(self):
        if not self.game_over:
            result = self.game_state.move(0, -1)
            self.handle_move_result(result)
    
    def action_move_right(self):
        if not self.game_over:
            result = self.game_state.move(0, 1)
            self.handle_move_result(result)
    
    def action_pickup(self):
        if not self.game_over:
            self.game_state.pickup_item()
            self.update_display()
    
    def action_restart(self):
        self.game_over = False
        self.game_state.restart()
        self.update_display()
    
    def action_back_to_menu(self):
        self.app.pop_screen()
    
    def handle_move_result(self, result):
        """Handle the result of a move"""
        self.update_display()
        
        if result == 'win':
            self.game_over = True
            self.app.push_screen(WinScreen(self.level_name, self.game_state.move_count))
        elif result == 'loss':
            self.game_over = True
            self.app.push_screen(LossScreen())


class WinScreen(Screen):
    """Screen shown when player wins"""
    
    BINDINGS = [
        Binding("r", "play_again", "Play Again", show=False),
        Binding("escape", "to_menu", "Menu", show=False),
    ]
    
    def __init__(self, level_name, move_count):
        super().__init__()
        self.level_name = level_name
        self.move_count = move_count
        self.username_saved = False
    
    def compose(self) -> ComposeResult:
        with Center():
            with Container(id="modal_container"):
                yield Label("🎉 YOU WIN! 🎉", id="modal_title")
                yield Label(f"You collected all mushrooms in {self.move_count} moves!", id="modal_message")
                yield Label("Enter username for leaderboard (optional):", id="username_label")
                yield Input(placeholder="Username", id="username_input")
                with Horizontal(id="modal_buttons"):
                    yield Button("Save & Continue", id="save_score", variant="success")
                    yield Button("Skip", id="skip", variant="default")
                    yield Button("Menu", id="menu", variant="primary")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_score":
            username_input = self.query_one("#username_input", Input)
            username = username_input.value.strip()
            if username:
                leaderboard = self.app.leaderboard
                leaderboard.add_score(username, self.level_name, self.move_count)
                self.username_saved = True
            self.action_play_again()
        elif event.button.id == "skip":
            self.action_play_again()
        elif event.button.id == "menu":
            self.action_to_menu()
    
    def action_play_again(self):
        self.app.pop_screen()
        game_screen = self.app.screen_stack[-1]
        if isinstance(game_screen, GameScreen):
            game_screen.action_restart()
    
    def action_to_menu(self):
        self.app.pop_screen()
        self.app.pop_screen()


class LossScreen(Screen):
    """Screen shown when player loses"""
    
    BINDINGS = [
        Binding("r", "try_again", "Try Again", show=False),
        Binding("escape", "to_menu", "Menu", show=False),
    ]
    
    def compose(self) -> ComposeResult:
        with Center():
            with Container(id="modal_container"):
                yield Label("💀 GAME OVER 💀", id="modal_title")
                yield Label("You drowned in the water!", id="modal_message")
                with Horizontal(id="modal_buttons"):
                    yield Button("Try Again (R)", id="try_again", variant="warning")
                    yield Button("Menu (ESC)", id="menu", variant="primary")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "try_again":
            self.action_try_again()
        elif event.button.id == "menu":
            self.action_to_menu()
    
    def action_try_again(self):
        self.app.pop_screen()
        game_screen = self.app.screen_stack[-1]
        if isinstance(game_screen, GameScreen):
            game_screen.action_restart()
    
    def action_to_menu(self):
        self.app.pop_screen()
        self.app.pop_screen()


class LeaderboardScreen(Screen):
    """Screen showing leaderboard for a specific level"""
    
    BINDINGS = [
        Binding("escape", "back", "Back", show=True),
    ]
    
    def __init__(self, level_name):
        super().__init__()
        self.level_name = level_name
    
    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            with Container(id="leaderboard_container"):
                yield Label(f"🏆 {self.level_name} Leaderboard 🏆", id="leaderboard_title")
                yield Static(id="leaderboard_table")
                with Center():
                    yield Button("Back", id="back", variant="primary")
        yield Footer()
    
    def on_mount(self):
        self.update_leaderboard()
    
    def update_leaderboard(self):
        """Update the leaderboard display"""
        table = Table(title="Top 10 Scores", border_style="cyan", show_header=True)
        table.add_column("Rank", style="yellow", justify="center")
        table.add_column("Username", style="green")
        table.add_column("Moves", style="cyan", justify="center")
        
        scores = self.app.leaderboard.get_leaderboard(self.level_name)
        
        if scores:
            for i, score in enumerate(scores, 1):
                rank_emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                table.add_row(
                    rank_emoji,
                    score["username"],
                    str(score["moves"])
                )
        else:
            table.add_row("—", "No scores yet", "—")
        
        self.query_one("#leaderboard_table", Static).update(table)
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.action_back()
    
    def action_back(self):
        self.app.pop_screen()


class LevelSelectScreen(Screen):
    """Screen for selecting levels"""
    
    BINDINGS = [
        Binding("escape", "back", "Back", show=True),
    ]
    
    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="level_select_container"):
            yield Label("SELECT LEVEL", id="level_select_title")
            with Grid(id="level_grid"):
                for i in range(1, 16):
                    with Vertical(classes="level_card"):
                        yield Button(f"Level {i}", id=f"level_{i}", variant="primary", classes="level_button")
                        yield Button("🏆", id=f"leaderboard_{i}", variant="default", classes="leaderboard_btn")
            with Center():
                yield Button("Back to Menu", id="back", variant="default", classes="back_button")
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.action_back()
        elif event.button.id.startswith("leaderboard_"):
            level_num = int(event.button.id.split("_")[1])
            level_name = f"Level {level_num}"
            self.app.push_screen(LeaderboardScreen(level_name))
        elif event.button.id.startswith("level_"):
            level_num = int(event.button.id.split("_")[1])
            level_name = f"Level {level_num}"
            level_file = Path(f"levels/Level{level_num}.txt")
            
            if level_file.exists():
                with open(level_file, 'r', encoding='utf-8') as f:
                    level_data = f.read()
                self.app.push_screen(GameScreen(level_data, level_name))
            else:
                # Show error or use default level
                self.app.push_screen(GameScreen(None, level_name))
    
    def action_back(self):
        self.app.pop_screen()

class MainMenuScreen(Screen):
    """Main menu screen"""
    
    BINDINGS = [
        Binding("q", "quit_app", "Exit", show=True),
    ]
    
    def compose(self) -> ComposeResult:
        yield Header()
        with Center():
            with Container(id="menu_container"):
                yield Label("🍄 MUSHROOM COLLECTOR 🍄", id="menu_title")
                with Vertical(id="menu_buttons"):
                    yield Button("Play", id="play", variant="success")
                    yield Button("Levels", id="levels", variant="primary")
                    yield Button("Exit", id="exit", variant="error")
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "play":
            self.app.push_screen(GameScreen())
        elif event.button.id == "levels":
            self.app.push_screen(LevelSelectScreen())
        elif event.button.id == "exit":
            self.app.exit()
    
    def action_quit_app(self):
        self.app.exit()


class MushroomGame(App):
    """Main application"""
    
    CSS_PATH = "game_styles.tcss"
    
    BINDINGS = [
        Binding("q", "quit", "Quit", show=False, priority=True),
    ]
    
    def __init__(self):
        super().__init__()
        self.leaderboard = LeaderboardManager()
    
    def on_mount(self) -> None:
        self.push_screen(MainMenuScreen())


if __name__ == "__main__":
    app = MushroomGame()
    app.run()