from typing import Dict, Union
from user import User  # Assuming User is a predefined class
from enum import Enum, auto


class SplitType(Enum):
    EQUAL = auto()
    EXACT = auto()
    PERCENTAGE = auto()
    # Add other split types as needed


class Expense:
    def __init__(
        self,
        description: str,
        amount: float,
        paid_by: User,
        split_type: SplitType,
        split_details: Dict[User, Union[int, float]],
    ) -> None:
        """
        Initialize a new Expense.
        :param description: Description of the expense.
        :param amount: Total amount of the expense.
        :param paid_by: The User who paid the expense.
        :param split_type: The method used to split the expense.
        :param split_details: Details of how the expense is split among users.
        """
        self.description: str = description
        self.amount: float = amount
        self.paid_by: User = paid_by
        self.split_type: SplitType = split_type
        self.split_details: Dict[User, Union[int, float]] = split_details

    def update_split_amount(
        self, user_id: str, new_split_amount: Union[int, float]
    ) -> None:
        """
        Update the split amount for a specific user.
        :param user_id: ID of the user whose split amount is to be updated.
        :param new_split_amount: New amount or percentage to be assigned to the user.
        """
        if new_split_amount <= 0:
            raise ValueError("New split amount must be a positive number")

        if user_id not in self.split_details:
            raise ValueError("User is not a participant in this expense")

        self.split_details[user_id] = new_split_amount

    # Additional methods for expense management can be added here
