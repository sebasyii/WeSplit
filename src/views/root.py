import tkinter as tk


class App(tk.Tk):
    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.resizable(False, False)
        self.minsize(size[0], size[1])

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
