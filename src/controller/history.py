from decimal import ROUND_DOWN, ROUND_UP, Decimal
from tkinter import BooleanVar, messagebox, ttk
from typing import Optional
from views.main import View
from models.main import Model
from models.expense import Expense
from models.user import User


class HistoryController:
    def __init__(self, model: Model, view: View):
        self.view = view
        self.model = model
        self.frame = self.view.frames["history"]

        self._setup_event_bindings()

    def _setup_event_bindings(self) -> None:
        self.frame.back_button.config(command=self._go_back)

    def _go_back(self) -> None:
        # self.model.trigger_event("page_loaded")
        self.view.switch("group")

    def _update_history_table(self) -> None:
        self.frame.history_table.delete(*self.frame.history_table.get_children())

        for expense in self.model.current_group.expenses:
            parent_id = self.frame.history_table.insert("", "end", text=expense.paid_by.name, values=("", expense.amount, expense.description, expense.category))

            for user, amount in expense.split_details.items():
                self.frame.history_table.insert(parent_id, "end", text=user.name, values=(amount, ""))

    def update_view(self) -> None:
        self._update_history_table()