from collections import defaultdict
from typing import Dict, List, Tuple
from expense import Expense
from user import User

class Group:
    group_id_counter = 0

    def __init__(self, group_name: str, group_description: str):
        self.group_name = group_name
        self.group_description = group_description
        self.group_id = Group.group_id_counter
        self.members: Dict[int, User] = {}
        self.expenses: List[Expense] = []

        Group.group_id_counter += 1

    def add_member(self, member: User) -> None:
        """Add a member to the group."""
        self.members[member.id] = member

    def remove_member(self, member: User) -> None:
        """Remove a member from the group. Raises KeyError if the member is not found."""
        try:
            del self.members[member.id]
        except KeyError:
            print(f"Member with ID {member.id} not found in the group.")

    def add_expense(self, expense: Expense) -> None:
        """Add an expense to the group."""
        self.expenses.append(expense)

    def remove_expense(self, expense: Expense) -> None:
        """Remove an expense from the group. Raises ValueError if the expense is not found."""
        try:
            self.expenses.remove(expense)
        except ValueError:
            print("Expense not found in the group.")

    def __shape_data(self) -> List[Tuple[int, int, float]]:
        """Private method to reshape expense data for calculations."""
        reshaped_data = []
        for expense in self.expenses:
            for user, amount in expense.split_details.items():
                if user.id != expense.paid_by.id:
                    reshaped_data.append((expense.paid_by.id, user.id, amount))
        print(f"Reshaped data: {reshaped_data}")
        return reshaped_data

    def calculate_min_transfers(self) -> List[Tuple[int, int, float]]:
        """
        Calculate the minimum number of transactions required to settle the group's expenses.
        Returns a list of transactions in the form of (payer_id, payee_id, amount).
        """
        balance = self.__calculate_balances()
        lenders, borrowers = self.__separate_lenders_borrowers(balance)
        return self.__match_and_create_transactions(lenders, borrowers)

    def __calculate_balances(self) -> Dict[int, float]:
        """Calculate the net balance for each user."""
        balance = defaultdict(float)
        for from_person, to_person, amount in self.__shape_data():
            balance[from_person] -= amount
            balance[to_person] += amount
        return balance

    def __separate_lenders_borrowers(self, balance: Dict[int, float]) -> Tuple[Dict[int, float], Dict[int, float]]:
        """Separate users into lenders and borrowers."""
        lenders = {person: amt for person, amt in balance.items() if amt > 0}
        borrowers = {person: amt for person, amt in balance.items() if amt < 0}
        return lenders, borrowers

    def __match_and_create_transactions(self, lenders: Dict[int, float], borrowers: Dict[int, float]) -> List[Tuple[int, int, float]]:
        """Match lenders with borrowers to create a list of transactions."""
        transactions = []
        for borrower, borrowed_amt in borrowers.items():
            while borrowed_amt < 0:
                lender = max(lenders, key=lenders.get)
                amt_to_pay = min(lenders[lender], -borrowed_amt)

                lenders[lender] -= amt_to_pay
                borrowed_amt += amt_to_pay

                if lenders[lender] == 0:
                    del lenders[lender]

                transactions.append((borrower, lender, amt_to_pay))
        return transactions

    def shape_data_for_treeview(self, transactions: List[Tuple[int, int, float]]) -> List[Tuple[str, str, str]]:
        """Shape data for the Treeview widget in the Group Frame."""
        reshaped_data = {}
        for payer, payee, amount in transactions:
            if payee not in reshaped_data:
                reshaped_data[payee] = {}
            reshaped_data[payee][payer] = amount
        
        return reshaped_data


    def __str__(self) -> str:
        return f"Group ID: {self.group_id}, Group Name: {self.group_name}, Group Description: {self.group_description}"
