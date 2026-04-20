from PIL import Image, ImageTk


class Color:
    def __init__(self):
        self.header_color = "#022E0B"
        self.header_text_color = "#FFFFFF"
        self.dark_active_color = "#049209"
        self.light_active_color = "#65B967"
        self.dark_inactive_color = "#DBDBDB"
        self.light_inactive_color = "#EEEEEE"
        self.mouse_hover_color = "#196328"
        self.revealed_color = "#ACBDAC"
        self.highlight_neighbors_dark_color = "#F1B9B9"
        self.highlight_neighbors_light_color = "#FCE9E9"
        self.mines_count_color_1 = "#00070A"
        self.mines_count_color_2 = "#07910D"
        self.mines_count_color_3 = "#166DFA"
        self.mines_count_color_4 = "#7116FA"
        self.mines_count_color_5 = "#C7B600"
        self.mines_count_color_6 = "#B17000"
        self.mines_count_color_7 = "#BB3E00"
        self.mines_count_color_8 = "#A10000"
    
class Icon:
    def __init__(self):
        FLAG_ICON_PATH = "assets/flag.png"
        FLAG_ICON = Image.open(FLAG_ICON_PATH)
        FLAG_ICON = FLAG_ICON.resize((50, 50))

        MINE_ICON_PATH = "assets/mine.png"
        MINE_ICON = Image.open(MINE_ICON_PATH)
        MINE_ICON = MINE_ICON.resize((40, 40))

        CAR_ICON_PATH = "assets/car.png"
        CAR_ICON = Image.open(CAR_ICON_PATH)
        CAR_ICON = CAR_ICON.resize((40, 40))
        CAR_ICON_UP = CAR_ICON
        CAR_ICON_RIGHT = CAR_ICON.rotate(270)
        CAR_ICON_DOWN = CAR_ICON.rotate(180)
        CAR_ICON_LEFT = CAR_ICON.rotate(90)
        CAR_ICON_LEFT_DOWN = CAR_ICON.rotate(135)
        CAR_ICON_LEFT_UP = CAR_ICON.rotate(45)
        CAR_ICON_RIGHT_DOWN = CAR_ICON.rotate(225)
        CAR_ICON_RIGHT_UP = CAR_ICON.rotate(315)

        self.flag_icon = ImageTk.PhotoImage(FLAG_ICON)

        self.mine_icon = ImageTk.PhotoImage(MINE_ICON)

        self.car_icon_up = ImageTk.PhotoImage(CAR_ICON_UP)
        self.car_icon_right_up = ImageTk.PhotoImage(CAR_ICON_RIGHT_UP)
        self.car_icon_right = ImageTk.PhotoImage(CAR_ICON_RIGHT)
        self.car_icon_right_down = ImageTk.PhotoImage(CAR_ICON_RIGHT_DOWN)
        self.car_icon_down = ImageTk.PhotoImage(CAR_ICON_DOWN)
        self.car_icon_left_down = ImageTk.PhotoImage(CAR_ICON_LEFT_DOWN)
        self.car_icon_left = ImageTk.PhotoImage(CAR_ICON_LEFT)
        self.car_icon_left_up = ImageTk.PhotoImage(CAR_ICON_LEFT_UP)

class Options:
    def __init__(self):
        self.current_game = ""
        self.selected_level = "Normal" # By default
        self._design_map = {
            "Fácil": {"rows": 8, "columns": 8, "mines": 8, "width": 400, "height": 400, "index": 0},
            "Normal": {"rows": 12, "columns": 12, "mines": 18, "width": 500, "height": 500, "index": 1},
            "Difícil": {"rows": 18, "columns": 18, "mines": 40, "width": 700, "height": 700, "index": 2}
            }
        self.title = "Buscaminas"
    
    @property
    def level_index(self):
        return self._design_map.get(self.selected_level).get("index")
    
    @property
    def rows(self):
        return self._design_map.get(self.selected_level).get("rows")
    
    @property
    def columns(self):
        return self._design_map.get(self.selected_level).get("columns")
    
    @property
    def mines(self):
        return self._design_map.get(self.selected_level).get("mines")
    
    @property
    def width(self):
        return self._design_map.get(self.selected_level).get("width")
    
    @property
    def height(self):
        return self._design_map.get(self.selected_level).get("height")
    
   


