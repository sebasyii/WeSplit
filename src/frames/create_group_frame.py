from tkinter import messagebox, ttk
import tkinter as tk

import frames.mainframe as mainframe

from group import Group
from user import User


class CreateGroupFrame(ttk.Frame):
    """
    A frame for creating a new group in WeSplit

    Attributes:
        parent (ttk.Frame): The parent frame or widget.
        groups (list): The list of existing groups.
        group_frame (ttk.Frame): The frame that displays group information.

    Methods:
        create_widgets: Creates and lays out widgets.
        configure_grid: Configures grid layout for the frame.
        add_member: Adds a member to the group.
        remove_member: Removes a selected member from the group.
        create_group: Creates a new group with the given details.
        set_group_frame: Sets the group frame to display group information.
    """

    def __init__(self, parent, groups, group_frame):
        """
        Initialise the CreateGroupFrame with parent, groups, and group_frame.

        Args:
            parent (ttk.Frame): The parent frame or widget.
            groups (list): The list of existing groups.
            group_frame (ttk.Frame): The frame that displays group information.
        """
        super().__init__(parent)
        self.place(relwidth=1, relheight=1)

        self.members = []
        self.groups = groups
        self.group_frame = group_frame

        self.create_widgets()

    def create_widgets(self) -> None:
        """Creates and arranges widgets for group creation."""
        self.back_btn = ttk.Button(self, text="Back", command=self.back_to_mainframe)

        self.group_name_label = ttk.Label(self, text="Group Name")
        self.group_name_entry = ttk.Entry(self)

        self.group_description_label = ttk.Label(self, text="Group Description")
        self.group_description_entry = ttk.Entry(self)

        self.member_name_label = ttk.Label(self, text="Member Name")
        self.member_name_entry = ttk.Entry(self)
        self.add_member_btn = ttk.Button(self, text="Add Member", command=self.add_member)
        self.remove_member_btn = ttk.Button(self, text="Remove Member", command=self.remove_member)

        self.list_of_members = tk.Listbox(self, height=10)
        self.create_group_btn = ttk.Button(self, text="Create Group", command=self.create_group)

        self.configure_grid()

        # Place widgets
        self.back_btn.grid(column=0, row=0, sticky=tk.W, padx=10, pady=10)
        self.group_name_label.grid(column=0, row=1, sticky=tk.W, padx=10, pady=10)
        self.group_name_entry.grid(column=1, row=1, sticky=tk.W, padx=10, pady=10)
        self.group_description_label.grid(column=0, row=2, sticky=tk.W, padx=10, pady=10)
        self.group_description_entry.grid(column=1, row=2, sticky=tk.W, padx=10, pady=10)
        self.member_name_label.grid(column=0, row=3, sticky=tk.W, padx=10, pady=10)
        self.member_name_entry.grid(column=1, row=3, sticky=tk.W, padx=10, pady=10)
        self.add_member_btn.grid(column=2, row=3, sticky=tk.W, padx=10, pady=10)
        self.remove_member_btn.grid(column=3, row=3, sticky=tk.W, padx=10, pady=10)
        self.list_of_members.grid(column=0, row=4, columnspan=12, rowspan=5, sticky=tk.NSEW, padx=10, pady=10)
        self.create_group_btn.grid(column=10, row=9, columnspan=2, sticky=tk.NSEW, padx=10, pady=10)

    def configure_grid(self) -> None:
        """Configure grid layout for Create Group Frame."""
        for i in range(12):
            self.columnconfigure(i, weight=1)

        for i in range(10):
            self.rowconfigure(i, weight=1)

    def back_to_mainframe(self) -> None:
        """Raise the mainframe to the top and update the group list."""
        self.mainframe.update_group_list()
        self.mainframe.tkraise()

    def update_group_frame_data(self, mainframe: "mainframe.MainFrame") -> None:
        """Update the group frame data."""
        self.mainframe = mainframe
        self.mainframe.update_group_list()

    def add_member(self) -> None:
        """Adds a new member to the group based on the input."""
        member_name = self.member_name_entry.get()
        if not member_name.strip():
            messagebox.showerror("Error", "Member name cannot be empty.")
            return
        if any(char.isdigit() for char in member_name):
            messagebox.showerror("Error", "Member name cannot contain digits.")
            return
        if member_name.casefold() in map(str.casefold, self.members):
            messagebox.showerror("Error", "Member name already exists.")
            return

        self.members.append(member_name)
        self.list_of_members.insert(tk.END, member_name)
        self.member_name_entry.delete(0, tk.END)

    def remove_member(self) -> None:
        """Removes the selected member from the group."""
        selected = self.list_of_members.curselection()
        if selected:
            self.members.remove(self.list_of_members.get(selected))
            self.list_of_members.delete(selected)

    def create_group(self) -> None:
        """Creates a new group with the provided details."""
        group_name = self.group_name_entry.get()
        group_description = self.group_description_entry.get()

        if not group_name.strip():
            messagebox.showerror("Error", "Group name cannot be empty.")
            return
        if not group_description.strip():
            messagebox.showerror("Error", "Group description cannot be empty.")
            return
        if len(self.members) <= 1:
            messagebox.showerror("Error", "There must be more than one member.")
            return

        new_group = Group(group_name, group_description)
        for member in self.members:
            temp_user = User(member)
            new_group.add_member(temp_user)

        self.groups.append(new_group)
        self.group_frame.update_group_frame_data(new_group)

        self.group_name_entry.delete(0, tk.END)
        self.group_description_entry.delete(0, tk.END)
        self.list_of_members.delete(0, tk.END)
        self.members.clear()

        self.group_frame.tkraise()

    def set_group_frame(self, group_frame) -> None:
        """
        Sets the group frame to display group information.

        Args:
            group_frame (ttk.Frame): The frame that displays group information.
        """
        self.group_frame = group_frame
