import tkinter as tk

from frames.create_group_frame import CreateGroupFrame
from frames.expense_frame import ExpenseFrame
from frames.mainframe import MainFrame

from frames.group_frame import GroupFrame


class App(tk.Tk):
    def __init__(self, title, size, groups):
        super().__init__()
        self.title(title)
        self.geometry(f"{size[0]}x{size[1]}")
        self.resizable(False, False)
        self.minsize(size[0], size[1])
        
        self.groups = groups

        self.setup_frames(self.groups)
        self.initialize_frame_references()

        self.mainloop()

    def setup_frames(self, groups):
        """Setup and initialize all frames."""
        self.expense_frame = ExpenseFrame(self)
        self.group_frame = GroupFrame(self, self.expense_frame)
        self.create_grp_frame = CreateGroupFrame(self, groups, self.group_frame)
        self.mainframe = MainFrame(self, groups, self.create_grp_frame, self.group_frame)

        self.mainframe.tkraise()  # Raise the main frame to the top

    def initialize_frame_references(self):
        """Set references between frames after all are created."""
        self.group_frame.set_create_grp_frame(self.create_grp_frame)
        self.create_grp_frame.set_group_frame(self.group_frame)