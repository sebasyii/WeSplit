import tkinter as tk
from tkinter import ttk

class App(tk.Tk):
    def __init__(self, title, size, groups):
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.minsize(size[0], size[1])

        # Widgets
        self.mainframe = MainFrame(self, groups)

        self.mainloop()

class MainFrame(ttk.Frame):
    def __init__(self, parent, groups):
        super().__init__(parent)
        self.groups = groups
        self.place(relwidth=1, relheight=1)

        self.create_widgets()

    def create_widgets(self):
        # Create Group button
        create_grp_btn = ttk.Button(self, text="Create Group")

        var = tk.Variable(value=self.groups)

        # Create Group List
        group_list = tk.Listbox(self, listvariable=var, height=5)

        # Create Grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)

        # Place widgets
        create_grp_btn.grid(column=0, row=0, sticky=tk.W, padx=5, pady=10)
        group_list.grid(column=0, row=1, columnspan=4, sticky=tk.NSEW, padx=5, pady=10)

class CreateGroupFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relwidth=1, relheight=1)

        self.create_widgets()

    def create_widgets(self):
        pass

class HistoryFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relwidth=1, relheight=1)

        self.create_widgets()

    def create_widgets(self):
        pass

class GroupFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relwidth=1, relheight=1)

        self.create_widgets()

    def create_widgets(self):
        pass

class ExpenseFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relwidth=1, relheight=1)

        self.create_widgets()

    def create_widgets(self):
        pass