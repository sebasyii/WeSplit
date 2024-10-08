from tkinter import filedialog

from models.main import Model
from views.main import View

from .home import HomeController
from .create_group import CreateGroupController
from .group import GroupController
from .create_expense import CreateExpenseController
from .history import HistoryController


class Controller:
    def __init__(self, model: Model, view: View) -> None:
        self.view = view
        self.model = model

        self.home_controller = HomeController(model, view)
        self.create_group_controller = CreateGroupController(model, view)
        self.group_controller = GroupController(model, view)
        self.create_expense_controller = CreateExpenseController(model, view)
        self.history_controller = HistoryController(model, view)

        event_listeners = {
            "group_selected": self.on_group_selected,
            "group_left": self.on_group_left,
            "page_loaded": self.on_page_loaded,
            "create_expense_page_loaded": self.on_create_expense_page_loaded,
            "edit_group_page_loaded": self.on_edit_group_page_loaded,
            "deselect_group": self.on_deselect_group,
            "created_group": self.on_group_selected,
            "created_expense": self.on_expense_created,
            "export_transactions_to_csv": self.export_transactions_to_csv,
            "history_page_loaded": self.on_history_page_loaded,
        }

        for event, handler in event_listeners.items():
            self.model.add_event_listener(event, handler)

    def on_page_loaded(self, _):
        self.home_controller.update_view()

    def on_history_page_loaded(self, _):
        self.history_controller.update_view()

    def on_group_selected(self, _):
        self.group_controller.update_view()

    def on_group_left(self, _):
        self.home_controller.update_view()

    def on_create_expense_page_loaded(self, _):
        self.create_expense_controller.update_view()

    def on_edit_group_page_loaded(self, _):
        self.create_group_controller.update_view()

    def on_deselect_group(self, _):
        self.model.clear_current_group()

    def on_group_created(self, _):
        self.group_controller.update_view()

    def on_expense_created(self, _):
        self.group_controller.update_view()

    def export_transactions_to_csv(self, _):
        expenses_to_export = self.model.current_group.expenses

        filename = filedialog.asksaveasfilename(
            title="Export transactions to CSV",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*")),
        )

        if filename:
            with open(filename, "w") as f:
                f.write("Description,Amount,Paid by,Split type,Split details\n")
                for expense in expenses_to_export:
                    f.write(expense.to_csv_row() + "\n")

    def start(self) -> None:
        if self.model.groups:
            self.model.trigger_event("page_loaded")

        self.view.start_mainloop()
