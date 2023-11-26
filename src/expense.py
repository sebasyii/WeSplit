from typing import Dict, Union
from enum import Enum, auto

from user import User


class SplitType(Enum):
    """Enumeration for the types of expense splitting methods."""

    EQUAL = auto()
    EXACT = auto()
    PERCENTAGE = auto()


class Expense:
    """Represents an expense in the app.

    This class encapsulates details about an expense, including its description,
    total amount, the user who paid, the split type, and the details of how the
    expense is split among users.

    Attributes:
        description (str): Description of the expense.
        amount (float): Total amount of the expense.
        paid_by (User): The user who paid for the expense.
        split_type (SplitType): The method used to split the expense among users.
        split_details (Dict[User, Union[int, float]]): Details of how the expense
            is split. The key is the user id and the value is the amount that
            user spent on the expense.
    """

    def __init__(
        self,
        description: str,
        amount: float,
        paid_by: User,
        split_type: SplitType,
        split_details: Dict[User, Union[int, float]],
    ) -> None:
        """Initialises a new instance of the Expense class.

        Args:
            description (str): Description of the expense.
            amount (float): Total amount of the expense.
            paid_by (User): The user who paid the expense.
            split_type (SplitType): The method used to split the expense.
            split_details (Dict[User, Union[int, float]]): Details of how the
                expense is split among users.

        Raises:
            ValueError: If the amount is non-positive.
        """
        if amount <= 0:
            raise ValueError("Expense amount must be a positive number")

        self.description = description
        self.amount = amount
        self.paid_by = paid_by
        self.split_type = split_type
        self.split_details = split_details

    def update_split_amount(self, user: User, new_split_amount: Union[int, float]) -> None:
        """Updates the split amount for a specific user in the expense.

        Args:
            user (User): The user whose split amount is to be updated.
            new_split_amount (Union[int, float]): New amount or percentage to be
                assigned to the user.

        Raises:
            ValueError: If the new split amount is non-positive or if the user
                is not a participant in this expense.
        """
        if new_split_amount <= 0:
            raise ValueError("New split amount must be a positive number")

        if user not in self.split_details:
            raise ValueError("User is not a participant in this expense")

        self.split_details[user] = new_split_amount
