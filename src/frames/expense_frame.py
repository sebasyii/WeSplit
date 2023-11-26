from math import floor
import math
from tkinter import messagebox, ttk
import tkinter as tk
from expense import Expense
from group import Group


class ExpenseFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(relwidth=1, relheight=1)

        self.checkboxes = []
        self.member_entries = []

        self.create_widgets()

    def create_widgets(self):
        self.back_button = ttk.Button(self, text="Back", command=lambda: self.group_frame.tkraise())
        self.back_button.grid(row=0, column=0, sticky="ew", padx=10, pady=1)

        self.amount_label = ttk.Label(self, text="Amount")
        self.amount_entry = ttk.Entry(self)

        self.amount_label.grid(row=1, column=0, sticky="ew", padx=10, pady=1)
        self.amount_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=10, pady=1)

        self.description_label = ttk.Label(self, text="Description")
        self.description_entry = ttk.Entry(self)

        self.description_label.grid(row=2, column=0, sticky="ew", padx=10, pady=1)
        self.description_entry.grid(row=2, column=1, columnspan=2, sticky="ew", padx=10, pady=1)

        self.split_type_label = ttk.Label(self, text="Split Type")
        self.split_type_label.grid(row=3, column=0, sticky="ew", padx=10, pady=1)
        self.split_type_combobox = ttk.Combobox(self, state="readonly")
        self.split_type_combobox["values"] = ("Equal", "Exact Amounts", "Percentages")
        self.split_type_combobox.grid(row=3, column=1, sticky="ew", padx=10, pady=1)
        self.split_type_combobox.current(0)  # Set the default value to 'Equal'
        self.split_type_combobox.bind("<<ComboboxSelected>>", self.on_split_type_changed)

        self.paid_by_label = ttk.Label(self, text="Paid By")
        self.paid_by_label.grid(row=4, column=0, sticky="ew", padx=10, pady=1)
        self.paid_by_combobox = ttk.Combobox(self, state="readonly")
        self.paid_by_combobox.grid(row=4, column=1, sticky="ew", padx=10, pady=1)

        self.record_expense_button = ttk.Button(self, text="Record Expense", command=self.record_expense)
        self.record_expense_button.grid(row=10, column=11, sticky="ew", padx=10, pady=20)

        self.configure_grid()

    def configure_grid(self):
        """Configure grid layout for Expense Frame."""
        for i in range(12):
            self.columnconfigure(i, weight=1)

        for i in range(10):
            self.rowconfigure(i, weight=1)

    def update_expense_frame_data(self, group: Group, group_frame: ttk.Frame):
        """Update the data in the expense frame."""
        # Declare self.group_frame
        self.group_frame = group_frame

        # Update the paid_by_combobox
        self.paid_by_combobox["values"] = tuple(group.members.values())
        self.paid_by_combobox.current(0)

        self.group = group  # Keep track of the group data

        if self.split_type_combobox.get() == "Equal":
            self.display_member_checkboxes()

    def on_split_type_changed(self, event):
        # Get the selected split type
        combobox = event.widget
        split_type = combobox.get()

        if split_type == "Equal":
            self.display_member_checkboxes()
        elif split_type in ["Exact Amounts", "Percentages"]:
            self.display_member_entries(split_type)
        else:
            self.hide_member_widgets()

    def display_member_checkboxes(self):
        self.hide_member_entries()

        # Create a checkbox for each member
        if self.group:  # Ensure that the group data is available
            for i, member in enumerate(self.group.members.values(), start=5):
                var = tk.BooleanVar(value=True)  # Pre-check the checkboxes
                chk = ttk.Checkbutton(self, text=member.name, variable=var)
                chk.grid(row=i, column=1, sticky="w", padx=10, pady=1)
                self.checkboxes.append((chk, var))  # Keep track of the checkbox and variable

    def display_member_entries(self, split_type):
        if self.group:  # Ensure that the group data is available
            for i, member in enumerate(self.group.members.values(), start=5):
                entry = ttk.Entry(self)
                entry.grid(row=i, column=2, columnspan=5)
                self.member_entries.append((member, entry))

    def hide_member_checkboxes(self):
        # Remove all member checkboxes
        for chk, var in self.checkboxes:
            chk.destroy()
        self.checkboxes.clear()

    def hide_member_entries(self):
        # Remove all member entries
        for member, entry in self.member_entries:
            entry.destroy()
        self.member_entries.clear()

    def record_expense(self):
        amount = self.amount_entry.get()
        description = self.description_entry.get()
        split_type = self.split_type_combobox.get()
        paid_by = self.paid_by_combobox.get()

        # Find the user object of the paid_by member
        paid_by = next((member for member in self.group.members.values() if member.name == paid_by), None)

        # Check if any of the fields are empty
        if not amount or not description or not split_type or not paid_by:
            messagebox.showerror(title="Error", message="Please fill all fields.")
            return

        # Check if the amount is a valid number
        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror(title="Error", message="Invalid amount.")
            return

        # Check if the amount is greater than 0
        if amount <= 0:
            messagebox.showerror(title="Error", message="Amount must be greater than 0.")
            return

        # at least one checkbox must be checked
        if split_type == "Equal":
            if not any(var.get() for chk, var in self.checkboxes):
                messagebox.showerror(title="Error", message="Please select at least one member.")
                return

        # This Section is used to convert the selected choices to the required format for split details
        if split_type == "Equal":
            num_members = sum(var.get() for chk, var in self.checkboxes)
            base_amount_per_member = round(amount / num_members, 2)  # Rounded to 2 decimal places

            covered_amount = base_amount_per_member * num_members
            rounding_difference = round(amount - covered_amount, 2)  # Rounding difference due to 2 decimal places

            split_details = {}
            for member, (chk, var) in zip(self.group.members.values(), self.checkboxes):
                if var.get():
                    split_details[member] = base_amount_per_member
                    # Distribute the rounding difference
                    if rounding_difference > 0:
                        extra_amount = min(0.01, rounding_difference)
                        split_details[member] += extra_amount
                        rounding_difference -= extra_amount

            # Check if rounding difference is completely distributed
            assert math.isclose(rounding_difference, 0, abs_tol=0.01), "Rounding difference not fully allocated"
        elif split_type == "Exact Amounts":
            total_input_amount = 0
            split_details = {}
            for member, (chk, var) in zip(self.group.members.values(), self.checkboxes):
                if var.get():  # Only if the member is selected
                    entry = next(
                        (entry for member_entry, entry in self.member_entries if member_entry.id == member.id), None
                    )
                    try:
                        member_amount = float(entry.get())
                        if member_amount < 0:
                            raise ValueError("Negative amount is not allowed")
                    except ValueError:
                        messagebox.showerror("Error", f"Invalid amount for {member.name}")
                        return

                    total_input_amount += member_amount
                    split_details[member] = member_amount

            # Validate if the total input amount matches the total expense amount
            if not math.isclose(total_input_amount, amount, rel_tol=1e-9):
                messagebox.showerror("Error", "The total of exact amounts does not equal the expense amount.")
                return
        elif split_type == "Percentages":
            total_percentage = 0
            split_details = {}
            for member, (chk, var) in zip(self.group.members.values(), self.checkboxes):
                if var.get():  # Only if the member is selected
                    entry = next(
                        (entry for member_entry, entry in self.member_entries if member_entry.id == member.id), None
                    )
                    try:
                        member_percentage = float(entry.get())
                        if member_percentage < 0 or member_percentage > 100:
                            raise ValueError("Percentage must be between 0 and 100")
                    except ValueError:
                        messagebox.showerror("Error", f"Invalid percentage for {member.name}")
                        return

                    total_percentage += member_percentage
                    split_details[member] = amount * (member_percentage / 100)

            # Validate if the total percentage is 100%
            if not math.isclose(total_percentage, 100, rel_tol=1e-9):
                messagebox.showerror("Error", "The total of percentages does not equal 100%.")
                return

        # If all validation passes, proceed to record the expense
        new_expense = Expense(description, amount, paid_by, split_type, split_details)

        # Print all the new expense details
        print("--------------------")
        print("Description:", new_expense.description)
        print("Amount:", new_expense.amount)
        print("Paid By:", new_expense.paid_by.name)
        print("Split Type:", new_expense.split_type)
        print("Split Details:", new_expense.split_details)
        print("--------------------")

        self.group.add_expense(new_expense)

        # Clear the fields after recording the expense
        self.amount_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.split_type_combobox.current(0)
        self.paid_by_combobox.current(0)
        self.hide_member_checkboxes()
        self.group_frame.update_group_frame_data(self.group)
        self.group_frame.tkraise()
