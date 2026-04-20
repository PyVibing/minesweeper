import tkinter as tk
import config


class Timer:
    def __init__(self, root, parent):
        color = config.Color()
        self.root = root
        self.parent = parent
        self.seconds = 0
        self.running = False
        self.label = tk.Label(parent, text="00:00", font=("Segoe UI", 20), bg=color.header_color, fg=color.header_text_color)
        self.label.pack()

    def start(self):
        if self.running == True:
            return
        
        self.running = True
        self.update_timer()
    
    def stop(self):
        self.running = False
    
    def update_timer(self):
        if not self.running:
            return
        
        self.seconds += 1
        minutes = self.seconds // 60
        secs = self.seconds % 60

        self.label.config(
            text=f"{minutes:02d}:{secs:02d}"
            )
        
        self.root.after(1000, self.update_timer)

