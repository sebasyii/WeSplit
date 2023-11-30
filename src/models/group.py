from collections import defaultdict
import copy
from decimal import Decimal
from typing import Dict, List, Tuple
from .expense import Expense
from .user import User
from .base import ObservableModel


class Group:
    _group_id_counter = 0

    def __init__(self, group_name: str, group_description: str) -> None:
        self._group_name = group_name
        self._group_description = group_description
        self._group_id = Group._group_id_counter
        self._members: Dict[int, User] = {}
        self._expenses: List[Expense] = []

        Group._group_id_counter += 1

    @property
    def id(self) -> int:
        return self._group_id

    @property
    def name(self) -> str:
        return self._group_name

    @name.setter
    def name(self, new_name: str) -> None:
        self._group_name = new_name

    @property
    def description(self) -> str:
        return self._group_description

    @description.setter
    def description(self, new_description: str) -> None:
        self.group_description = new_description

    @property
    def members(self) -> Dict[int, User]:
        return self._members
    
    @property
    def expenses(self) -> List[Expense]:
        return self._expenses

    def update_members(self, members: Dict[int, User]) -> None:
        self._members = members

    def add_member(self, member: User) -> None:
        self._members[member.id] = member

    def remove_member(self, member: User) -> None:
        if member.id not in self._members:
            raise KeyError(f"Member with ID {member.id} not found in the group.")
        del self._members[member.id]

    def add_expense(self, expense: Expense) -> None:
        self._expenses.append(expense)

    def remove_expense(self, expense: Expense) -> None:
        try:
            self._expenses.remove(expense)
        except ValueError as e:
            raise ValueError("Expense not found in the list.") from e

    def calculate_min_transfers(self) -> List[Tuple[int, int, Decimal]]:
        balance = self._calculate_balances()

        if sum(balance.values()) != Decimal(0):
            raise ValueError("The group is not balanced.")

        return self._settle_debts(balance)

    def _calculate_balances(self) -> Dict[int, Decimal]:
        balance = defaultdict(Decimal)
        for from_person, to_person, amount in self._shape_data():
            balance[from_person] -= amount
            balance[to_person] += amount
        return balance

    def _shape_data(self) -> List[Tuple[int, int, Decimal]]:
        reshaped_data = []
        for expense in self._expenses:
            for user, amount in expense.split_details.items():
                if user.id != expense.paid_by.id:
                    reshaped_data.append((expense.paid_by.id, user.id, amount))
        return reshaped_data

    def _settle_debts(self, balances: Dict[int, Decimal]) -> List[Tuple[int, int, Decimal]]:
        debtors = {k: v for k, v in balances.items() if v < 0}
        creditors = {k: v for k, v in balances.items() if v > 0}
        transactions = []

        while debtors and creditors:
            debtor_id, debtor_amount = max(debtors.items(), key=lambda x: x[1])  # Get the max debtor
            creditor_id, creditor_amount = min(creditors.items(), key=lambda x: x[1])  # Get the min creditor

            transfer_amount = min(-debtor_amount, creditor_amount)  # Get the min of the two amounts
            transactions.append((debtor_id, creditor_id, transfer_amount))

            debtors[debtor_id] += transfer_amount
            if debtors[debtor_id] == 0:
                del debtors[debtor_id]

            creditors[creditor_id] -= transfer_amount
            if creditors[creditor_id] == 0:
                del creditors[creditor_id]

        return transactions

    def shape_data_for_treeview(self, transactions: List[Tuple[int, int, float]]) -> List[Tuple[str, str, str]]:
        reshaped_data = {}
        for payer, payee, amount in transactions:
            if payee not in reshaped_data:
                reshaped_data[payee] = {}
            reshaped_data[payee][payer] = amount

        return reshaped_data

    def __str__(self) -> str:
        return f"Group Name: {self.group_name}, Group Description: {self.group_description}"
