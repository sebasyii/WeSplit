from .base import BaseView
from tkinter import ttk
import tkinter as tk


class GroupView(BaseView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        BaseView.configure_grid(self, 12, 10)
        self.create_widgets()

    def create_widgets(self):
        self.back_button = ttk.Button(self, text="Back")
        self.add_expense_button = ttk.Button(self, text="Add Expense")
        self.edit_group_button = ttk.Button(self, text="Edit Group")

        self.back_button.grid(column=0, row=0, padx=20, pady=10, columnspan=4, sticky=tk.EW)
        self.add_expense_button.grid(column=4, row=0, padx=20, pady=10, columnspan=4, sticky=tk.EW)
        self.edit_group_button.grid(column=8, row=0, padx=20, pady=10, columnspan=4, sticky=tk.EW)

        self.member_tree = ttk.Treeview(self, columns=("owed_owe", "amount"))

        self.member_tree.column("#0", width=120, minwidth=25, anchor=tk.W)  # Name column
        self.member_tree.column("owed_owe", width=120, anchor=tk.CENTER)
        self.member_tree.column("amount", width=120, anchor=tk.E)

        self.member_tree.heading("#0", text="Name", anchor=tk.W)
        self.member_tree.heading("owed_owe", text="Owe", anchor=tk.CENTER)
        self.member_tree.heading("amount", text="Amount", anchor=tk.E)

        self.member_tree.grid(row=1, rowspan=11, column=0, columnspan=12, sticky="nsew", padx=20, pady=20)
