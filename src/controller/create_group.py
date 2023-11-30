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

        self._setup()

    def _setup(self):
        self.frame.create_group_btn.config(command=self.create_group)
        self.frame.back_btn.config(command=self.back)
        self.frame.add_member_btn.config(command=self.add_member)
        self.frame.remove_member_btn.config(command=self.remove_member)

    def create_group(self):
        group_name = self.frame.group_name_entry.get()
        group_description = self.frame.group_description_entry.get()

        if self.model.current_group:
            group = next(
                (group for group in self.model.groups.values() if group.id == self.model.current_group.id), None
            )
            group.name = group_name
            group.description = group_description
            group.update_members({member.id: member for member in self.temp_members})

            self.model.set_current_group(group.id)
            self.view.switch("group")
        else:
            if group_name and group_description:
                new_group = Group(group_name, group_description)
                for member in self.temp_members:
                    new_group.add_member(member)
                self.model.add_group(new_group)
                self.model.set_current_group(new_group.id)

                self.view.switch("group")
        self.temp_members.clear()  # Clear temporary members after group creation

    def back(self):
        if self.model.current_group:
            self.view.switch("group")
            self.temp_members.clear()
        else:
            self.view.switch("home")

    def add_member(self):
        member_name = self.frame.member_name_entry.get()
        # TODO: validation
        if member_name:
            member = User(member_name)
            self.temp_members.append(member)
            self.frame.list_of_members.insert("end", member_name)
            self.frame.member_name_entry.delete(0, "end")

    def remove_member(self):
        selected = self.frame.list_of_members.curselection()
        if selected:
            index = selected[0]
            self.frame.list_of_members.delete(index)
            self.temp_members.pop(index)

    def update_view(self):
        if self.model.current_group:
            self.frame.group_name_entry.delete(0, "end")
            self.frame.group_name_entry.insert(0, self.model.current_group.group_name)
            self.frame.group_description_entry.delete(0, "end")
            self.frame.group_description_entry.insert(0, self.model.current_group.group_description)
            self.frame.list_of_members.delete(0, "end")
            for member in self.model.current_group.members.values():
                self.frame.list_of_members.insert("end", member.name)
                self.temp_members.append(member)
        else:
            self.frame.group_name_entry.delete(0, "end")
            self.frame.group_description_entry.delete(0, "end")
            self.frame.list_of_members.delete(0, "end")
