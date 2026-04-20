import random
import tkinter as tk
import config, timer
from typing import Callable
from tkinter import ttk
from config import Options


class Board:
    def __init__(self, root: tk.Tk, game_name: str, on_game_end: Callable, options: Options):
        self.color = config.Color()
        self.icon = config.Icon()
        self.options = options
        
        self.root = root
        self.game_board_frame = tk.Frame(root)
        self.game_name = game_name
        self.on_game_end = on_game_end
        
        self.header_frame = tk.Frame(self.game_board_frame, height=70, bg=self.color.header_color)
        self.game_frame = tk.Frame(self.game_board_frame)

        # For game_frame
        self.cells = self._create_button_cells(self.options.rows, self.options.columns)
        self.buttons = [values["button"] for _, values in self.cells.items()]
        self._set_neighbors()
        self._create_mines()
        self._calculate_mines_around()
        
        for r in range(self.options.rows):
            self.game_frame.rowconfigure(r+1, weight=1)

        for c in range(self.options.columns):
            self.game_frame.columnconfigure(c+1, weight=1)

        # For header_frame
        self._create_header_elements()
        
        self.header_frame.pack(side="top", fill="x")
        self.header_frame.pack_propagate(False)
        self.game_frame.pack(side="top", fill="both", expand=True)
        self.game_board_frame.pack(side="top", fill="both", expand=True)

    # -------------- RESOURCES CREATION --------------
    def _create_header_elements(self) -> None:
        container_left = tk.Frame(self.header_frame)
        container_left.pack(side="left", expand=True)
        container_center = tk.Frame(self.header_frame)
        container_center.pack(side="left", expand=True)
        container_right = tk.Frame(self.header_frame)
        container_right.pack(side="left", expand=True)

        self.difficulty_var = tk.StringVar()
        combo = ttk.Combobox(
            container_left,
            textvariable=self.difficulty_var,
            values=["Fácil", "Normal", "Difícil"],
            state="readonly",
            width=15
        )
        combo.grid(row=0, column=0)
        combo.current(self.options.level_index)
        combo.bind("<<ComboboxSelected>>", self.on_level_change)

        label_icon_remaining_flags = tk.Label(container_center, image=self.icon.flag_icon, bg=self.color.header_color)
        label_icon_remaining_flags.grid(row=0, column=0, sticky="nsew")

        self.label_number_remaining_flags = tk.Label(container_center, text=self.options.mines, bg=self.color.header_color, 
                                                fg=self.color.header_text_color, font=("Arial", 20, "bold"))
        self.label_number_remaining_flags.grid(row=0, column=1, sticky="nsew")

        self.timer = timer.Timer(self.root, container_right)        

    def _create_button_cells(self, rows: int, columns: int) -> dict:
        cells = {}
        dark_color = self.color.dark_active_color
        light_color = self.color.light_active_color
        for row in range(1, rows+1):            
            for column in range(1, columns+1):
                button = tk.Button(self.game_frame, borderwidth=0, highlightthickness=0, 
                                   activebackground=self.color.mouse_hover_color, width=2, height=1,
                                   font=("Arial", 14, "bold"))

                if column % 2 != 0:
                    button["bg"] = dark_color                    
                    button.color_alt = "dark" if dark_color == self.color.dark_active_color else "light"
                else:
                    button["bg"] = light_color
                    button.color_alt = "light" if light_color == self.color.light_active_color else "dark"

                button.row = row
                button.column = column
                cells[(row,column)] = {"button": button,
                                       "is_mine": False,
                                       "is_flag": False,
                                       "is_revealed": False,
                                       }
                button.grid(row=row, column=column, sticky="nsew")
            light_color, dark_color = dark_color, light_color
        
        return cells
    
    def _create_mines(self):
        mines_set = 0
        while mines_set < self.options.mines:
            mine_coord = random.choice(list(self.cells.keys()))
            button = self.get_button(mine_coord)
            currently_is_mine = self.get_button_single_value(button, "is_mine")
            if not currently_is_mine:
                set_ok = self._set_hidden_mine(button)
                if set_ok:
                    mines_set += 1

    def _create_topup(self, icon_text, title_text, subtitle_text):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.TFrame", background="#1E1E1E")

        style.configure(
            "Title.TLabel",
            background="#1E1E1E",
            foreground="#FFFFFF",
            font=("Segoe UI", 14, "bold")
        )

        style.configure(
            "Icon.TLabel",
            background="#1E1E1E",
            foreground="#FFFFFF",
            font=("Segoe UI", 30, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            background="#1E1E1E",
            foreground="#CCCCCC",
            font=("Segoe UI", 10)
        )

        style.configure(
            "Primary.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=2
        )

        style.configure(
            "Secondary.TButton",
            font=("Segoe UI", 10),
            padding=2
        )

        top_level_width = 500
        top_level_height = 250

        dialog = tk.Toplevel(self.game_board_frame)
        dialog.title("")
        dialog.resizable(False, False)
        dialog.transient(self.game_board_frame)
        dialog.grab_set()
        dialog.protocol("WM_DELETE_WINDOW", lambda: None)

        frame = ttk.Frame(dialog, style="Custom.TFrame", padding=25)
        frame.pack(fill="both", expand=True)

        icon = ttk.Label(
            frame,
            text=icon_text,
            style="Icon.TLabel",
            anchor="center"
        )
        icon.pack(pady=(0, 10))

        title = ttk.Label(
            frame,
            text=title_text,
            style="Title.TLabel",
            anchor="center"
        )
        title.pack()

        subtitle = ttk.Label(
            frame,
            text=subtitle_text,
            style="Subtitle.TLabel",
            anchor="center",
            justify="center"
        )
        subtitle.pack(pady=(10, 20))

        buttons_frame = ttk.Frame(frame, style="Custom.TFrame")
        buttons_frame.pack()

        restart_btn = ttk.Button(
            buttons_frame,
            text="Nueva partida",
            style="Primary.TButton",
            command=self.new_game
        )
        restart_btn.pack(side="left", padx=5)

        different_game = ttk.Button(
            buttons_frame,
            text="Menú principal",
            style="Primary.TButton",
            command=self.different_game
        )
        different_game.pack(side="left", padx=5)

        close_btn = ttk.Button(
            buttons_frame,
            text="Cerrar",
            style="Secondary.TButton",
            command=self.exit_game
        )
        close_btn.pack(side="left", padx=5)

        self.root.update_idletasks()

        w = top_level_width
        h = top_level_height

        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (w // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (h // 2)

        dialog.geometry(f"{w}x{h}+{x}+{y}")
    # -------------- RESOURCES CREATION END ----------
    
    # -------------- VISUAL BUTTON CHANGES ---------------
    def highlight_neighbors(self, neighbors):
        for _, coords in neighbors.items():
            if not coords:
                continue
            neighbor_button = self.get_button(coords)
            revealed_value = self.get_button_single_value(neighbor_button, "is_revealed")
            dark_or_light = neighbor_button.color_alt

            if not revealed_value:
                if dark_or_light == "dark":
                    self.set_button_values(neighbor_button, {"last_color": self.color.dark_active_color})
                    neighbor_button["bg"] = self.color.highlight_neighbors_dark_color
                else:
                    self.set_button_values(neighbor_button, {"last_color": self.color.light_active_color})
                    neighbor_button["bg"] = self.color.highlight_neighbors_light_color
            else:
                if dark_or_light == "dark":
                    self.set_button_values(neighbor_button, {"last_color": self.color.dark_inactive_color})
                    neighbor_button["bg"] = self.color.highlight_neighbors_dark_color
                else:
                    self.set_button_values(neighbor_button, {"last_color": self.color.light_inactive_color})
                    neighbor_button["bg"] = self.color.highlight_neighbors_light_color
    
    def unhighlight_neighbors(self, neighbors):
        for _, coords in neighbors.items():
            if not coords:
                continue
            
            neighbor_button = self.get_button(coords)
            last_color = self.get_button_single_value(neighbor_button, "last_color")
            neighbor_button.config(bg = last_color)

    def set_unset_flag(self, button: tk.Button) -> None:
        self.timer.start()
        flag_value = self.get_button_single_value(button, "is_flag")
        revealed_value = self.get_button_single_value(button, "is_revealed")
        current_remaining_flags = int(self.label_number_remaining_flags["text"])

        if not flag_value and not revealed_value:
            if not current_remaining_flags:
                return
            button["image"] = self.icon.flag_icon
            self.label_number_remaining_flags["text"] = current_remaining_flags - 1
        elif flag_value:
            button["image"] = ""
            self.label_number_remaining_flags["text"] = current_remaining_flags + 1            
        else:
            return
            
        self.set_button_values(button, {"is_flag": not flag_value})
    
    
    def disable_button(self, button: tk.Button) -> None:
        color_alt = button.color_alt
        button["bg"] = self.color.dark_inactive_color if color_alt == "dark" else self.color.light_inactive_color
        button["activebackground"] = self.color.dark_inactive_color if color_alt == "dark" else self.color.light_inactive_color      
        
    def reveal_button(self, button: tk.Button, reveal_number_around:bool = True, timer:bool = True) -> None:
        if timer:
            self.timer.start()

        flag_value = self.get_button_single_value(button, "is_flag")
        mine_value = self.get_button_single_value(button, "is_mine")
        mines_around = self.get_mines_around(button)
        
        if flag_value:
            return
        
        self.disable_button(button)
        self.set_button_values(button, {"is_revealed": True})
        
        if mine_value:
            button["image"] = self.icon.mine_icon # Later it is checked if win or lose
        else:
            if self.game_name == "Clásico":           
                button["text"] = mines_around if mines_around else ""
                # Colored numbers
                if mines_around == 1:
                    button.config(fg=self.color.mines_count_color_1,
                                    activeforeground=self.color.mines_count_color_1)
                elif mines_around == 2:
                    button.config(fg=self.color.mines_count_color_2,
                                    activeforeground=self.color.mines_count_color_2)
                elif mines_around == 3:
                    button.config(fg=self.color.mines_count_color_3,
                                    activeforeground=self.color.mines_count_color_3)
                elif mines_around == 4:
                    button.config(fg=self.color.mines_count_color_4,
                                    activeforeground=self.color.mines_count_color_4)
                elif mines_around == 5:
                    button.config(fg=self.color.mines_count_color_5,
                                    activeforeground=self.color.mines_count_color_5)
                elif mines_around == 6:
                    button.config(fg=self.color.mines_count_color_6,
                                    activeforeground=self.color.mines_count_color_6)
                elif mines_around == 7:
                    button.config(fg=self.color.mines_count_color_7,
                                    activeforeground=self.color.mines_count_color_7)
                elif mines_around == 8:
                    button.config(fg=self.color.mines_count_color_8,
                                    activeforeground=self.color.mines_count_color_8)
            elif self.game_name == "En Coche" and reveal_number_around:
                button.config(
                    fg="white",
                    text=mines_around,
                    compound="center"
                    )
    
    def reveal_buttons_around(self, start_button: tk.Button, safe: bool, only_next_ones:bool = False) -> bool:
        """Returns True if game is won, False if it has not been confirmed the win"""
        queue = []
        neighbors = self.get_neighbors(start_button)
        mines_around = self.get_mines_around(start_button)
        if mines_around and safe: # To avoid losing the game when left-clicking and revealing neighbors
            return False
        
        def append_neighbors_coords(neighbors):
            for neighbor_coords in neighbors.values():
                neighbor_button = self.get_button(neighbor_coords) if neighbor_coords else None
                neighbor_is_flag = self.get_button_single_value(neighbor_button, "is_flag") if neighbor_button else None
                if neighbor_coords and not neighbor_is_flag:
                    queue.append(neighbor_coords)

        append_neighbors_coords(neighbors)

        win = False
        while queue:
            coords = queue.pop()
            current_button = self.get_button(coords)

            if self.get_button_single_value(current_button, "is_revealed"):
                continue

            if self.game_name == "En Coche":
                self.reveal_button(current_button, reveal_number_around=False)
            else:
                self.reveal_button(current_button)
            
            if not safe:
                current_is_mine = self.get_button_single_value(current_button, "is_mine")
                current_is_flag = self.get_button_single_value(current_button, "is_flag")
                if current_is_mine and not current_is_flag:
                    self.lose_game() # Quitar if current_is_mine... y poner if self.check_if_lose
                    return
            
            self.check_win_or_lose(current_button)

            mines_around = self.get_mines_around(current_button)
            if mines_around == 0 and not only_next_ones:
                neighbors = self.get_neighbors(current_button)
                append_neighbors_coords(neighbors)
        
        return win
    
    def _set_hidden_mine(self, button: tk.Button) -> bool:
        mine_value = self.get_button_single_value(button, "is_mine")
        if not mine_value:
            self.set_button_values(button, {"is_mine": True})
            return True
        return False
    # -------------- VISUAL BUTTON CHANGES END -----------

    # ------------ GET AND SET BUTTON VALUES -------------
    def on_level_change(self, event):
        self.options.selected_level = self.difficulty_var.get()
        self.new_game()

    def deactivate_all_buttons(self):
        for button in self.buttons:
            button["state"] = "disabled"
        
    def get_button(self, coords: tuple) -> tk.Button:
        return self.cells[coords]["button"]

    def get_button_values(self, button: tk.Button) -> tuple:
        coords = (button.row, button.column)        
        values = self.cells[coords]
        return (coords, values)
    
    def get_button_single_value(self, button: tk.Button, key: str) -> str | bool:
        coords = (button.row, button.column)        
        values = self.cells[coords]
        return values.get(key)
    
    def set_button_values(self, button: tk.Button, values: dict) -> None:
        coords = (button.row, button.column)
        for key, value in values.items():
            self.cells[coords][key] = value

    def get_neighbors(self, button: tk.Button) -> dict:
        """Returns a dict like: 
        {1: (4, 2), 2: (4, 3), 3: (4, 4), 4: (5, 2), 6: (5, 4), 7: (6, 2), 8: (6, 3), 9: (6, 4)}
        The keys refers to the relative position to the current button. Position 5 does not exists, 
        since it is the current position. The values could be None.
        """        
        return self.get_button_single_value(button, "neighbors")

    def _set_neighbors(self) -> None:
        for button in self.buttons:
            coords, _ = self.get_button_values(button)
            button_row, button_col = coords
            
            directions = {
            7: (-1, -1),
            8: (-1, 0),
            9: (-1, 1),
            4: (0, -1),
            6: (0, 1),
            1: (1, -1),
            2: (1, 0),
            3: (1, 1),
            }

            neighbors = {}

            for position, (dir_row, dir_col) in directions.items():
                new_row, new_col = button_row + dir_row, button_col + dir_col

                if 1 <= new_row <= self.options.rows and 1 <= new_col <= self.options.columns:
                    neighbors[position] = (new_row, new_col)
                else:
                    neighbors[position] = None
            
            self.set_button_values(button, {"neighbors": neighbors})
    
    def _calculate_mines_around(self) -> None:
        for button in self.buttons:
            neighbors = self.get_neighbors(button)

            mine_count = 0
            for neighbor_coord in neighbors.values():
                if not neighbor_coord:
                    continue

                neighbor_button = self.get_button(neighbor_coord)                
                neighbor_is_mine = self.get_button_single_value(neighbor_button, "is_mine")
                if neighbor_is_mine:
                    mine_count += 1
            self.set_button_values(button, {"mines_around": mine_count})
    
    def get_mines_around(self, button: tk.Button) -> int:
        return self.get_button_single_value(button, "mines_around")
    
    def get_flags_around(self, button: tk.Button) -> int:
        neighbors = self.get_neighbors(button)
        
        flag_count = 0
        for _, coords in neighbors.items():
            if not coords:
                continue
            neighbor_button = self.get_button(coords)
            if self.get_button_single_value(neighbor_button, "is_flag"):
                flag_count += 1
        
        return flag_count
    # ------------ GET AND SET BUTTON VALUES END ---------

    # ---------------------- CHECKERS --------------------
    def check_if_lose(self, button: tk.Button) -> bool:        
        is_mine = self.get_button_single_value(button, "is_mine")
        is_flag = self.get_button_single_value(button, "is_flag")
        if is_mine and not is_flag:
            return True
        return False
    
    def check_any_neighbor_is_mine(self,button: tk.Button) -> bool:
        neighbors = self.get_neighbors(button)
        neighbors_coords = [coords for _, coords in neighbors.items() if coords]
        for coords in neighbors_coords:
            neighbor_button = self.get_button(coords)
            neighbor_is_mine = self.get_button_single_value(neighbor_button, "is_mine")
            neighbor_is_flag = self.get_button_single_value(neighbor_button, "is_flag")
            if neighbor_is_mine and not neighbor_is_flag:
                return True
        return False
    
    def check_if_win(self) -> None:
        revealed_buttons = [button for button in self.buttons if self.get_button_single_value(button, "is_revealed")]
        remaining_buttons = len(self.buttons) - len(revealed_buttons)
        
        flags_buttons = [button for button in self.buttons if self.get_button_single_value(button, "is_flag")]

        if remaining_buttons - len(flags_buttons) == 0 and len(flags_buttons) - self.options.mines == 0:            
            return True
        return False
    
    def check_win_or_lose(self, button: tk.Button) -> None:
        win = self.check_if_win()
        if win:
            self.win_game()
            return
        lose = self.check_if_lose(button)
        if lose:
            self.lose_game()
            return
    # -------------------- CHECKERS END ------------------

    # ------------------------- GAME ---------------------
    def exit_game(self):
        self.on_game_end("exit")
    
    def new_game(self):
        self.on_game_end("restart")

    def different_game(self):
        self.on_game_end("menu")

    def win_game(self):
        self.deactivate_all_buttons()
        self.timer.stop()
        self._create_topup("🎉", "¡FELICIDADES, SOBREVIVISTE!", "Has ganado la partida\n¿Qué quieres hacer ahora?")
        
    def lose_game(self):
        self.deactivate_all_buttons()
        self.timer.stop()
        self._create_topup("🧨", "¡REVENTASTE EN MIL PEDAZOS!", "Has perdido la partida\n¿Qué quieres hacer ahora?")

    def destroy(self):
        self.game_board_frame.destroy() 
    # ---------------------- GAME END -------------------
    

