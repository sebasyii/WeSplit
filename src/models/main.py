from typing import Union
from .user import User
from .group import Group
from .base import ObservableModel
from .expense import Expense


class Model(ObservableModel):
    def __init__(self) -> None:
        super().__init__()
        # Temp
        self.groups = {
            0: Group("SUTD MAKAN GROUP", "Makan Group for the plebs"),
            1: Group("Test Group 2", "This is another test group"),
            2: Group("Test Group 3", "This is a third test group"),
        }
        self.groups[0].add_member(User("Sebastian"))
        self.groups[0].add_member(User("Zhao en"))
        self.groups[0].add_member(User("Peng Siang"))
        self.groups[0].add_member(User("Roger"))
        self.groups[0].add_member(User("Zhan Yue"))
        self.current_group: Union[Group, None] = None

    def set_current_group(self, group_id: int) -> None:
        try:
            self.current_group = self.groups[group_id]
            self.trigger_event("group_selected")
        except KeyError as e:
            raise KeyError(f"Group with ID {group_id} not found in the model.") from e

    def add_expense_to_group(self, group_id: int, expense: Expense) -> None:
        try:
            selected_group = self.groups[group_id]
            selected_group.add_expense(expense)
        except KeyError as e:
            raise KeyError(f"Group with ID {group_id} not found in the model.") from e

    def clear_current_group(self) -> None:
        self.current_group = None

    def add_group(self, group: Group) -> None:
        self.groups[group.id] = group

    def remove_group(self, id: int) -> None:
        try:
            del self.groups[id]
        except KeyError as e:
            raise KeyError(f"Group with ID {id} not found in the model.") from e

    def edit_group(self, id: int, group_name: str, group_description: str) -> None:
        try:
            self.groups[id].group_name = group_name
            self.groups[id].group_description = group_description
            self.groups[id].trigger_event("group_updated")
        except KeyError as e:
            raise KeyError(f"Group with ID {id} not found in the model.") from e
