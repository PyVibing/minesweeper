import tkinter as tk
import classic, mined_road
import config, intro


relaunch = True # When going to main menu from the game, current App instance is destroyed and recreated again

class App:
    def __init__(self) -> None:
        self.options = config.Options()

        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.on_game_end("exit"))
        self.root.title(self.options.title)
        self.game = None
        self.intro = None
        self._center_window()
        self._configure_window()
        self.root.grid()

    def _center_window(self):
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.center_x = int(self.screen_width/2 - self.options.width / 2)
        self.center_y = int(self.screen_height/2 - self.options.height / 2)
        self.root.geometry(f"{self.options.width}x{self.options.height}+{self.center_x}+{self.center_y}")
    
    def _configure_window(self):
        self.root.resizable(False, False)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
    
    def launch_intro(self):
        self.intro = intro.Intro(self.root, self.start_new_game)

    def start_new_game(self, game_name) -> None:
        self._center_window()
        self._configure_window()
        if game_name == "Clásico":
            self.options.current_game = "Clásico"
            self.game = classic.Game(self.root, "Clásico", self.on_game_end, self.options)
        elif game_name == "En Coche":
            self.options.current_game = "En Coche"
            self.game = mined_road.Game(self.root, "En Coche", self.on_game_end, self.options)
    
    def on_game_end(self, option: str) -> None:
        """
        'option' posible values: 'restart', 'menu', 'exit'.
        """

        if option == "exit":
            global relaunch
            self.root.destroy()
            relaunch = False
        elif option == "restart":
            self.game.board.destroy()
            self.game = None
            self.start_new_game(self.options.current_game)
        elif option == "menu":
            self.root.destroy()
        else:
            raise Exception("Wrong value for argument 'option'")
    
    def run(self) -> None:
        self.launch_intro()
        self.root.mainloop()


if __name__ == "__main__":
    while relaunch:
        App().run()

    

