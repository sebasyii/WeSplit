from tkinter import Tk
from app import App

from typing import List

from group import Group
from expense import Expense

def main():

    # Temp group
    temp_group = Group("Test Group", "This is a test group")
    groups: List[Group] = [temp_group]
    App("WeSplit", (800, 600), groups)


if __name__ == "__main__":
    main()
