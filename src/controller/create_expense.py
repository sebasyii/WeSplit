import copy
from decimal import ROUND_DOWN, ROUND_UP, Decimal
from tkinter import BooleanVar, messagebox, ttk
from typing import Dict, Optional
from views.main import View
from models.main import Model
from models.expense import Expense
from models.user import User


class CreateExpenseController:
    def __init__(self, model: Model, view: View):
        self.view = view
        self.model = model
        self.frame = self.view.frames["create_expense"]

        self.temp_checkboxes = []

        self._setup_event_bindings()

    def _setup_event_bindings(self) -> None:
        self.frame.record_expense_button.config(command=self._record_expense)
        self.frame.back_button.config(command=self._cancel)
        self.frame.split_type_combobox.bind("<<ComboboxSelected>>", self._on_split_type_changed)

    def _on_split_type_changed(self, _) -> None:
        split_type = self.frame.split_type_combobox.get()
        if split_type == "Equal":
            self._generate_checkboxes(equal_split=True)
        else:
            self._generate_checkboxes(equal_split=False)

    def _generate_checkboxes(self, equal_split=False) -> None:
        self.temp_checkboxes.clear()
        self._clear_member_entries()

        self.member_vars, self.member_entries = {}, []

        for idx, member in enumerate(self.model.current_group.members.values()):
            var, chk = self._create_member_checkbox(member, idx, equal_split)
            self.temp_checkboxes.append((chk, var))

    def _clear_member_entries(self) -> None:
        for widget in self.frame.members_split_entries_container.winfo_children():
            widget.destroy()

    def _create_member_checkbox(self, member: User, idx: int, equal_split: bool) -> tuple[BooleanVar, ttk.Checkbutton]:
        var = BooleanVar(value=True)
        chk = ttk.Checkbutton(self.frame.members_split_entries_container, text=member.name, variable=var, padding=5)
        chk.grid(row=idx, sticky="ew")
        self.member_vars[member.id] = var

        if not equal_split:
            entry = ttk.Entry(self.frame.members_split_entries_container, width=5)
            entry.grid(row=idx, column=1, columnspan=11, sticky="ew")
            self.member_entries.append((member, entry))

        return var, chk

    def _record_expense(self) -> None:
        amount, description, paid_by, category = self._get_expense_details()
        split_type = self.frame.split_type_combobox.get()
        service_charge = self.frame.service_charge_checkbutton.instate(["selected"])
        gst = self.frame.gst_checkbutton.instate(["selected"])

        paid_by = next((member for member in self.model.current_group.members.values() if member.name == paid_by), None)

        if not self._validate_expense_input(amount, description, paid_by, split_type):
            return

        split_data = self._calculate_splits(amount, split_type, service_charge, gst)

        if split_data is None:
            return

        split_details, new_amount = split_data

        new_expense = Expense(description, new_amount, category, paid_by, split_type, split_details)

        # Print all the new expense details
        print("--------------------")
        print("Description:", new_expense.description)
        print("Amount:", new_expense.amount)
        print("Paid By:", new_expense.paid_by.name)
        print("Split Type:", new_expense.split_type)
        print("Split Details:", new_expense.split_details)
        print("Category:", new_expense.category)
        print("--------------------")

        self.model.add_expense_to_group(self.model.current_group.id, new_expense)

        self._clear_expense_entries()
        self.model.trigger_event("created_expense")
        self.view.switch("group")

    def _validate_expense_input(
        self, amount: Decimal, description: str, paid_by: Optional[User], split_type: str
    ) -> bool:
        if not amount or not description or not split_type or not paid_by:
            messagebox.showerror(title="Error", message="Please fill all fields.")
            return False

        try:
            amount = Decimal(amount)
        except ValueError:
            messagebox.showerror(title="Error", message="Invalid amount.")
            return False

        # Check if the amount is greater than 0
        if amount <= 0:
            messagebox.showerror(title="Error", message="Amount must be greater than 0.")
            return False

        # check if amount input is in 2d.p
        if amount != round(amount, 2):
            messagebox.showerror(title="Error", message="Amount must be in 2 decimal places.")
            return False

        # check if there is at least one checked member
        if not any(var.get() for var in self.member_vars.values()):
            messagebox.showerror(title="Error", message="Please select at least one member.")
            return False

        return True

    def _get_expense_details(self) -> tuple[Decimal, str, Optional[User]]:
        amount = self.frame.amount_entry.get()
        description = self.frame.description_entry.get()
        paid_by = self.frame.paid_by_combobox.get()
        category = self.frame.category_combobox.get()

        if amount == "":
            amount = 0

        return Decimal(amount), description, paid_by, category

    def _calculate_splits(self, amount, split_type, service_charge, gst) -> dict[User, Decimal]:
        split_details = {}
        new_amount = self._calculate_new_amount(amount, service_charge, gst, rounding=ROUND_UP)

        if split_type == "Equal":
            num_members = sum(var.get() for _, var in self.temp_checkboxes)

            splits = self._split_amount(new_amount, num_members)
            for member, (_, var) in zip(self.model.current_group.members.values(), self.temp_checkboxes):
                if var.get():
                    split_details[member] = splits.pop(0)

            if new_amount != sum(split_details.values()):
                messagebox.showerror(title="Error", message="Total input amount does not match the total amount.")
                return

        elif split_type == "Exact Amounts":
            total_input_amount = 0

            for member, (_, var) in zip(self.model.current_group.members.values(), self.temp_checkboxes):
                if var.get():
                    entry = next(
                        (entry for member_entry, entry in self.member_entries if member_entry.id == member.id), None
                    )
                    try:
                        member_amount = Decimal(entry.get())
                        if member_amount < 0 or member_amount != round(member_amount, 2):
                            raise ValueError

                        new_member_amount = self._calculate_new_amount(
                            member_amount, service_charge, gst, rounding=ROUND_DOWN
                        )
                        print(new_member_amount)
                        total_input_amount += new_member_amount
                        split_details[member] = new_member_amount
                    except ValueError:
                        messagebox.showerror(title="Error", message="Invalid amount for " + member.name)
                        return

            split_details, total_input_amount = self._match_amount(new_amount, total_input_amount, split_details)

            print(f"The split details are: {split_details}")
            if total_input_amount != new_amount:
                print(f"Total input amount: {total_input_amount}, New amount: {new_amount}")
                messagebox.showerror(title="Error", message="Total input amount does not match the total amount.")
                return

        elif split_type == "Percentages":
            total_percentage = 0
            total_input_amount = 0
            for member, (_, var) in zip(self.model.current_group.members.values(), self.temp_checkboxes):
                if var.get():
                    entry = next(
                        (entry for member_entry, entry in self.member_entries if member_entry.id == member.id), None
                    )
                    try:
                        member_percentage = Decimal(entry.get())
                        if member_percentage == 0:
                            continue
                        if (
                            member_percentage < 0
                            or member_percentage > 100
                            or member_percentage != round(member_percentage, 2)
                        ):
                            raise ValueError
                        total_percentage += member_percentage

                        member_amount = ((member_percentage / 100) * amount).quantize(
                            Decimal(".01"), rounding=ROUND_DOWN
                        )
                        total_input_amount += self._calculate_new_amount(
                            member_amount, service_charge, gst, rounding=ROUND_DOWN
                        )

                        split_details[member] = self._calculate_new_amount(
                            member_amount, service_charge, gst, rounding=ROUND_DOWN
                        )
                    except ValueError:
                        messagebox.showerror(title="Error", message="Invalid percentage for " + member.name)
                        return

            split_details, total_input_amount = self._match_amount(new_amount, total_input_amount, split_details)

            if total_percentage != 100:
                messagebox.showerror(title="Error", message="Total percentage does not equal 100%.")
                return

            if total_input_amount != new_amount:
                messagebox.showerror(title="Error", message="Total input amount does not match the total amount.")
                return

        return split_details, new_amount

    def _calculate_new_amount(self, amount: Decimal, service_charge: bool, gst: bool, rounding: str) -> Decimal:
        if service_charge:
            amount *= Decimal("1.1")
        if gst:
            amount *= Decimal("1.08")
        return amount.quantize(Decimal(".01"), rounding=rounding)

    def _match_amount(self, amount: Decimal, total_input_amount: Decimal, split_details: Dict[User, Decimal]) -> bool:
        new_dict = copy.deepcopy(split_details)
        remainder = amount - total_input_amount

        temp_idx = 0
        while remainder >= Decimal("0.01"):
            new_dict[list(new_dict.keys())[temp_idx]] += Decimal(".01")
            remainder -= Decimal(".01")
            temp_idx += 1
            temp_idx %= len(new_dict)

            total_input_amount += Decimal(".01")

        new_dict[list(new_dict.keys())[temp_idx]] = (new_dict[list(new_dict.keys())[temp_idx]] + remainder).quantize(
            Decimal(".01"), rounding=ROUND_UP
        )

        return new_dict, total_input_amount

    def _clear_expense_entries(self) -> None:
        self.frame.amount_entry.delete(0, "end")
        self.frame.description_entry.delete(0, "end")
        self.frame.paid_by_combobox.set("")
        self.temp_checkboxes.clear()
        self.frame.category_combobox.set("")
        self.frame.split_type_combobox.current(0)
        self.frame.gst_checkbutton.state(["selected"])
        self.frame.service_charge_checkbutton.state(["selected"])
        self.frame.paid_by_combobox.set("")

    def _cancel(self) -> None:
        self.view.switch("group")

    def update_view(self) -> None:
        members = self.model.current_group.members
        self.frame.paid_by_combobox["values"] = tuple(member.name for member in members.values())
        self._on_split_type_changed(None)

    def _split_amount(self, total_amount: Decimal, num_members: int) -> list[Decimal]:
        split_amount_precise = total_amount / num_members
        split_amount = split_amount_precise.quantize(Decimal(".01"), rounding=ROUND_DOWN)

        total_allocated = split_amount * num_members
        remainder = total_amount - total_allocated

        splits = [split_amount for _ in range(num_members)]
        temp_idx = 0
        while remainder >= Decimal("0.01"):
            splits[temp_idx] += Decimal(".01")
            remainder -= Decimal(".01")
            temp_idx += 1
            temp_idx %= num_members

        splits[temp_idx] = (splits[temp_idx] + remainder).quantize(Decimal(".01"), rounding=ROUND_UP)

        return splits
