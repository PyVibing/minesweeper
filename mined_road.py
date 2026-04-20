import random
import tkinter as tk
import board
from typing import Callable
from config import Options


class Game:
    def __init__(self, root: tk.Tk, game_name: str, on_game_end: Callable, options: Options):
        self.board = board.Board(root, game_name, on_game_end, options)
        self.root = root
        self.root.bind("<KP_0>", self.reveal_neighbors)
        self.root.bind("<KP_1>", self.move_to_pos_1)
        self.root.bind("<KP_2>", self.move_to_pos_2)
        self.root.bind("<KP_3>", self.move_to_pos_3)
        self.root.bind("<KP_4>", self.move_to_pos_4)
        self.root.bind("<KP_5>", self.start_set_a_flag)
        self.root.bind("<KP_6>", self.move_to_pos_6)
        self.root.bind("<KP_7>", self.move_to_pos_7)
        self.root.bind("<KP_8>", self.move_to_pos_8)
        self.root.bind("<KP_9>", self.move_to_pos_9)
        self.root.focus_set()

        self.set_a_flag = False
        self.neighbors_highlighted = False
        self.current_button = self.define_starting_button()
        self.board.reveal_button(self.current_button, timer=False)
    
    # --------------------- INITIAL CONFIG ----------------------
    def define_starting_button(self) -> tk.Button:
        starting_button = None
        while not starting_button:
            button = random.choice(self.board.buttons)
            is_mine = self.board.get_button_single_value(button, "is_mine")
            if not is_mine:
                starting_button = button
        self.board.set_button_values(starting_button, {"is_car": True})

        starting_button["image"] = self.board.icon.car_icon_up

        return starting_button
    # ------------------- INITIAL CONFIG END --------------------

    def reveal_neighbors(self, event):
        mines_around = self.board.get_mines_around(self.current_button)
        flags_around = self.board.get_flags_around(self.current_button)
        if mines_around != flags_around or self.neighbors_highlighted:
            return
        self.board.reveal_buttons_around(self.current_button, False, only_next_ones=True)

    def move_to_pos_1(self, event):
        self.move_to_coord(1)
        self.board.check_win_or_lose(self.current_button)

    def move_to_pos_2(self, event):
        self.move_to_coord(2)
        self.board.check_win_or_lose(self.current_button)
    
    def move_to_pos_3(self, event):
        self.move_to_coord(3)
        self.board.check_win_or_lose(self.current_button)

    def move_to_pos_4(self, event):
        self.move_to_coord(4)
        self.board.check_win_or_lose(self.current_button)
    
    def start_set_a_flag(self, event):
        neighbors = self.board.get_neighbors(self.current_button)
        
        if not self.neighbors_highlighted:
            self.board.highlight_neighbors(neighbors)
            self.neighbors_highlighted = True
        else:
            self.board.unhighlight_neighbors(neighbors)
            self.neighbors_highlighted = False

        self.set_a_flag = not self.set_a_flag
        self.board.check_win_or_lose(self.current_button)
        

    def move_to_pos_6(self, event):
        self.move_to_coord(6)
        self.board.check_win_or_lose(self.current_button)

    def move_to_pos_7(self, event):
        self.move_to_coord(7)
        self.board.check_win_or_lose(self.current_button)

    def move_to_pos_8(self, event):
        self.move_to_coord(8)
        self.board.check_win_or_lose(self.current_button)

    def move_to_pos_9(self, event):
        self.move_to_coord(9)
        self.board.check_win_or_lose(self.current_button)
    
    def move_to_coord(self, key):
        target_coords = self.board.get_neighbors(self.current_button).get(key)
        if not target_coords:
            return
        target_button = self.board.get_button(target_coords)

        if self.set_a_flag:
            self.board.set_unset_flag(target_button)
            return
        
        self.board.set_button_values(self.current_button, {"is_car": False})
        self.current_button["image"] = ""
        previous_button = self.current_button
        self.current_button = target_button
        if key == 1:
            self.current_button["image"] = self.board.icon.car_icon_left_down
        elif key == 2:
            self.current_button["image"] = self.board.icon.car_icon_down
        elif key == 3:
            self.current_button["image"] = self.board.icon.car_icon_right_down
        elif key == 4:
            self.current_button["image"] = self.board.icon.car_icon_left
        elif key == 6:
            self.current_button["image"] = self.board.icon.car_icon_right
        elif key == 7:
            self.current_button["image"] = self.board.icon.car_icon_left_up
        elif key == 8:
            self.current_button["image"] = self.board.icon.car_icon_up
        elif key == 9:
            self.current_button["image"] = self.board.icon.car_icon_right_up
        
        self.board.set_button_values(self.current_button, {"is_car": True})
        self.board.reveal_button(target_button)
        previous_button.config(text="")
        previous_button_is_flag = self.board.get_button_single_value(previous_button, "is_flag")
        previous_button["image"] = self.board.icon.flag_icon if previous_button_is_flag else ""
    