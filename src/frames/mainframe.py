import json
from tkinter import filedialog, ttk
import tkinter as tk

import frames.create_group_frame as create_group_frame
import frames.group_frame as group_frame


class MainFrame(ttk.Frame):
    def __init__(self, parent, groups, create_grp_frame: "create_group_frame.CreateGroupFrame", group_frame: "group_frame.GroupFrame"):
        super().__init__(parent)
        self.groups = groups
        self.place(relwidth=1, relheight=1)

        self.create_grp_frame = create_grp_frame
        self.group_frame = group_frame

        self.create_widgets(create_grp_frame)

    def create_widgets(self, create_grp_frame):
        """Create and place widgets for MainFrame."""
        create_grp_btn = ttk.Button(self, text="Create Group", command=self.call_create_grp_frame)
        self.group_list = self.create_group_list()
        select_grp_btn = ttk.Button(self, text="Select Group", command=self.select_group)
        leave_grp_btn = ttk.Button(self, text="Leave Group", command=self.leave_group)

        load_grp_btn = ttk.Button(self, text="Load Groups", command=self.load_groups_from_file)
        save_grp_btn = ttk.Button(self, text="Save Groups", command=self.save_groups_to_file)

        self.configure_grid()
        create_grp_btn.grid(column=0, columnspan=6, row=0, sticky=tk.NSEW, padx=20)
        select_grp_btn.grid(column=0, columnspan=6, row=1, sticky=tk.NSEW, padx=20)
        leave_grp_btn.grid(column=6, columnspan=6, row=1, sticky=tk.NSEW, padx=20)
        self.group_list.grid(column=0, columnspan=12, row=2, rowspan=8, sticky=tk.NSEW, padx=20, pady=10)

        load_grp_btn.grid(column=0, columnspan=6, row=11, sticky=tk.NSEW, padx=20, pady=10)
        save_grp_btn.grid(column=6, columnspan=6, row=11, sticky=tk.NSEW, padx=20, pady=10)

    def call_create_grp_frame(self):
        """Call the create group frame."""
        self.create_grp_frame.update_group_frame_data(self)
        self.create_grp_frame.tkraise()

    def create_group_list(self):
        """Create the listbox widget for groups."""
        var = tk.Variable(value=self.groups)
        return tk.Listbox(self, listvariable=var, height=5)

    def configure_grid(self):
        """Configure grid layout for MainFrame."""
        for i in range(12):
            self.columnconfigure(i, weight=1)

        for i in range(10):
            self.rowconfigure(i, weight=1)

    def select_group(self):
        """Select a group."""
        selected = self.group_list.curselection()
        if selected:
            print(self.groups[selected[0]])
            self.group_frame.update_group_frame_data(self.groups[selected[0]])
            self.group_frame.tkraise()
            self.state(["!disabled"])
        else:
            self.state(["disabled"])

    def leave_group(self):
        """Leave a group."""
        selected = self.group_list.curselection()
        if selected:
            self.groups.pop(selected[0])
            self.group_list.delete(selected)
            print(self.group_list)

    def load_groups_from_file(self):
        """Load a list of groups from a JSON file."""
        file_path = filedialog.askopenfilename(
            title="Open Groups File", filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, "r") as file:
                groups_data = json.load(file)
                self.groups.extend(groups_data)
                self.update_group_list()

    def save_groups_to_file(self):
        """Save the current list of groups to a JSON file."""
        file_path = filedialog.asksaveasfilename(
            title="Save Groups File", filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, "w") as file:
                json.dump(list(self.groups), file)

    def update_group_list(self):
        """Update the group listbox with the current groups."""
        self.group_list.delete(0, tk.END)
        print(self.groups)
        for group in self.groups:
            self.group_list.insert(tk.END, group)
