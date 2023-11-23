from collections import defaultdict
from user import User

class Group:
    group_id = 0
    def __init__(self, group_name: str, group_description: str):
        self.group_name = group_name
        self.group_description = group_description
        self.group_id = Group.group_id
        self.members = {}
        self.expenses = []

        Group.group_id += 1
    
    def add_member(self, member: User):
        self.members[member.id] = member
    
    def remove_member(self, member: User):
        del self.members[member.id]

    def add_expense(self, expense):
        self.expenses.append(expense)

    def remove_expense(self, expense):
        self.expenses.remove(expense)

    def shape_data(self): # TODO: Make this private once done with testing
        new_data = []
        for expense in self.expenses:
            for id, amount in expense.split_details.items():
                if id == expense.paid_by.id:
                    continue
                new_data.append([expense.paid_by.id, id, amount])
        return new_data
    
    # https://github.com/nishasinha/Splitwise-Python/blob/master/src/splitwise.py
    def calulate_min_transfers(self, data):
        balance = defaultdict(int)

        # Calculate the net balance for each user
        for from_person, to_person, amount in data:
            balance[from_person] -= amount
            balance[to_person] += amount

        # Categorise users into lenders and borrowers
        lenders = {} #owed money
        borrowers = {} #owe money

        for person, amount in balance.items():
            if amount > 0:
                lenders[person] = amount
            elif amount < 0:
                borrowers[person] = amount

        transactions = []

        # Match borrowers with lenders
        for borrower, borrowed_amt in borrowers.items():
            print(borrower, borrowed_amt)
            abs_borrowed_amt = round(abs(borrowed_amt), 2)
            while abs_borrowed_amt > 0:
                # Get Lender with the highest amount
                lender = max(lenders, key=lenders.get) 
                
                # get lender
                lenders_amt = lenders[lender]
                amt_to_pay = lenders_amt if lenders_amt < abs_borrowed_amt else abs_borrowed_amt

                # Update the lender and borrower amounts
                lenders[lender] -= amt_to_pay
                borrowers[borrower] += amt_to_pay
                abs_borrowed_amt -= amt_to_pay

                # Add transaction
                transactions.append([borrower, lender, amt_to_pay])
        
        return transactions