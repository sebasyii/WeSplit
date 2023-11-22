from group import Group

from user import User
from expense import Expense

def test():
    g = Group("Test Group", "This is the test group description.")

    # Create new user
    bob = User("Bob")
    alice = User("Alice")
    john = User("John")

    # Create Expense
    expense = Expense("Starbucks", 30, bob, "equal", {alice.id: 10, john.id: 10, bob.id: 10})
    expense2 = Expense("Coffee Bean", 30, alice, "equal", {alice.id: 10, john.id: 10, bob.id: 10})
    expense3 = Expense("Trip", 50, john, "exact", {alice.id: 15, john.id: 25, bob.id: 10})
    

    # Add members to group
    g.add_member(bob)
    g.add_member(alice)
    g.add_member(john)

    # Add expense to group
    g.add_expense(expense)
    g.add_expense(expense2)
    g.add_expense(expense3)

    print(g.shape_data())

if __name__ == "__main__":
    test()