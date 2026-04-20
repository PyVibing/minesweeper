import tkinter as tk
import board
from typing import Callable
from config import Options


class Game:
    def __init__(self, root: tk.Tk, game_name: str, on_game_end: Callable, options: Options):
        self.board = board.Board(root, game_name, on_game_end, options)
        for button in self.board.buttons:
            button.bind("<ButtonPress-1>", self.on_press_left_click)
            button.bind("<ButtonRelease-1>", self.on_release_left_click)
            button.bind("<ButtonPress-2>", self.on_press_center_click)
            button.bind("<ButtonRelease-2>", self.on_release_center_click)
            button.bind("<ButtonPress-3>", self.on_press_right_click)
            button.bind("<ButtonRelease-3>", self.on_release_right_click)
            button.bind("<Leave>", self.on_leave)
    
    def left_click(self, event: tk.Event) -> None:
        button = event.widget
        
        is_flag = self.board.get_button_single_value(button, "is_flag")
        if is_flag:
            return
        
        self.board.reveal_button(button)
        
        is_mine = self.board.check_if_lose(button)
        if is_mine:
            self.board.lose_game()
            return
        
        self.board.reveal_buttons_around(button, True)
                    
        win = self.board.check_if_win()
        if win:
            self.board.win_game()
    
    def on_press_left_click(self, event: tk.Event) -> None:
        self.board.pressed_left_click = True
    
    def on_release_left_click(self, event: tk.Event) -> None:
        if self.board.pressed_left_click:
            self.left_click(event)

    def center_click(self, event: tk.Event) -> None:
        button = event.widget
        flags_count = self.board.get_flags_around(button)
        mines_around = self.board.get_mines_around(button)
        revealed_value = self.board.get_button_single_value(button, "is_revealed")
        
        if mines_around == flags_count and revealed_value:
            win = self.board.reveal_buttons_around(button, False)

            if win:
                self.board.win_game()
    
    def on_press_center_click(self, event: tk.Event) -> None:
        self.board.pressed_center_click = True
        button = event.widget
        neighbors = self.board.get_neighbors(button)
        self.board.highlight_neighbors(neighbors)
    
    def on_release_center_click(self, event: tk.Event) -> None:
        button = event.widget
        neighbors = self.board.get_neighbors(button)
        self.board.unhighlight_neighbors(neighbors)

        if self.board.pressed_center_click:
            self.center_click(event)

    def right_click(self, event: tk.Event) -> None:
        button = event.widget
        self.board.set_unset_flag(button)

        win = self.board.check_if_win()
        if win: 
            self.board.win_game()
    
    def on_press_right_click(self, event: tk.Event) -> None:
        self.board.pressed_right_click = True
    
    def on_release_right_click(self, event: tk.Event) -> None:
        if self.board.pressed_right_click:
            self.right_click(event)
    
    def on_leave(self, event: tk.Event) -> None:
        self.board.pressed_left_click = False
        self.board.pressed_right_click = False