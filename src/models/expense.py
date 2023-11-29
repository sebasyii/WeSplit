from decimal import Decimal
from typing import Dict, Union
from enum import Enum, auto

from .user import User


class SplitType(Enum):
    EQUAL = auto()
    EXACT = auto()
    PERCENTAGE = auto()


class Expense:
    def __init__(
        self,
        description: str,
        amount: float,
        paid_by: User,
        split_type: SplitType,
        split_details: Dict[User, Decimal],
    ) -> None:
        if amount <= 0:
            raise ValueError("Expense amount must be a positive number")

        self.description = description
        self.amount = amount
        self.paid_by = paid_by
        self.split_type = split_type
        self.split_details = split_details

    def update_split_amount(self, user: User, new_split_amount: Union[int, float]) -> None:
        if new_split_amount <= 0:
            raise ValueError("New split amount must be a positive number")

        if user not in self.split_details:
            raise ValueError("User is not a participant in this expense")

        self.split_details[user] = new_split_amount
