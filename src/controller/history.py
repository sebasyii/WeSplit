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