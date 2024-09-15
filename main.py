import tkinter as tk
from tkinter import messagebox
import logic  # Assuming logic.py is in the same directory

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title("2048 Game")
        self.grid_color = "#bbada0"
        self.empty_color = "#cdc1b4"
        self.tile_colors = {
            2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563",
            32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61",
            512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
        }
        self.tile_font = ("Helvetica", 40, "bold")
        self.score_font = ("Helvetica", 20, "bold")

        # Initialize game with the home screen
        self.home_screen()

    def home_screen(self):
        """Display the home screen with Play and Exit buttons."""
        self.clear_screen()

        self.home_frame = tk.Frame(self.master, bg=self.grid_color, bd=3, width=400, height=400)
        self.home_frame.grid(padx=10, pady=10)

        tk.Label(self.home_frame, text="Welcome to 2048!", font=("Helvetica", 30, "bold"), bg=self.grid_color, fg="white").pack(pady=20)

        play_button = tk.Button(self.home_frame, text="Play Game", font=("Helvetica", 20), command=self.start_game, width=10, height=2, bg="#8f7a66", fg="white")
        play_button.pack(pady=20)

        exit_button = tk.Button(self.home_frame, text="Exit", font=("Helvetica", 20), command=self.master.quit, width=10, height=2, bg="#8f7a66", fg="white")
        exit_button.pack(pady=20)

    def start_game(self):
        """Start the 2048 game and display the game grid."""
        self.clear_screen()

        # Recreate the grid frame after clearing the screen
        self.grid_frame = tk.Frame(self.master, bg=self.grid_color, bd=3, width=400, height=400)
        self.grid_frame.grid(padx=10, pady=10)

        # Initialize the game matrix
        self.game_matrix = logic.start_game()
        self.cells = []

        # Create the grid of cells (4x4 grid)
        for i in range(4):
            row = []
            for j in range(4):
                cell = tk.Label(self.grid_frame, text="", bg=self.empty_color, width=4, height=2, font=self.tile_font)
                cell.grid(row=i, column=j, padx=5, pady=5)
                row.append(cell)
            self.cells.append(row)

        # Update the grid with the initial state
        self.update_grid()

        # Bind the arrow keys to the corresponding game moves
        self.master.bind("<Up>", self.move_up)
        self.master.bind("<Down>", self.move_down)
        self.master.bind("<Left>", self.move_left)
        self.master.bind("<Right>", self.move_right)
        #wasd keys
        self.master.bind("<w>", self.move_up)
        self.master.bind("<s>", self.move_down)
        self.master.bind("<a>", self.move_left)
        self.master.bind("<d>", self.move_right)
        
    def clear_screen(self):
        """Clear any existing widgets on the screen."""
        for widget in self.master.winfo_children():
            widget.destroy()

    def update_grid(self):
        """Update the visual grid based on the game matrix."""
        for i in range(4):
            for j in range(4):
                value = self.game_matrix[i][j]
                if value == 0:
                    self.cells[i][j].config(text="", bg=self.empty_color)
                else:
                    self.cells[i][j].config(text=str(value), bg=self.tile_colors.get(value, "#ff0000"))

    def move_up(self, event):
        self.game_matrix, changed = logic.move_up(self.game_matrix)
        self.perform_game_action(changed)

    def move_down(self, event):
        self.game_matrix, changed = logic.move_down(self.game_matrix)
        self.perform_game_action(changed)

    def move_left(self, event):
        self.game_matrix, changed = logic.move_left(self.game_matrix)
        self.perform_game_action(changed)

    def move_right(self, event):
        self.game_matrix, changed = logic.move_right(self.game_matrix)
        self.perform_game_action(changed)

    def perform_game_action(self, changed):
        """Perform the game action if the board has changed, check for game status."""
        if changed:
            logic.add_new_2(self.game_matrix)
            self.update_grid()
            state = logic.get_current_state(self.game_matrix)
            if state == 'WON':
                self.show_game_over("Congratulations!", "You won!")
            elif state == 'LOST':
                self.show_game_over("Game Over", "You lost!")

    def show_game_over(self, title, message):
        """Display a modern game over message."""
        game_over_window = tk.Toplevel(self.master)
        game_over_window.title(title)
        game_over_window.geometry("300x200")
        game_over_window.configure(bg="#faf8ef")

        tk.Label(game_over_window, text=title, font=("Helvetica", 24, "bold"), bg="#faf8ef").pack(pady=20)
        tk.Label(game_over_window, text=message, font=("Helvetica", 16), bg="#faf8ef").pack(pady=10)

        play_again_button = tk.Button(game_over_window, text="Play Again", font=("Helvetica", 14), command=lambda: [game_over_window.destroy(), self.start_game()])
        play_again_button.pack(pady=10)

        exit_button = tk.Button(game_over_window, text="Exit", font=("Helvetica", 14), command=self.master.quit)
        exit_button.pack(pady=10)

        game_over_window.transient(self.master)
        game_over_window.grab_set()
        game_over_window.wait_window()

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()

