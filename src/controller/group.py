from tkinter import messagebox
from views.main import View
from models.main import Model


class GroupController:
    def __init__(self, model: Model, view: View):
        self.view = view
        self.model = model
        self.frame = self.view.frames["group"]
        self._setup_event_bindings()

    def _setup_event_bindings(self):
        self.frame.add_expense_button.config(command=self._add_expense)
        self.frame.edit_group_button.config(command=self._edit_group)
        self.frame.back_button.config(command=self._go_back)
        self.frame.export_expenses_button.config(command=self.export_transactions_to_csv)

    def _go_back(self):
        self.model.trigger_event("deselect_group")
        self.model.trigger_event("page_loaded")
        self.view.switch("home")

    def _add_expense(self):
        self.model.trigger_event("create_expense_page_loaded")
        self.view.switch("create_expense")

    def _edit_group(self):
        self.model.trigger_event("edit_group_page_loaded")
        self.view.switch("create_group")

    def export_transactions_to_csv(self):
        self.model.trigger_event("export_transactions_to_csv")
        messagebox.showinfo("Success", "Transactions exported")

    def _update_member_treeview(self, treeview_data):
        self.frame.member_tree.delete(*self.frame.member_tree.get_children())

        for member_id, transactions in treeview_data.items():
            member_name = self.model.current_group.members[member_id].name
            parent_id = self.frame.member_tree.insert("", "end", text=member_name, values=("", ""))

            for owed_member_id, amount in transactions.items():
                owed_member_name = self.model.current_group.members[owed_member_id].name
                self.frame.member_tree.insert(parent_id, "end", text=owed_member_name, values=("Owes", amount))

    def update_view(self):
        transactions = self.model.current_group.calculate_min_transfers()
        treeview_data = self.model.current_group.shape_data_for_treeview(transactions)

        self._update_member_treeview(treeview_data)
