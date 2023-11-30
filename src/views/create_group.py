from .base import BaseView
from tkinter import ttk
import tkinter as tk


class CreateGroupView(BaseView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        BaseView.configure_grid(self, 12, 10)
        self._create_widgets()

    def _create_widgets(self):
        self.back_btn = ttk.Button(self, text="Back")

        self.group_name_label = ttk.Label(self, text="Group Name")
        self.group_name_entry = ttk.Entry(self)

        self.group_description_label = ttk.Label(self, text="Group Description")
        self.group_description_entry = ttk.Entry(self)

        self.member_name_label = ttk.Label(self, text="Member Name")
        self.member_name_entry = ttk.Entry(self)
        self.add_member_btn = ttk.Button(self, text="Add Member")
        self.remove_member_btn = ttk.Button(self, text="Remove Member")

        self.list_of_members = tk.Listbox(self, height=10)
        self.create_group_btn = ttk.Button(self, text="Create Group")

        self.back_btn.grid(column=0, row=0, sticky=tk.W, padx=20, pady=10)
        self.group_name_label.grid(column=0, row=1, sticky=tk.W, padx=20, pady=10)
        self.group_name_entry.grid(column=1, row=1, sticky=tk.W, padx=20, pady=10)
        self.group_description_label.grid(column=0, row=2, sticky=tk.W, padx=20, pady=10)
        self.group_description_entry.grid(column=1, row=2, sticky=tk.W, padx=20, pady=10)
        self.member_name_label.grid(column=0, row=3, sticky=tk.W, padx=20, pady=10)
        self.member_name_entry.grid(column=1, row=3, sticky=tk.W, padx=20, pady=10)
        self.add_member_btn.grid(column=2, columnspan=2, row=3, sticky=tk.EW, padx=10, pady=10)
        self.remove_member_btn.grid(column=4, columnspan=2, row=3, sticky=tk.EW, padx=10, pady=10)
        self.list_of_members.grid(column=0, row=4, columnspan=12, rowspan=5, sticky=tk.NSEW, padx=20, pady=10)
        self.create_group_btn.grid(column=9, row=9, columnspan=2, sticky=tk.NSEW, padx=20, pady=10)
