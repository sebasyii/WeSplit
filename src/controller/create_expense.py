from decimal import ROUND_DOWN, ROUND_HALF_DOWN, ROUND_UP, Decimal
import math
from tkinter import BooleanVar, DoubleVar, IntVar, messagebox
from tkinter import ttk
from views.main import View
from models.main import Model
from models.expense import Expense

class CreateExpenseController:
    def __init__(self, model: Model, view: View):
        self.view = view
        self.model = model
        self.frame = self.view.frames["create_expense"]

        self.temp_checkboxes = []

        self._setup()

    def _setup(self):
        self.frame.record_expense_button.config(command=self.record_expense)
        self.frame.back_button.config(command=self.cancel)
        self.frame.split_type_combobox.bind("<<ComboboxSelected>>", self.on_split_type_changed)

    def on_split_type_changed(self, event):
        split_type = self.frame.split_type_combobox.get()
        if split_type == "Equal":
            self.generate_checkboxes(equal_split=True)
        else:
            self.generate_checkboxes(equal_split=False)

    def generate_checkboxes(self, equal_split=False):
        # Clear any existing checkboxes
        for widget in self.frame.members_split_entries_container.winfo_children():
            widget.destroy()

        self.member_vars = {}
        self.member_entries = []
        for idx, member in enumerate(self.model.current_group.members.values()):
            var = BooleanVar(value=True)  # Pre-check the checkboxes
            chk = ttk.Checkbutton(self.frame.members_split_entries_container, text=member.name, variable=var, padding=5)
            self.temp_checkboxes.append((chk, var))
            chk.grid(row=idx, sticky="ew")
            self.member_vars[member.id] = var

            if not equal_split:
                entry = ttk.Entry(self.frame.members_split_entries_container, width=5)
                entry.grid(row=idx, column=1, columnspan=11, sticky="ew")
                self.member_entries.append((member, entry))

    def clear_checkboxes(self):
        for widget in self.frame.members_split_entries_container.winfo_children():
            widget.destroy()

    def record_expense(self):
        amount = self.frame.amount_entry.get()
        description = self.frame.description_entry.get()
        split_type = self.frame.split_type_combobox.get()
        paid_by = self.frame.paid_by_combobox.get()

        paid_by = next((member for member in self.model.current_group.members.values() if member.name == paid_by), None)

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
        
        # check if amount input is in 2d.p
        if amount != round(amount, 2):
            messagebox.showerror(title="Error", message="Amount must be in 2 decimal places.")
            return
        
        # check if there is at least one checked member
        if not any(var.get() for var in self.member_vars.values()):
            messagebox.showerror(title="Error", message="Please select at least one member.")
            return
        
        # Main split amount
        split_details = {}

        if split_type == "Equal":
            num_members = sum(var.get() for chk, var in self.temp_checkboxes)

            splits = self._split_amount(amount, num_members)
            for member, (chk, var) in zip(self.model.current_group.members.values(), self.temp_checkboxes):
                if var.get():
                    split_details[member] = splits.pop(0)
            
        elif split_type == "Exact Amounts":
            total_input_amount = 0
            
        elif split_type == "Percentages":
            total_percentage = 0
            
        new_expense = Expense(description, amount, paid_by, split_type, split_details)

         # Print all the new expense details
        print("--------------------")
        print("Description:", new_expense.description)
        print("Amount:", new_expense.amount)
        print("Paid By:", new_expense.paid_by.name)
        print("Split Type:", new_expense.split_type)
        print("Split Details:", new_expense.split_details)
        print("--------------------")

        self.model.add_expense_to_group(self.model.current_group.id, new_expense)

        # Clear the entries
        self.frame.amount_entry.delete(0, "end")
        self.frame.description_entry.delete(0, "end")
        self.frame.paid_by_combobox.set("")

        self.model.trigger_event('created_expense')
        self.view.switch("group")


    def cancel(self):
        self.view.switch("group")

    def update_view(self):
        members = self.model.current_group.members
        self.frame.paid_by_combobox["values"] = tuple(members.values())
        self.on_split_type_changed(None)


    # Private methods
    def _split_amount(self, total_amount: str, num_members: int):
        amount = Decimal(total_amount)
        split_amount_precise = amount / num_members
        split_amount = split_amount_precise.quantize(Decimal('.01'), rounding=ROUND_DOWN)

        total_allocated = split_amount * num_members
        remainder = amount - total_allocated
        
        splits = [split_amount for _ in range(num_members)]
        temp_idx = 0
        while remainder >= Decimal('0.01'):
            splits[temp_idx] += Decimal('.01')  
            remainder -= Decimal('.01')
            temp_idx += 1 
            temp_idx %= num_members

        splits[temp_idx] = (splits[temp_idx] + remainder).quantize(Decimal('.01'), rounding=ROUND_UP)

        return splits