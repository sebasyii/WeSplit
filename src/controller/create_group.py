from views.main import View
from models.main import Model
from models.group import Group
from models.user import User


class CreateGroupController:
    def __init__(self, model: Model, view: View):
        self.view = view
        self.model = model
        self.frame = self.view.frames["create_group"]
        self.temp_members = []

        self._setup_event_bindings()

    def _setup_event_bindings(self):
        self.frame.create_group_btn.config(command=self._create_group)
        self.frame.back_btn.config(command=self._go_back)
        self.frame.add_member_btn.config(command=self._add_member)
        self.frame.remove_member_btn.config(command=self._remove_member)

    def _create_group(self):
        group_name, group_description = self._get_group_details()

        if self.model.current_group:
            self._update_existing_group(group_name, group_description)
        else:
            self._create_new_group(group_name, group_description)
        self.temp_members.clear()  # Clear temporary members after group creation

    def _get_group_details(self):
        return self.frame.group_name_entry.get(), self.frame.group_description_entry.get()

    def _update_existing_group(self, group_name: str, group_description: str) -> None:
        group = next((group for group in self.model.groups.values() if group.id == self.model.current_group.id), None)
        if group:
            group.name, group.description = group_name, group_description
            group.update_members({member.id: member for member in self.temp_members})
            self.model.set_current_group(group.id)
            self.view.switch("group")

    def _create_new_group(self, group_name: str, group_description: str):
        new_group = Group(group_name, group_description)
        for member in self.temp_members:
            new_group.add_member(member)
        self.model.add_group(new_group)
        self.model.set_current_group(new_group.id)
        self.view.switch("group")

    def _go_back(self):
        self.view.switch("group" if self.model.current_group else "home")
        self.temp_members.clear()

    def _add_member(self):
        member_name = self.frame.member_name_entry.get()
        if member_name:
            new_member = User(member_name)
            self.temp_members.append(new_member)
            self.frame.list_of_members.insert("end", member_name)
            self.frame.member_name_entry.delete(0, "end")

    def _remove_member(self):
        selected = self.frame.list_of_members.curselection()
        if selected:
            self.frame.list_of_members.delete(selected[0])
            self.temp_members.pop(selected[0])

    def update_view(self):
        self._clear_group_inputs()
        if self.model.current_group:
            self._populate_group_data()

    def _clear_group_inputs(self):
        self.frame.group_name_entry.delete(0, "end")
        self.frame.group_description_entry.delete(0, "end")
        self.frame.list_of_members.delete(0, "end")

    def _populate_group_data(self):
        group = self.model.current_group
        self.frame.group_name_entry.insert(0, group.name)
        self.frame.group_description_entry.insert(0, group.description)
        for member in group.members.values():
            self.frame.list_of_members.insert("end", member.name)
            self.temp_members.append(member)
