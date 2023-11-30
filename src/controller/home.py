from views.main import View
from models.main import Model


class HomeController:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.frame = self.view.frames["home"]
        self._setup()

    def _setup(self):
        self.frame.create_grp_btn.config(command=self.create_group)
        self.frame.select_grp_btn.config(command=self.select_group)
        self.frame.leave_grp_btn.config(command=self.leave_group)

    # View methods
    def create_group(self):
        self.model.trigger_event("edit_group_page_loaded")
        self.view.switch("create_group")

    def select_group(self):
        selected = self.frame.groups_listbox.curselection()
        if selected:
            group_id = selected[0]
            selected_group = list(self.model.groups.keys())[group_id]
            self.model.set_current_group(self.model.groups[selected_group].id)
            self.model.trigger_event("group_selected")
            self.view.switch("group")

    def leave_group(self):
        selected = self.frame.groups_listbox.curselection()
        if selected:
            group_id = selected[0]
            selected_group = list(self.model.groups.keys())[group_id]
            self.model.remove_group(self.model.groups[selected_group].id)
            self.model.trigger_event("group_left")

    def update_view(self):
        self.frame.groups_listbox.delete(0, "end")
        for group in self.model.groups.values():
            self.frame.groups_listbox.insert("end", group.group_name)
