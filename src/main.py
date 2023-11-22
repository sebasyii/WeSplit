from tkinter import Tk
from app import App

from group import Group
from expense import Expense

def main():
    groups = []
    App("WeSplit", (800, 600), groups)


if __name__ == "__main__":
    main()
