from typing import Optional
from .user import User
from .group import Group
from .base import ObservableModel
from .expense import Expense


class Model(ObservableModel):
    def __init__(self) -> None:
        super().__init__()

        self.current_group: Optional[Group] = None

    def set_current_group(self, group_id: int) -> None:
        self._validate_group_id(group_id)
        self.current_group = self.groups[group_id]
        self.trigger_event("group_selected")

    def add_expense_to_group(self, group_id: int, expense: Expense) -> None:
        self._validate_group_id(group_id)
        self.groups[group_id].add_expense(expense)

    def clear_current_group(self) -> None:
        self.current_group = None

    def add_group(self, group: Group) -> None:
        self.groups[group.id] = group

    def remove_group(self, group_id: int) -> None:
        self._validate_group_id(group_id)
        self.groups.pop(group_id)

    def edit_group(self, group_id: int, group_name: str, group_description: str) -> None:
        self._validate_group_id(group_id)
        group = self.groups[group_id]
        group.group_name = group_name
        group.group_description = group_description
        group.trigger_event("group_updated")

    def _validate_group_id(self, group_id: int) -> None:
        if group_id not in self.groups:
            raise KeyError(f"Group with ID {group_id} not found.")
