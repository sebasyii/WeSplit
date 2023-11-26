import json
from tkinter import filedialog, ttk
import tkinter as tk

class MainFrame(ttk.Frame):
    def __init__(self, parent, groups, create_grp_frame):
        super().__init__(parent)
        self.groups = groups
        self.place(relwidth=1, relheight=1)

        self.create_widgets(create_grp_frame)

    def create_widgets(self, create_grp_frame):
        """Create and place widgets for MainFrame."""
        create_grp_btn = ttk.Button(
            self, text="Create Group", command=create_grp_frame.tkraise
        )
        self.group_list = self.create_group_list()
        select_grp_btn = ttk.Button(self, text="Select Group", command=self.select_group)
        leave_grp_btn = ttk.Button(self, text="Leave Group", command=self.leave_group)

        # Add buttons for loading and saving groups
        load_grp_btn = ttk.Button(
            self, text="Load Groups", command=self.load_groups_from_file
        )
        save_grp_btn = ttk.Button(
            self, text="Save Groups", command=self.save_groups_to_file
        )

        self.configure_grid()
        create_grp_btn.grid(column=0, columnspan=6, row=0, sticky=tk.NSEW ,padx=20)
        self.group_list.grid(column=0, columnspan=12, row=2, rowspan=8, sticky=tk.NSEW, padx=20, pady=10)
        select_grp_btn.grid(column=0, columnspan=6, row=10, rowspan=3, sticky=tk.NSEW, padx=20, pady=20)
        leave_grp_btn.grid(column=6, columnspan=6, row=11, rowspan=1, sticky=tk.NSEW, padx=20, pady=20)

        # Place the new buttons on the grid
        load_grp_btn.grid(column=0, columnspan=6, row=11, sticky=tk.NSEW, padx=20, pady=10)
        save_grp_btn.grid(column=6, columnspan=6, row=11, sticky=tk.NSEW, padx=20, pady=10)

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
    
    # Mutative methods
    def select_group(self):
        """Select a group."""
        selected = self.group_list.curselection()
        if selected:
            print(self.groups[selected[0]])
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
            title="Open Groups File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, 'r') as file:
                groups_data = json.load(file)
                # Assuming groups_data is a list of group names
                self.groups.extend(groups_data)
                self.update_group_list()

    def save_groups_to_file(self):
        """Save the current list of groups to a JSON file."""
        file_path = filedialog.asksaveasfilename(
            title="Save Groups File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, 'w') as file:
                # Assuming self.groups is a list of group names
                json.dump(list(self.groups), file)

    def update_group_list(self):
        """Update the group listbox with the current groups."""
        self.group_list.delete(0, tk.END)
        for group in self.groups:
            self.group_list.insert(tk.END, group)