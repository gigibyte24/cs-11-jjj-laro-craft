import os
import sys
import copy
import json
from pathlib import Path
from datetime import datetime
from argparse import ArgumentParser
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Static, Button, Label, Header, Footer, Input
from textual.containers import Container, Vertical, Horizontal, Grid, Center
from textual.binding import Binding
from rich.text import Text
from rich.panel import Panel
from rich.table import Table


def parse_args():
    """Parse command line arguments for terminal mode"""
    parser = ArgumentParser(description="Shroom Raider - Mushroom Collector Game")
    parser.add_argument('-f', '--file', help='Stage file path')
    parser.add_argument('-m', '--moves', help='String of moves')
    parser.add_argument('-o', '--output', help='Output file path')
    return parser.parse_args()


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
        }
        
        self.data[level_name].append(entry)
        self.data[level_name].sort(key=lambda x: x["moves"])
        self.data[level_name] = self.data[level_name][:10]
        self.save_leaderboard()
    
    def get_leaderboard(self, level_name):
        """Get leaderboard for a specific level"""
        return self.data.get(level_name, [])


class GameState:
    """Manages the game state and logic"""
    def __init__(self, level_data=None):
        self.move_count = 0
        self.total_mushrooms_collected = 0
        if level_data:
            self.load_level(level_data)
        else:
            self.load_default_level()
        
        self.initial_player1 = copy.deepcopy(self.player1)
        self.initial_player2 = copy.deepcopy(self.player2)
        self.initial_board = copy.deepcopy(self.display_board)
        self.toggle_board = copy.deepcopy(self.display_board)
        self.total_mushrooms = self.player1["win"]
    
    def load_default_level(self):
        """Load the default level"""
        self.player1 = {
            "xPos": 2,
            "yPos": 2,
            "axe": 0,
            "flamethrower": 0,
            "win": 2
        }
        
        self.player2 = {
            "xPos": 7,
            "yPos": 2,
            "axe": 0,
            "flamethrower": 0,
            "win": 2
        }
        
        self.display_board = [
            ["🌲", "🌲", "🌲", "🌲", "🌲", "🌲", "🌲", "🌲", "🌲", "🌲"],
            ["🌲", "　", "　", "　", "　", "　", "　", "　", "　", "🌲"],
            ["🌲", "　", "🧑", "　", "　", "　", "　", "👩", "　", "🌲"],
            ["🌲", "　", "　", "　", "🍄", "🍄", "　", "　", "　", "🌲"],
            ["🌲", "🌲", "🌲", "🌲", "🌲", "🌲", "🌲", "🌲", "🌲", "🌲"]
        ]
    
    def load_level(self, level_data):
        """Load a level from string data"""
        lines = level_data.strip().split('\n')
        board_lines = [line for line in lines if line.strip() and not line.startswith('r =')]
        
        row = 0
        display_board = []
        mushroom_count = 0
        
        self.player1 = {
            "xPos": 0,
            "yPos": 0,
            "axe": 0,
            "flamethrower": 0,
            "win": 0
        }
        
        self.player2 = {
            "xPos": 0,
            "yPos": 0,
            "axe": 0,
            "flamethrower": 0,
            "win": 0
        }
        
        for line in board_lines:
            col = 0
            row_constructor = []
            for char in line:
                if char == "L":
                    self.player1["xPos"] = col
                    self.player1["yPos"] = row
                    row_constructor.append("🧑")
                elif char == "O":
                    self.player2["xPos"] = col
                    self.player2["yPos"] = row
                    row_constructor.append("👩")
                elif char == "+":
                    mushroom_count += 1
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
        
        self.player1["win"] = mushroom_count
        self.player2["win"] = mushroom_count
        self.display_board = display_board
    
    def restart(self):
        """Reset the game to initial state"""
        self.move_count = 0
        self.total_mushrooms_collected = 0
        self.player1 = copy.deepcopy(self.initial_player1)
        self.player2 = copy.deepcopy(self.initial_player2)
        self.display_board = copy.deepcopy(self.initial_board)
        self.toggle_board = copy.deepcopy(self.initial_board)
    
    def burn_tree(self, i, j):
        """Recursively burn adjacent trees"""
        if i < 0 or j < 0 or i >= len(self.display_board) or j >= len(self.display_board[0]):
            return
        if self.display_board[i][j] != "🌲":
            return
        self.display_board[i][j] = "　"
        adjacent = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dy, dx in adjacent:
            self.burn_tree(i + dy, j + dx)
    
    def clear_space(self, y_move, x_move, player):
        """Clear the current space before moving"""
        space_tiles = ("　", "🍄", "🌲", "🪨", "🧑", "👩")
        if self.initial_board[player["yPos"]][player["xPos"]] in space_tiles:
            self.display_board[player["yPos"]][player["xPos"]] = "　"
        elif self.initial_board[player["yPos"]][player["xPos"]] == "🟦":
            self.display_board[player["yPos"]][player["xPos"]] = "⬜"
        elif self.initial_board[player["yPos"]][player["xPos"]] == "🪓":
            if self.toggle_board[player["yPos"]][player["xPos"]] == "/":
                self.display_board[player["yPos"]][player["xPos"]] = "　"
            else:
                self.display_board[player["yPos"]][player["xPos"]] = "🪓"
        elif self.initial_board[player["yPos"]][player["xPos"]] == "🔥":
            if self.toggle_board[player["yPos"]][player["xPos"]] == "/":
                self.display_board[player["yPos"]][player["xPos"]] = "　"
            else:
                self.display_board[player["yPos"]][player["xPos"]] = "🔥"
        
        player["yPos"] += y_move
        player["xPos"] += x_move
        
        if player["yPos"] < 0:
            player["yPos"] = 0
        if player["xPos"] < 0:
            player["xPos"] = 0
    
    def move(self, y_move, x_move, player_num):
        """Execute a move for a specific player"""
        player = self.player1 if player_num == 1 else self.player2
        other_player = self.player2 if player_num == 1 else self.player1
        
        try:
            next_tile = self.display_board[player["yPos"] + y_move][player["xPos"] + x_move]
        except IndexError:
            return 'blocked'
        
        if (player["yPos"] + y_move == other_player["yPos"] and 
            player["xPos"] + x_move == other_player["xPos"]):
            return 'blocked'
        
        skip_tiles = ("　", "⬜", "🪓", "🔥")
        
        if next_tile in skip_tiles:
            self.clear_space(y_move, x_move, player)
            self.move_count += 1
            return 'moved'
        
        elif next_tile == "🍄":
            self.total_mushrooms_collected += 1
            self.clear_space(y_move, x_move, player)
            self.move_count += 1
            if self.total_mushrooms_collected == self.total_mushrooms:
                return 'win'
            return 'moved'
        
        elif next_tile == "🟦":
            self.clear_space(y_move, x_move, player)
            self.move_count += 1
            return 'loss'
        
        elif next_tile == "🪨":
            avoid = ("🍄", "🪨", "🪓", "🔥", "🌲", "🧑", "👩")
            try:
                beyond_tile = self.display_board[player["yPos"] + (y_move * 2)][player["xPos"] + (x_move * 2)]
                if (player["yPos"] + (y_move * 2) == other_player["yPos"] and 
                    player["xPos"] + (x_move * 2) == other_player["xPos"]):
                    return 'blocked'
                
                if beyond_tile not in avoid:
                    if beyond_tile == "🟦":
                        self.display_board[player["yPos"] + (y_move * 2)][player["xPos"] + (x_move * 2)] = "⬜"
                    else:
                        self.display_board[player["yPos"] + (y_move * 2)][player["xPos"] + (x_move * 2)] = "🪨"
                    self.clear_space(y_move, x_move, player)
                    self.move_count += 1
                    return 'moved'
            except IndexError:
                pass
            return 'blocked'
        
        elif next_tile == "🌲":
            if player["axe"] > 0:
                self.clear_space(y_move, x_move, player)
                self.move_count += 1
                player["axe"] -= 1
                return 'moved'
            elif player["flamethrower"] > 0:
                next_y = player["yPos"] + y_move
                next_x = player["xPos"] + x_move
                self.burn_tree(next_y, next_x)
                self.clear_space(y_move, x_move, player)
                self.move_count += 1
                player["flamethrower"] -= 1
                return 'moved'
            return 'blocked'
        
        return 'blocked'
    
    def pickup_item(self, player_num):
        """Try to pick up an item at current position for specific player"""
        player = self.player1 if player_num == 1 else self.player2
        
        if player["axe"] == 0 and player["flamethrower"] == 0:
            if self.initial_board[player["yPos"]][player["xPos"]] == "🪓" and \
               self.toggle_board[player["yPos"]][player["xPos"]] != "/":
                self.toggle_board[player["yPos"]][player["xPos"]] = "/"
                player["axe"] += 1
                return True
            elif self.initial_board[player["yPos"]][player["xPos"]] == "🔥" and \
                 self.toggle_board[player["yPos"]][player["xPos"]] != "/":
                self.toggle_board[player["yPos"]][player["xPos"]] = "/"
                player["flamethrower"] += 1
                return True
        return False
    
    def position_players(self):
        """Place both players on the board"""
        self.display_board[self.player1["yPos"]][self.player1["xPos"]] = "🧑"
        self.display_board[self.player2["yPos"]][self.player2["xPos"]] = "👩"
    
    def get_board_string(self):
        """Get the board as a formatted string"""
        self.position_players()
        return "\n".join(" ".join(line) for line in self.display_board)
    
    def export_to_file(self, output_file, result):
        """Export current state to output file"""
        self.position_players()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result + "\n")
            f.write(f"r = {len(self.display_board)}; c = {len(self.display_board[0])}\n")
            
            for row in self.display_board:
                line = ""
                for cell in row:
                    if cell == "🧑":
                        line += "L"
                    elif cell == "👩":
                        line += "O"
                    elif cell == "🍄":
                        line += "+"
                    elif cell == "　":
                        line += "."
                    elif cell == "🌲":
                        line += "T"
                    elif cell == "🪨":
                        line += "R"
                    elif cell == "🟦":
                        line += "~"
                    elif cell == "⬜":
                        line += "-"
                    elif cell == "🪓":
                        line += "x"
                    elif cell == "🔥":
                        line += "*"
                f.write(line + "\n")


