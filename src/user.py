class User:
    id = 0
    
    def __init__(self, name):
        self.id = User.id
        self.name = name
        self.balances = {} # { group: amount }
        User.id += 1