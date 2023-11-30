from models.main import Model
from views.main import View

from .home import HomeController
from .create_group import CreateGroupController
from .group import GroupController
from .create_expense import CreateExpenseController


class Controller:
    def __init__(self, model: Model, view: View) -> None:
        self.view = view
        self.model = model
        self.home_controller = HomeController(model, view)
        self.create_group_controller = CreateGroupController(model, view)
        self.group_controller = GroupController(model, view)
        self.create_expense_controller = CreateExpenseController(model, view)

        self.model.add_event_listener("group_selected", self.on_group_selected)
        self.model.add_event_listener("group_left", self.on_group_left)
        self.model.add_event_listener("page_loaded", self.on_page_loaded)
        self.model.add_event_listener("create_expense_page_loaded", self.on_create_expense_page_loaded)
        self.model.add_event_listener("edit_group_page_loaded", self.on_edit_group_page_loaded)
        self.model.add_event_listener("deselect_group", self.on_deselect_group)
        self.model.add_event_listener("created_group", self.on_group_selected)
        self.model.add_event_listener("created_expense", self.on_expense_created)

    def on_page_loaded(self, data):
        self.home_controller.update_view()

    def on_group_selected(self, data):
        self.group_controller.update_view()

    def on_group_left(self, data):
        self.home_controller.update_view()

    def on_create_expense_page_loaded(self, data):
        self.create_expense_controller.update_view()

    def on_edit_group_page_loaded(self, data):
        self.create_group_controller.update_view()

    def on_deselect_group(self, data):
        print(self.model.current_group)
        self.model.clear_current_group()

    def on_group_created(self, data):
        self.group_controller.update_view()

    def on_expense_created(self, data):
        self.group_controller.update_view()
        # Clear view

    def start(self) -> None:
        if self.model.groups:
            self.model.trigger_event("page_loaded")

        self.view.start_mainloop()
