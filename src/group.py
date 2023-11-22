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
    
    def calulate_min_transfers(self, data):
        balance = defaultdict(int)

        # Calculate the net balance for each user
        for from_person, to_person, amount in data:
            balance[from_person] -= amount
            balance[to_person] += amount

        
    