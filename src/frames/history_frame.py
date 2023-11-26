from tkinter import ttk
import tkinter as tk

from group import Group


class HistoryFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relwidth=1, relheight=1)

        self.create_widgets()

    def create_widgets(self):
        # Back button
        back_button = ttk.Button(self, text="Back")

        # Table of expenses
        # Date, Title, Description, Amount, Paid By, Split Type, Members

        self.configure_grid()

    def configure_grid(self):
        """Configure grid layout for Group Frame."""
        for i in range(12):
            self.columnconfigure(i, weight=1)

        for i in range(10):
            self.rowconfigure(i, weight=1)
