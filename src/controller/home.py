from views.main import View
from models.main import Model


class HomeController:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view
        self.frame = self.view.frames["home"]
        self._setup_event_bindings()

    def _setup_event_bindings(self) -> None:
        self.frame.create_grp_btn.config(command=self._create_group)
        self.frame.select_grp_btn.config(command=self._select_group)
        self.frame.leave_grp_btn.config(command=self._leave_group)
        self.frame.groups_listbox.bind("<<ListboxSelect>>", lambda _: self._enable_group_modification_btn())

    def _create_group(self):
        self.model.trigger_event("edit_group_page_loaded")
        self.view.switch("create_group")

    def _select_group(self):
        selected_group = self._get_selected_group_id()
        if selected_group is not None:
            self.model.set_current_group(self.model.groups[selected_group].id)
            self.model.trigger_event("group_selected")
            self.view.switch("group")

    def _leave_group(self):
        selected_group = self._get_selected_group_id()
        print(selected_group)
        if selected_group is not None:
            self.model.remove_group(self.model.groups[selected_group].id)
            self.model.trigger_event("group_left")

    def _get_selected_group_id(self) -> int:
        selected = self.frame.groups_listbox.curselection()
        if selected:
            return list(self.model.groups.keys())[selected[0]]
        return None
    
    def _enable_group_modification_btn(self):
        self.frame.select_grp_btn.config(state="normal")
        self.frame.leave_grp_btn.config(state="normal")

    def update_view(self):
        self.frame.groups_listbox.delete(0, "end")
        self.frame.select_grp_btn.config(state="disabled")
        self.frame.leave_grp_btn.config(state="disabled")
        for group in self.model.groups.values():
            self.frame.groups_listbox.insert("end", group.name)