class GameScreen(Screen):
    """The main game screen"""
    
    BINDINGS = [
        Binding("w", "move_p1_up", "P1 Up", show=False),
        Binding("s", "move_p1_down", "P1 Down", show=False),
        Binding("a", "move_p1_left", "P1 Left", show=False),
        Binding("d", "move_p1_right", "P1 Right", show=False),
        Binding("i", "move_p2_up", "P2 Up", show=False),
        Binding("k", "move_p2_down", "P2 Down", show=False),
        Binding("j", "move_p2_left", "P2 Left", show=False),
        Binding("l", "move_p2_right", "P2 Right", show=False),
        Binding("p", "pickup_p1", "P1 Pickup", show=False),
        Binding("o", "pickup_p2", "P2 Pickup", show=False),
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
        with Center():
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
        
        board_text = Text(self.game_state.get_board_string(), justify="center")
        board_widget.update(Panel(board_text, border_style="bright_cyan", title="🍄 Shroom Raider 🍄", 
                title_align="center"))
        
        p1 = self.game_state.player1
        p2 = self.game_state.player2
        
        mushroom_progress = f"{self.game_state.total_mushrooms_collected}/{self.game_state.total_mushrooms}"
        
        info_text = Text()
        info_text.append("═" * 50 + "\n", style="bold bright_cyan")
        info_text.append(f"  🎯 Total Progress: ", style="bold yellow")
        info_text.append(f"{mushroom_progress} Mushrooms  ", style="bold bright_green")
        info_text.append(f"  📊 Moves: {self.game_state.move_count}\n", style="bold bright_blue")
        info_text.append("═" * 50 + "\n\n", style="bold bright_cyan")
        
        info_text.append("🧑 Player 1 (WASD)\n", style="bold bright_green")
        if p1["axe"] > 0:
            info_text.append("  Item: 🪓 Axe\n", style="bright_yellow")
        elif p1["flamethrower"] > 0:
            info_text.append("  Item: 🔥 Flamethrower\n", style="bright_red")
        else:
            info_text.append("  Item: None\n", style="dim")
        
        info_text.append("\n👩 Player 2 (IJKL)\n", style="bold bright_magenta")
        if p2["axe"] > 0:
            info_text.append("  Item: 🪓 Axe\n", style="bright_yellow")
        elif p2["flamethrower"] > 0:
            info_text.append("  Item: 🔥 Flamethrower\n", style="bright_red")
        else:
            info_text.append("  Item: None\n", style="dim")
        
        info_widget.update(info_text)
    
    def action_move_p1_up(self):
        if not self.game_over:
            result = self.game_state.move(-1, 0, 1)
            self.handle_move_result(result)
    
    def action_move_p1_down(self):
        if not self.game_over:
            result = self.game_state.move(1, 0, 1)
            self.handle_move_result(result)
    
    def action_move_p1_left(self):
        if not self.game_over:
            result = self.game_state.move(0, -1, 1)
            self.handle_move_result(result)
    
    def action_move_p1_right(self):
        if not self.game_over:
            result = self.game_state.move(0, 1, 1)
            self.handle_move_result(result)
    
    def action_pickup_p1(self):
        if not self.game_over:
            self.game_state.pickup_item(1)
            self.update_display()
    
    def action_move_p2_up(self):
        if not self.game_over:
            result = self.game_state.move(-1, 0, 2)
            self.handle_move_result(result)
    
    def action_move_p2_down(self):
        if not self.game_over:
            result = self.game_state.move(1, 0, 2)
            self.handle_move_result(result)
    
    def action_move_p2_left(self):
        if not self.game_over:
            result = self.game_state.move(0, -1, 2)
            self.handle_move_result(result)
    
    def action_move_p2_right(self):
        if not self.game_over:
            result = self.game_state.move(0, 1, 2)
            self.handle_move_result(result)
    
    def action_pickup_p2(self):
        if not self.game_over:
            self.game_state.pickup_item(2)
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
    """Screen shown when players win"""
    
    BINDINGS = [
        Binding("r", "play_again", "Play Again", show=False),
        Binding("escape", "to_menu", "Menu", show=False),
    ]
    
    def __init__(self, level_name, move_count):
        super().__init__()
        self.level_name = level_name
        self.move_count = move_count
    
    def compose(self) -> ComposeResult:
        with Center():
            with Container(id="modal_container"):
                yield Label("🎉 VICTORY! 🎉", id="modal_title")
                yield Label(f"Completed in {self.move_count} moves!", id="modal_message")
                yield Label("Enter username for leaderboard:", id="username_label")
                yield Input(placeholder="Username (optional)", id="username_input")
                with Horizontal(id="modal_buttons"):
                    yield Button("💾 Save", id="save_score", variant="success")
                    yield Button("⏭️ Skip", id="skip", variant="default")
                    yield Button("🏠 Menu", id="menu", variant="primary")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_score":
            username_input = self.query_one("#username_input", Input)
            username = username_input.value.strip()
            if username:
                self.app.leaderboard.add_score(username, self.level_name, self.move_count)
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
    """Screen shown when a player loses"""
    
    BINDINGS = [
        Binding("r", "try_again", "Try Again", show=False),
        Binding("escape", "to_menu", "Menu", show=False),
    ]
    
    def compose(self) -> ComposeResult:
        with Center():
            with Container(id="modal_container"):
                yield Label("💀 GAME OVER 💀", id="modal_title")
                yield Label("A player drowned!", id="modal_message")
                with Horizontal(id="modal_buttons"):
                    yield Button("🔄 Try Again", id="try_again", variant="warning")
                    yield Button("🏠 Menu", id="menu", variant="primary")
    
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
                yield Button("⬅️ Back", id="back", variant="primary", classes="centered_button")
        yield Footer()
    
    def on_mount(self):
        self.update_leaderboard()
    
    def update_leaderboard(self):
        """Update the leaderboard display"""
        table = Table(title="🌟 Top 10 Scores 🌟", border_style="bright_cyan", show_header=True, 
                     title_style="bold bright_yellow")
        table.add_column("Rank", style="bold yellow", justify="center", width=8)
        table.add_column("Username", style="bold bright_green", width=20)
        table.add_column("Moves", style="bold bright_cyan", justify="center", width=10)
        
        scores = self.app.leaderboard.get_leaderboard(self.level_name)
        
        if scores:
            for i, score in enumerate(scores, 1):
                rank_emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                table.add_row(rank_emoji, score["username"], str(score["moves"]))
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
        with Center():
            with Container(id="level_select_container"):
                yield Label("🎮 SELECT LEVEL 🎮", id="level_select_title")
                with Grid(id="level_grid"):
                    for i in range(1, 16):
                        with Vertical(classes="level_card"):
                            yield Button(f"🍄 Level {i}", id=f"level_{i}", variant="primary", classes="level_button")
                            yield Button("🏆", id=f"leaderboard_{i}", variant="default", classes="leaderboard_btn")
                yield Button("⬅️ Back to Menu", id="back", variant="default", classes="centered_button")
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        
        if button_id == "back":
            self.action_back()
        elif button_id.startswith("leaderboard_"):
            level_num = int(button_id.split("_")[1])
            level_name = f"Level {level_num}"
            self.app.push_screen(LeaderboardScreen(level_name))
        elif button_id.startswith("level_"):
            level_num = int(button_id.split("_")[1])
            level_name = f"Level {level_num}"
            level_file = Path(f"levels/Level{level_num}.txt")
            
            if level_file.exists():
                with open(level_file, 'r', encoding='utf-8') as f:
                    level_data = f.read()
                self.app.push_screen(GameScreen(level_data, level_name))
            else:
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
                yield Label("🍄 SHROOM RAIDER 🍄", id="menu_title")
                yield Label("Cooperative Mushroom Collector", id="menu_subtitle")
                with Vertical(id="menu_buttons"):
                    yield Button("🎮 Play", id="play", variant="success")
                    yield Button("📋 Levels", id="levels", variant="primary")
                    yield Button("🚪 Exit", id="exit", variant="error")
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


def run_terminal_mode(stage_file, moves, output_file):
    """Run game in terminal mode and output to file"""
    # Load stage file
    with open(stage_file, 'r', encoding='utf-8') as f:
        level_data = f.read()
    
    # Create game state
    game = GameState(level_data)
    
    # Process moves
    for move in moves.lower():
        if move == 'w':
            result = game.move(-1, 0, 1)
        elif move == 's':
            result = game.move(1, 0, 1)
        elif move == 'a':
            result = game.move(0, -1, 1)
        elif move == 'd':
            result = game.move(0, 1, 1)
        elif move == 'i':
            result = game.move(-1, 0, 2)
        elif move == 'k':
            result = game.move(1, 0, 2)
        elif move == 'j':
            result = game.move(0, -1, 2)
        elif move == 'l':
            result = game.move(0, 1, 2)
        elif move == 'p':
            game.pickup_item(1)
            continue
        elif move == 'o':
            game.pickup_item(2)
            continue
        else:
            continue
        
        # Check for win/loss
        if result == 'win':
            game.export_to_file(output_file, "Clear")
            return
        elif result == 'loss':
            game.export_to_file(output_file, "No Clear")
            return
    
    # If moves ran out
    game.export_to_file(output_file, "No Clear")


def main():
    """Main entry point for the application"""
    args = parse_args()
    
    if args.file and args.moves and args.output:
        # Terminal mode
        run_terminal_mode(args.file, args.moves, args.output)
    else:
        # GUI mode
        app = MushroomGame()
        app.run()


if __name__ == "__main__":
    main()