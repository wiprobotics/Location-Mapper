import tkinter as tk
import os
from tkinter import ttk, messagebox
from location_manager import LocationManager

class LocationEditor:
    def __init__(self, location_manager):
        self.location_manager = location_manager

    def change_name(self, location, new_name):
        if not new_name:
            messagebox.showerror("Error", "New name cannot be empty.")
            return

        old_name = location.name
        location.name = new_name

        # Update links
        for linked_location in self.location_manager.locations:
            for i, (link, link_type) in enumerate(linked_location.links):
                if link.name == old_name:
                    linked_location.links[i] = (location, link_type)

        # Update filenames
        old_filename = f"{old_name}.txt"
        new_filename = f"{new_name}.txt"
        if os.path.exists(old_filename):
            os.rename(old_filename, new_filename)

        # Save all files
        for location in self.location_manager.locations:
            location.save_to_file()

        messagebox.showinfo("Success", f"Location name changed from '{old_name}' to '{new_name}'.")

    def change_description(self, location, new_description):
        location.description = new_description
        messagebox.showinfo("Success", "Description updated successfully.")

class LocationEditorUI(tk.Tk):
    def __init__(self, location_manager, location_editor):
        super().__init__()
        self.title("Location Editor")
        self.location_manager = location_manager
        self.location_editor = location_editor

        self.name_label = tk.Label(self, text="Location Name:")
        self.name_label.grid(row=0, column=0, sticky="w")
        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(self, textvariable=self.name_var, width=40)
        self.name_entry.grid(row=0, column=1)
        self.new_name_label = tk.Label(self, text="New Name:")
        self.new_name_label.grid(row=0, column=2, sticky="w")
        self.new_name_var = tk.StringVar()
        self.new_name_entry = tk.Entry(self, textvariable=self.new_name_var, width=40)
        self.new_name_entry.grid(row=0, column=3)

        self.description_label = tk.Label(self, text="Location Description:")
        self.description_label.grid(row=1, column=0, sticky="w")
        self.description_var = tk.StringVar()
        self.description_entry = tk.Entry(self, textvariable=self.description_var, width=40)
        self.description_entry.grid(row=1, column=1)
        self.new_description_label = tk.Label(self, text="New Description:")
        self.new_description_label.grid(row=1, column=2, sticky="w")
        self.new_description_var = tk.StringVar()
        self.new_description_entry = tk.Entry(self, textvariable=self.new_description_var, width=40)
        self.new_description_entry.grid(row=1, column=3)

        self.change_name_button = tk.Button(self, text="Change Name", command=self.change_name)
        self.change_name_button.grid(row=2, column=0, columnspan=2)

        self.change_description_button = tk.Button(self, text="Change Description", command=self.change_description)
        self.change_description_button.grid(row=3, column=0, columnspan=2)

    def change_name(self):
        location_name = self.name_var.get()
        new_name = self.new_name_var.get()

        location_to_edit = self.location_manager.find_location(location_name)
        if location_to_edit:
            self.location_editor.change_name(location_to_edit, new_name)
        else:
            messagebox.showerror("Error", f"Location '{location_name}' not found.")

    def change_description(self):
        location_name = self.name_var.get()
        new_description = self.description_entry.get()

        location_to_edit = self.location_manager.find_location(location_name)
        if location_to_edit:
            self.location_editor.change_description(location_to_edit, new_description)
        else:
            messagebox.showerror("Error", f"Location '{location_name}' not found.")


if __name__ == "__main__":
    location_manager = LocationManager()
    location_manager.load_locations()

    editor = LocationEditor(location_manager)

    app = LocationEditorUI(location_manager, editor)
    app.mainloop()
