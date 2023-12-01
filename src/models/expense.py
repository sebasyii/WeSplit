from decimal import Decimal
from typing import Dict, Union
from enum import Enum, auto

from .user import User


class SplitType(Enum):
    EQUAL = auto()
    EXACT = auto()
    PERCENTAGE = auto()


class Expense:
    _id_counter: int = 0

    def __init__(
        self,
        description: str,
        amount: float,
        category: str,
        paid_by: User,
        split_type: SplitType,
        split_details: Dict[User, Decimal],
    ) -> None:
        self._id = Expense._id_counter
        Expense._id_counter += 1

        self._description: str = description
        self._amount: Decimal = Decimal(amount)
        self._paid_by: User = paid_by
        self._category: str = category
        self._split_type: SplitType = split_type
        self._split_details: Dict[User, Decimal] = split_details

    @property
    def id(self) -> int:
        return self._id

    @property
    def description(self) -> str:
        return self._description

    @property
    def amount(self) -> Decimal:
        return self._amount
    
    @property
    def category(self) -> str:
        return self._category

    @property
    def paid_by(self) -> User:
        return self._paid_by

    @property
    def split_type(self) -> SplitType:
        return self._split_type

    @property
    def split_details(self) -> Dict[User, Decimal]:
        return self._split_details

    @description.setter
    def description(self, description: str) -> None:
        self._description = description

    @amount.setter
    def amount(self, amount: float) -> None:
        self._amount = Decimal(amount)

    @paid_by.setter
    def paid_by(self, paid_by: User) -> None:
        self._paid_by = paid_by

    @category.setter
    def category(self, category: str) -> None:
        self._category = category

    @split_type.setter
    def split_type(self, split_type: SplitType) -> None:
        self._split_type = split_type

    @split_details.setter
    def split_details(self, split_details: Dict[User, Decimal]) -> None:
        self._split_details = split_details

    def to_csv_row(self) -> str:
        split_details_str = ""
        if self.split_type == "Equal":
            split_details_str = ",".join(f"{user.name}:{amount}" for user, amount in self.split_details.items())
        elif self.split_type == "Exact Amounts":
            split_details_str = ",".join(f"{user.name}:{amount}" for user, amount in self.split_details.items())
        elif self.split_type == "Percentages":
            split_details_str = ",".join(f"{user.name}:{amount}%" for user, amount in self.split_details.items())
        else:
            raise ValueError(f"Invalid split type: {self.split_type}")

        return f"{self.description},{self.amount},{self.paid_by.name},{self.split_type},{split_details_str}"

    def __str__(self) -> str:
        return f"Expense: {self.description}, Amount: {self.amount}, Paid By: {self.paid_by}, Split Type: {self.split_type}"
