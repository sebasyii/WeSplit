from tkinter import messagebox, ttk
import tkinter as tk

from group import Group
from user import User


class CreateGroupFrame(ttk.Frame):
    def __init__(self, parent, groups, group_frame):
        super().__init__(parent)
        self.place(relwidth=1, relheight=1)

        self.members = []
        self.groups = groups
        self.group_frame = group_frame

        self.create_widgets()

    def create_widgets(self):
        # Group name label
        # Group name entry
        self.group_name_label = ttk.Label(self, text="Group Name")
        self.group_name_entry = ttk.Entry(self)

        # Group description label
        # Group description entry
        self.group_description_label = ttk.Label(self, text="Group Description")
        self.group_description_entry = ttk.Entry(self)

        # Member name label
        # Member name entry
        # Add member button
        # Remove member button
        self.member_name_label = ttk.Label(self, text="Member Name")
        self.member_name_entry = ttk.Entry(self)
        self.add_member_btn = ttk.Button(self, text="Add Member", command=self.add_member)
        self.remove_member_btn = ttk.Button(self, text="Remove Member", command=self.remove_member)

        # List of members
        # Create Group button
        self.list_of_members = tk.Listbox(self, height=5)
        self.create_group_btn = ttk.Button(
            self, text="Create Group", command=self.create_group
        )

        # Create Grid
        # Use a loop to create 12 columns
        for i in range(12):
            self.columnconfigure(i, weight=1)

        # Use a loop to create 10 rows
        for i in range(10):
            self.rowconfigure(i, weight=1)

        # Place widgets
        self.group_name_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=10)
        self.group_name_entry.grid(column=1, row=0, sticky=tk.W, padx=5, pady=10)
        self.group_description_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=10)
        self.group_description_entry.grid(column=1, row=1, sticky=tk.W, padx=5, pady=10)
        self.member_name_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=10)
        self.member_name_entry.grid(column=1, row=2, sticky=tk.W, padx=5, pady=10)
        self.add_member_btn.grid(column=2, row=2, sticky=tk.W, padx=5, pady=10)
        self.remove_member_btn.grid(column=3, row=2, sticky=tk.W, padx=5, pady=10)
        self.list_of_members.grid(
            column=0, row=3, columnspan=4, sticky=tk.NSEW, padx=5, pady=10
        )
        self.create_group_btn.grid(
            column=0, row=4, columnspan=4, sticky=tk.NSEW, padx=5, pady=10
        )
    
    def add_member(self):
        member_name = self.member_name_entry.get()
        if not member_name.strip():
            messagebox.showerror("Error", "Member name cannot be empty.")
            return
        if any(char.isdigit() for char in member_name):
            messagebox.showerror("Error", "Member name cannot contain digits.")
            return
        # Check if the member name already exists both, small and capital letters
        if member_name.casefold() in self.members:
            messagebox.showerror("Error", "Member name already exists.")
            return

        self.members.append(member_name.casefold())
        self.list_of_members.insert(tk.END, member_name)
        self.member_name_entry.delete(0, tk.END)

    def remove_member(self):
        selected = self.list_of_members.curselection()
        if selected:
            self.members.remove(self.list_of_members.get(selected))
            self.list_of_members.delete(selected)

    def create_group(self):
        group_name = self.group_name_entry.get()
        group_description = self.group_description_entry.get()

        # Validation checks
        if not group_name.strip():
            messagebox.showerror("Error", "Group name cannot be empty.")
            return
        if not group_description.strip():
            messagebox.showerror("Error", "Group description cannot be empty.")
            return
        if len(self.members) <= 1:
            messagebox.showerror("Error", "There must be more than one member.")
            return

        # If validation passes, proceed to save the group details
        print("Group Name:", group_name)
        print("Group Description:", group_description)
        print("Members:", self.members)

        # Create a new group
        new_group = Group(group_name, group_description)
        for member in self.members:
            temp_user = User(member)
            new_group.add_member(temp_user)
        
        # Add the group to the list of groups
        self.groups.append(new_group)
        self.group_frame.update_group_frame_data(new_group)

        # Clear the fields after creating the group
        self.group_name_entry.delete(0, tk.END)
        self.group_description_entry.delete(0, tk.END)
        self.list_of_members.delete(0, tk.END)
        self.members.clear()

        # Raise the group_frame or perform any other action
        self.group_frame.tkraise()

    def set_group_frame(self, group_frame):
        self.group_frame = group_frame
