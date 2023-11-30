from views.main import View
from models.main import Model


class GroupController:
    def __init__(self, model: Model, view: View):
        self.view = view
        self.model = model
        self.frame = self.view.frames["group"]
        self._setup()

    def _setup(self):
        self.frame.add_expense_button.config(command=self.add_expense)
        self.frame.edit_group_button.config(command=self.edit_group)
        self.frame.back_button.config(command=self.back)

    def back(self):
        self.model.trigger_event("deselect_group")
        self.model.trigger_event("page_loaded")
        self.view.switch("home")

    def add_expense(self):
        self.model.trigger_event("create_expense_page_loaded")
        self.view.switch("create_expense")

    def edit_group(self):
        self.model.trigger_event("edit_group_page_loaded")
        self.view.switch("create_group")

    def update_view(self):
        transactions = self.model.current_group.calculate_min_transfers()
        treeview_data = self.model.current_group.shape_data_for_treeview(transactions)

        self.frame.member_tree.delete(*self.frame.member_tree.get_children())

        for member, owes in treeview_data.items():
            # Temp here but will create a function next time
            # Basically get the user name from id
            member_data = self.model.current_group.members[member]

            member_id = self.frame.member_tree.insert("", "end", text=member_data.name, values=("", ""))
            for owed_member, amount in owes.items():
                member_data = self.model.current_group.members[owed_member]
                self.frame.member_tree.insert(member_id, "end", text=member_data.name, values=("Owes", amount))
