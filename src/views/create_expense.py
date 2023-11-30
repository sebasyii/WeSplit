from tkinter import Frame, ttk
from .base import BaseView


class CreateExpenseView(BaseView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        BaseView.configure_grid(self, 12, 10)
        self._create_widgets()

    def _create_widgets(self):
        self.back_button = ttk.Button(self, text="Back")
        self.back_button.grid(row=0, column=0, sticky="ew", padx=20, pady=10)

        self.amount_label = ttk.Label(self, text="Amount")
        self.amount_entry = ttk.Entry(self)

        self.amount_label.grid(row=1, column=0, sticky="ew", padx=20, pady=1)
        self.amount_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=20, pady=1)

        self.description_label = ttk.Label(self, text="Description")
        self.description_entry = ttk.Entry(self)

        self.description_label.grid(row=2, column=0, sticky="ew", padx=20, pady=1)
        self.description_entry.grid(row=2, column=1, columnspan=2, sticky="ew", padx=20, pady=1)

        self.split_type_label = ttk.Label(self, text="Split Type")
        self.split_type_label.grid(row=3, column=0, sticky="ew", padx=20, pady=1)
        self.split_type_combobox = ttk.Combobox(self, state="readonly")
        self.split_type_combobox["values"] = ("Equal", "Exact Amounts", "Percentages")
        self.split_type_combobox.grid(row=3, column=1, sticky="ew", padx=20, pady=1)
        self.split_type_combobox.current(0)  # Set the default value to 'Equal'

        self.paid_by_label = ttk.Label(self, text="Paid By")
        self.paid_by_label.grid(row=4, column=0, sticky="ew", padx=20, pady=1)
        self.paid_by_combobox = ttk.Combobox(self, state="readonly")
        self.paid_by_combobox.grid(row=4, column=1, sticky="ew", padx=20, pady=1)

        self.members_split_entries_container = Frame(self)
        self.members_split_entries_container.grid(
            row=5, rowspan=9, column=1, columnspan=5, sticky="nsew", padx=20, pady=10
        )

        BaseView.configure_grid(self.members_split_entries_container, 12, 10)

        self.record_expense_button = ttk.Button(self, text="Record Expense")
        self.record_expense_button.grid(row=10, column=11, sticky="ew", padx=20, pady=20)
