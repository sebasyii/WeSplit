from tkinter import Frame, ttk
import tkinter as tk
from .base import BaseView


class HomeView(BaseView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        BaseView.configure_grid(self, 12, 10)
        self._create_widgets()

    def _create_widgets(self):
        self.create_grp_btn = ttk.Button(self, text="Create Group")
        self.select_grp_btn = ttk.Button(self, text="Select Group", state=tk.DISABLED)
        self.leave_grp_btn = ttk.Button(self, text="Leave Group", state=tk.DISABLED)

        var = tk.Variable(value=[])
        self.groups_listbox = tk.Listbox(self, listvariable=var, height=5)

        self.create_grp_btn.grid(column=0, columnspan=6, row=0, sticky=tk.NSEW, padx=20)
        self.select_grp_btn.grid(column=0, columnspan=6, row=1, sticky=tk.NSEW, padx=20)
        self.leave_grp_btn.grid(column=6, columnspan=6, row=1, sticky=tk.NSEW, padx=20)

        self.groups_listbox.grid(column=0, columnspan=12, row=2, rowspan=8, sticky=tk.NSEW, padx=20, pady=20)
