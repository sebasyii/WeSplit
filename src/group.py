from collections import defaultdict
import copy
from typing import Dict, List, Tuple
from expense import Expense
from user import User


class Group:
    """Represents a group of users who share a list of expenses.

    This class is responsible for adding and removing members and expenses,
    calculating balances, and determining the minimum number of transactions
    needed to settle all expenses within the group.

    Attributes:
        group_id_counter (int): A class-level counter to assign unique IDs to groups.
        group_name (str): The name of the group.
        group_description (str): A description of the group.
        group_id (int): A unique identifier for the group.
        members (Dict[int, User]): A dictionary of group members, keyed by user ID.
        expenses (List[Expense]): A list of expenses incurred by group members.
    """

    group_id_counter = 0

    def __init__(self, group_name: str, group_description: str):
        """Initializes a new instance of the Group class.

        Args:
            group_name (str): The name of the group.
            group_description (str): A description of the group.
        """
        self.group_name = group_name
        self.group_description = group_description
        self.group_id = Group.group_id_counter
        self.members: Dict[int, User] = {}
        self.expenses: List[Expense] = []

        Group.group_id_counter += 1

    def add_member(self, member: User) -> None:
        """Adds a member to the group.

        Args:
            member (User): The member to be added to the group.
        """
        self.members[member.id] = member

    def remove_member(self, member: User) -> None:
        """Removes a member from the group.

        Args:
            member (User): The member to be removed from the group.

        Raises:
            KeyError: If the member is not found in the group.
        """
        try:
            del self.members[member.id]
        except KeyError as e:
            raise KeyError(f"Member with ID {member.id} not found in the group.") from e

    def add_expense(self, expense: Expense) -> None:
        """Adds an expense to the group.

        Args:
            expense (Expense): The expense to be added to the group.
        """
        self.expenses.append(expense)

    def remove_expense(self, expense: Expense) -> None:
        """Removes an expense from the self.expenses list.

        Args:
            expense (Expense): The expense to be removed from the self.expenses list.

        Raises:
            ValueError: If the expense is not found in the list.
        """
        try:
            self.expenses.remove(expense)
        except ValueError as e:
            raise ValueError("Expense not found in the list.") from e

    def __shape_data(self) -> List[Tuple[int, int, float]]:
        """Reshapes expense data for calculations.

        This private method processes the expenses of the group, preparing the data
        for `calculate_min_transfers()`

        Returns:
            List[Tuple[int, int, float]]: A list of tuples representing the expenses
            in the form (payer_id, payee_id, amount).
        """
        reshaped_data = []
        for expense in self.expenses:
            for user, amount in expense.split_details.items():
                if user.id != expense.paid_by.id:
                    reshaped_data.append((expense.paid_by.id, user.id, amount))
        return reshaped_data

    def calculate_min_transfers(self) -> List[Tuple[int, int, float]]:
        """Calculates the minimum number of transactions to settle group expenses.

        This method calculates the minimum number of transactions needed to settle
        all the debts in the group.

        Returns:
            List[Tuple[int, int, float]]: A list of transactions in the form
            (payer_id, payee_id, amount) representing the minimal transfers needed
            to settle all the debts.
        """
        balance = self.__calculate_balances()
        temp_sum = 0
        for i in balance:
            temp_sum += balance[i]
        if temp_sum != 0:
            raise ValueError("The group is not balanced.")

        # lenders, borrowers = self.__separate_lenders_borrowers(balance)
        # return self.__match_and_create_transactions(balance)
        return self.greedy(balance, [])

    def __calculate_balances(self) -> Dict[int, float]:
        """Calculates the net balance for each user in the group.

        This private method computes the net balance for each user in the group.
        Negative balances indicate that the user owes money to the group, while
        positive balances indicate that the user is owed money by the group.

        Returns:
            Dict[int, float]: A dictionary mapping user IDs to their net balances.
        """
        balance = defaultdict(float)
        for from_person, to_person, amount in self.__shape_data():
            print(f"from_person: {from_person}, to_person: {to_person}, amount: {amount}")
            balance[from_person] -= amount
            balance[to_person] += amount
        return balance

    def __separate_lenders_borrowers(self, balance: Dict[int, float]) -> Tuple[Dict[int, float], Dict[int, float]]:
        """Separates users into lenders and borrowers based on their balances.

        Args:
            balance (Dict[int, float]): The balance of each user in the group.

        Returns:
            Tuple[Dict[int, float], Dict[int, float]]: Two dictionaries representing
            lenders and borrowers, respectively.
        """
        lenders = {person: amt for person, amt in balance.items() if amt > 0}
        borrowers = {person: amt for person, amt in balance.items() if amt < 0}
        return lenders, borrowers

    def __match_and_create_transactions(
        self, lenders: Dict[int, float], borrowers: Dict[int, float]
    ) -> List[Tuple[int, int, float]]:
        """Matches lenders with borrowers to create a list of transactions.

        This private method pairs borrowers with lenders to settle debts with the
        minimum number of transactions.

        Args:
            lenders (Dict[int, float]): A dictionary of lenders and amounts they are owed.
            borrowers (Dict[int, float]): A dictionary of borrowers and amounts they owe.

        Returns:
            List[Tuple[int, int, float]]: A list of transactions in the form
            (borrower_id, lender_id, amount).
        """
        transactions = []
        for borrower, borrowed_amt in borrowers.items():
            while borrowed_amt < 0:
                print(f"lenders: {lenders}")
                lender = max(lenders, key=lenders.get)
                amt_to_pay = min(lenders[lender], -borrowed_amt)

                lenders[lender] -= amt_to_pay
                borrowed_amt += amt_to_pay

                if lenders[lender] == 0:
                    del lenders[lender]

                transactions.append((borrower, lender, amt_to_pay))
        return transactions
    
    # edge case where if the divisble is not even, the greedy algorithm will not work since the balance is not 0
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
        for i in m :
            index = i
            value = m[index]
            break
        # obtain min element
        for x in m :
            if m[x] < value :
                index, value = x, m[x]
        return index, value


    def shape_data_for_treeview(self, transactions: List[Tuple[int, int, float]]) -> List[Tuple[str, str, str]]:
        """Shapes data for display in a Treeview widget in the group frame.

        This method restructures transaction data to a format suitable for
        the treeview widget in the group frame.

        Args:
            transactions (List[Tuple[int, int, float]]): A list of transactions that
            is created by `calculate_min_transfers()`.

        Returns:
            List[Tuple[str, str, str]]: A list of tuples in the format suitable for
            the Treeview widget.
        """
        reshaped_data = {}
        for payer, payee, amount in transactions:
            if payee not in reshaped_data:
                reshaped_data[payee] = {}
            reshaped_data[payee][payer] = amount

        return reshaped_data

    def __str__(self) -> str:
        """String representation of the Group.

        Returns:
            str: A string describing the group, including its ID, name, and description.
        """
        return f"Group Name: {self.group_name}, Group Description: {self.group_description}"
