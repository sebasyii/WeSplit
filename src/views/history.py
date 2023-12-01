from .base import BaseView
from tkinter import ttk
import tkinter as tk


class HistoryView(BaseView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        BaseView.configure_grid(self, 12, 10)
        self._create_widgets()

    def _create_widgets(self):
        self.back_button = ttk.Button(self, text="Back")

        self.back_button.grid(column=0, row=0, padx=20, pady=10, columnspan=2, sticky=tk.EW)

        self.history_table = ttk.Treeview(self, columns=("amount", "total_amount", "description", "category"))

        self.history_table.column("#0", minwidth=25, width=60, anchor=tk.CENTER)
        self.history_table.column("amount", width=60, anchor=tk.CENTER)
        self.history_table.column("total_amount", width=60, anchor=tk.CENTER)
        self.history_table.column("description", width=120, anchor=tk.CENTER)
        self.history_table.column("category", width=100, anchor=tk.CENTER)

        self.history_table.heading("#0", text="Paid By", anchor=tk.CENTER)
        self.history_table.heading("amount", text="Amount", anchor=tk.CENTER)
        self.history_table.heading("total_amount", text="Total Amount", anchor=tk.CENTER)
        self.history_table.heading("description", text="Description", anchor=tk.CENTER)
        self.history_table.heading("category", text="Category", anchor=tk.CENTER)

        self.history_table.grid(row=2, rowspan=10, column=0, columnspan=12, sticky="nsew", padx=20, pady=20)
