from tkinter import ttk
import tkinter as tk

from group import Group


class GroupFrame(ttk.Frame):
    def __init__(self, parent, expense_frame):
        super().__init__(parent)
        self.place(relwidth=1, relheight=1)
        self.expense_frame = expense_frame

        self.create_widgets()

    def create_widgets(self):
        add_expense_button = ttk.Button(self, text="Add Expense", command=self.call_expense_frame)
        history_button = ttk.Button(self, text="History")
        self.edit_group_button = ttk.Button(self, text="Edit Group")

        self.configure_grid()

        # Place widgets
        add_expense_button.grid(column=0, row=0, padx=10, pady=20, columnspan=4, sticky=tk.EW)
        history_button.grid(column=4, row=0, padx=10, pady=20, columnspan=4, sticky=tk.EW)
        self.edit_group_button.grid(column=8, row=0, padx=10, pady=20, columnspan=4, sticky=tk.EW)

        # Create Treeview widget
        self.member_tree = ttk.Treeview(self, columns=("owed_owe", "amount"))

        # Define the columns
        self.member_tree.column("#0", width=120, minwidth=25, anchor=tk.W)  # Name column
        self.member_tree.column("owed_owe", width=120, anchor=tk.CENTER)
        self.member_tree.column("amount", width=120, anchor=tk.E)

        # Create Headings
        self.member_tree.heading("#0", text="Name", anchor=tk.W)
        self.member_tree.heading("owed_owe", text="Owed/Owe", anchor=tk.CENTER)
        self.member_tree.heading("amount", text="Amount", anchor=tk.E)

        # Place Treeview widget in the grid
        self.member_tree.grid(row=1, rowspan=11, column=0, columnspan=12, sticky="nsew", padx=10, pady=20)

    def configure_grid(self):
        """Configure grid layout for Group Frame."""
        for i in range(12):
            self.columnconfigure(i, weight=1)

        for i in range(10):
            self.rowconfigure(i, weight=1)

    def set_create_grp_frame(self, create_grp_frame):
        self.create_grp_frame = create_grp_frame
        # Add command to create group button
        self.edit_group_button.configure(command=self.create_grp_frame.tkraise)

    def update_group_frame_data(self, group: Group):
        """Update the group frame data."""
        self.group = group
        transactions = self.group.calculate_min_transfers()
        treeview_data = self.group.shape_data_for_treeview(transactions)

        # Clear the treeview
        self.member_tree.delete(*self.member_tree.get_children())

        # Insert new data into the treeview
        for member, owes in treeview_data.items():
            # Temp here but will create a function next time
            # Basically get the user name from id
            member_data = self.group.members[member]

            member_id = self.member_tree.insert("", "end", text=member_data.name, values=("", ""))
            for owed_member, amount in owes.items():
                if amount < 0:
                    owe_text = "Owed"
                else:
                    owe_text = "Owes"

                member_data = self.group.members[owed_member]
                self.member_tree.insert(member_id, "end", text=member_data.name, values=(owe_text, amount))

    def call_expense_frame(self):
        """Raise the expense frame to the top."""
        self.expense_frame.update_expense_frame_data(self.group, self)
        self.expense_frame.tkraise()
