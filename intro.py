import config
from tkinter import ttk


class Intro:
    def __init__(self, root, on_start):
        self.icon = config.Icon()
        self.root = root
        self.on_start = on_start
        self._create_screen()
    
    def _start_game(self, game):
        self.intro_board_frame.destroy()
        self.on_start(game)    

    def _create_screen(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Custom.TFrame", background="#1E1E1E")
        style.configure(
            "Title.TLabel",
            background="#1E1E1E",
            foreground="#FFFFFF",
            font=("Segoe UI", 22, "bold")
            )
        style.configure(
            "Icon.TLabel",
            background="#1E1E1E",
            foreground="#FFFFFF",
            font=("Segoe UI", 40)
            )
        style.configure(
            "Subtitle.TLabel",
            background="#1E1E1E",
            foreground="#AAAAAA",
            font=("Segoe UI", 11)
            )
        style.configure(
            "Game.TButton",
            font=("Segoe UI", 12, "bold"),
            padding=10,
            )
        style.configure(
            "Desc.TLabel",
            background="#1E1E1E",
            foreground="#888888",
            font=("Segoe UI", 9)
            )

        self.intro_board_frame = ttk.Frame(self.root, style="Custom.TFrame")
        self.intro_board_frame.pack(fill="both", expand=True)

        container = ttk.Frame(self.intro_board_frame, style="Custom.TFrame")
        container.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(container, text="💣", style="Icon.TLabel").pack(pady=(0, 5))

        ttk.Label(container, text="Buscaminas", style="Title.TLabel").pack()

        ttk.Label(
            container,
            text="Elige tu modo de juego",
            style="Subtitle.TLabel"
            ).pack(pady=(0, 20))

        options_frame = ttk.Frame(container, style="Custom.TFrame")
        options_frame.pack()

        classic_frame = ttk.Frame(options_frame, style="Custom.TFrame")
        classic_frame.grid(row=0, column=0, padx=20)

        ttk.Button(
            classic_frame,
            text="Clásico",
            image=self.icon.mine_icon,
            compound="left",
            style="Game.TButton",
            command=lambda: self._start_game("Clásico")
            ).pack()

        ttk.Label(
            classic_frame,
            text="El Buscaminas de toda la vida.\nEncuentra todas las minas.",
            style="Desc.TLabel",
            justify="center"
            ).pack(pady=(5, 0))

        minedroad_frame = ttk.Frame(options_frame, style="Custom.TFrame")
        minedroad_frame.grid(row=0, column=1, padx=20)

        ttk.Button(
            minedroad_frame,
            text="En Coche",
            image=self.icon.car_icon_up,
            compound="left",
            style="Game.TButton",
            command=lambda: self._start_game("En Coche")
            ).pack()

        ttk.Label(
            minedroad_frame,
            text="Conduce por el tablero esquivando minas.\nUna versión con un giro diferente.",
            style="Desc.TLabel",
            justify="center"
            ).pack(pady=(5, 0))