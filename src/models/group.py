from collections import defaultdict
import copy
from decimal import Decimal
from typing import Dict, List, Tuple
from .expense import Expense
from .user import User
from .base import ObservableModel


class Group:
    group_id_counter = 0

    def __init__(self, group_name: str, group_description: str):
        self.group_name = group_name
        self.group_description = group_description
        self.group_id = Group.group_id_counter
        self.members: Dict[int, User] = {}
        self.expenses: List[Expense] = []

        Group.group_id_counter += 1

    @property
    def id(self) -> int:
        return self.group_id

    @property
    def name(self) -> str:
        return self.group_name

    @name.setter
    def name(self, new_name: str) -> None:
        self.group_name = new_name

    @property
    def description(self) -> str:
        return self.group_description

    @description.setter
    def description(self, new_description: str) -> None:
        self.group_description = new_description

    def update_members(self, members: Dict[int, User]) -> None:
        self.members = members

    def add_member(self, member: User) -> None:
        self.members[member.id] = member

    def remove_member(self, member: User) -> None:
        try:
            del self.members[member.id]
        except KeyError as e:
            raise KeyError(f"Member with ID {member.id} not found in the group.") from e

    def add_expense(self, expense: Expense) -> None:
        self.expenses.append(expense)

    def remove_expense(self, expense: Expense) -> None:
        try:
            self.expenses.remove(expense)
        except ValueError as e:
            raise ValueError("Expense not found in the list.") from e

    def __shape_data(self) -> List[Tuple[int, int, float]]:
        reshaped_data = []
        for expense in self.expenses:
            for user, amount in expense.split_details.items():
                if user.id != expense.paid_by.id:
                    reshaped_data.append((expense.paid_by.id, user.id, amount))
        return reshaped_data

    def calculate_min_transfers(self) -> List[Tuple[int, int, float]]:
        balance = self.__calculate_balances()
        temp_sum = 0
        for i in balance:
            temp_sum += balance[i]
        if temp_sum != 0:
            raise ValueError("The group is not balanced.")

        return self.greedy(balance, [])

    def __calculate_balances(self) -> Dict[int, float]:
        balance = defaultdict(Decimal)
        for from_person, to_person, amount in self.__shape_data():
            print(f"from_person: {from_person}, to_person: {to_person}, amount: {amount}, type: {type(amount)}")
            balance[from_person] -= amount
            balance[to_person] += amount
        return balance

    # edge case where if the divisble is not even, the greedy algorithm will not work since the balance is not 0
    # https://github.com/ATMackay/splitwise/blob/main/python/src/splitwise/split.py
    def greedy(self, scores, debt_array):
        if len(scores) == 0:
            return debt_array

        # Create a deep copy of scores to avoid modifying the original
        scores_copy = copy.deepcopy(scores)

        max_creditor, max_credit = self.max_entry(scores_copy)
        max_debtor, max_debt = self.min_entry(scores_copy)

        if max_credit == -max_debt:
            debt_array.append([max_debtor, max_creditor, -max_debt])
            del scores_copy[max_debtor]
            del scores_copy[max_creditor]
        elif max_credit > -max_debt:
            debt_array.append([max_debtor, max_creditor, -max_debt])
            del scores_copy[max_debtor]
            scores_copy[max_creditor] += max_debt
        else:  # max_credit < -max_debt
            debt_array.append([max_debtor, max_creditor, max_credit])
            del scores_copy[max_creditor]
            scores_copy[max_debtor] += max_credit

        return self.greedy(scores_copy, debt_array)

    def max_entry(self, m):
        # find first element
        for i in m:
            index = i
            value = m[index]
            break

        # obtain max element
        for x in m:
            if m[x] > value:
                index, value = x, m[x]
        return index, value

    def min_entry(self, m):
        # find first element
        for i in m:
            index = i
            value = m[index]
            break
        # obtain min element
        for x in m:
            if m[x] < value:
                index, value = x, m[x]
        return index, value

    def shape_data_for_treeview(self, transactions: List[Tuple[int, int, float]]) -> List[Tuple[str, str, str]]:
        # TDOO: add payee if not in transactions anyways because I want them to appear in the treeview
        reshaped_data = {}
        for payer, payee, amount in transactions:
            if payee not in reshaped_data:
                reshaped_data[payee] = {}
            reshaped_data[payee][payer] = amount

        return reshaped_data

    def __str__(self) -> str:
        return f"Group Name: {self.group_name}, Group Description: {self.group_description}"
