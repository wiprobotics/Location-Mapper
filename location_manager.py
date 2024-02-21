import tkinter as tk
from tkinter import ttk, messagebox
import os

class Location:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.links = []  # Each link is a tuple: (location, link_type)

    def add_link(self, other_location, link_type=""):
        self.links.append((other_location, link_type))
        other_location.links.append((self, link_type))

    def remove_link(self, other_location):
        for link in self.links:
            if link[0] == other_location:
                self.links.remove(link)
                other_location.links.remove((self, link[1]))

    def save_to_file(self):
        filename = f"Locations/{self.name}.txt"
        with open(filename, "w") as file:
            file.write(f"Name: {self.name}\n")
            if self.description:
                file.write(f"Description: {self.description}\n")
            for link, link_type in self.links:
                file.write(f"Link: {link.name} ({link_type})\n")

    def find_link_type(self, other_location):
        for link, link_type in self.links:
            if link == other_location:
                return link_type
        return None

class LocationManager:
    def __init__(self):
        self.locations = []

    def add_location(self, name, description=""):
        new_location = Location(name, description)
        self.locations.append(new_location)
        return new_location

    def load_locations(self):
        for filename in os.listdir("Locations"):
            full_path = os.path.join("Locations", filename)
            if filename.endswith(".txt"):
                with open(full_path, "r") as file:
                    name = file.readline().strip().split(": ")[1]
                    description = ""
                    for line in file:
                        if line.startswith("Description:"):
                            description = line.strip().split(": ")[1]
                            break
                    new_location = self.add_location(name, description)
                    file.seek(0)
                    for line in file:
                        if line.startswith("Link: "):
                            parts = line.strip().split(": ")
                            if len(parts) >= 2:  # Ensure there are at least two elements
                                link_name = parts[1].split(" (")[0]
                                link_type = parts[1].split(" (")[1][:-1] if len(parts[1].split(" (")) > 1 else ""
                                linked_location = self.find_location(link_name)
                                if linked_location:
                                    new_location.add_link(linked_location, link_type)

    def find_location(self, name):
        for location in self.locations:
            if location.name == name:
                return location
        return None

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Location Manager")
        self.location_manager = LocationManager()
        self.location_manager.load_locations()
        self.location_manager.locations.sort(key=lambda x: x.name)
        self.current_location = None

        self.name_label = tk.Label(self, text="Name:")
        self.name_label.grid(row=0, column=0, sticky="w")
        self.name_entry = tk.Entry(self, width=75)
        self.name_entry.grid(row=0, column=1)

        self.description_label = tk.Label(self, text="Description:")
        self.description_label.grid(row=1, column=0, sticky="w")
        self.description_entry = tk.Entry(self, width=75)
        self.description_entry.grid(row=1, column=1)

        self.add_location_button = tk.Button(self, text="Add Location", command=self.add_location, width=25)
        self.add_location_button.grid(row=2, column=0, columnspan=2)

        self.location_menu_label = tk.Label(self, text="Select Location:")
        self.location_menu_label.grid(row=3, column=0, sticky="w")
        self.location_var = tk.StringVar()
        self.location_dropdown = ttk.Combobox(self, textvariable=self.location_var, state="readonly", width=50)
        self.location_dropdown.grid(row=3, column=1)
        self.location_dropdown.bind("<<ComboboxSelected>>", self.select_location)

        self.link_menu_label = tk.Label(self, text="Link to:")
        self.link_menu_label.grid(row=4, column=0, sticky="w")
        self.link_var = tk.StringVar()
        self.link_dropdown = ttk.Combobox(self, textvariable=self.link_var, state="readonly", width=50)
        self.link_dropdown.grid(row=4, column=1)

        self.link_type_label = tk.Label(self, text="Link Type:")
        self.link_type_label.grid(row=5, column=0, sticky="w")
        self.link_type_entry = tk.Entry(self, width=50)
        self.link_type_entry.grid(row=5, column=1)

        self.link_button = tk.Button(self, text="Link Locations", command=self.link_locations, width=25)
        self.link_button.grid(row=6, column=0, columnspan=2)

        self.link_frame = tk.Frame(self)
        self.link_frame.grid(row=7, column=0, columnspan=2)

        self.link_type_listbox_label = tk.Label(self.link_frame, text="Linked Location & Link Type:")
        self.link_type_listbox_label.grid(row=0, column=0)
        self.link_type_listbox = tk.Listbox(self.link_frame, width=35)
        self.link_type_listbox.grid(row=0, column=2)

        self.link_listbox = tk.Listbox(self.link_frame, width=35)
        self.link_listbox.grid(row=0, column=1)

        self.delete_link_button = tk.Button(self, text="Delete Link", command=self.delete_link, width=25)
        self.delete_link_button.grid(row=9, column=1, columnspan=2)

        self.save_frame = tk.Frame(self)
        self.save_frame.grid(row=10, column=0, columnspan=2)

        self.save_button = tk.Button(self.save_frame, text="Save This One", command=self.save_location)
        self.save_button.grid(row= 0, column=0)
        self.save_all_button = tk.Button(self.save_frame, text="Save All", command=self.save_all_locations)
        self.save_all_button.grid(row= 0, column=1)
        self.save_quit_button = tk.Button(self.save_frame, text="Save & Quit", command=self.save_and_quit)
        self.save_quit_button.grid(row=0, column=2)

        self.populate_location_dropdown()

    def add_location(self):
        name = self.name_entry.get()
        description = self.description_entry.get()
        if name:
            new_location = self.location_manager.add_location(name, description)
            self.populate_location_dropdown()
            self.name_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)

    def populate_location_dropdown(self):
        self.location_dropdown["values"] = [location.name for location in self.location_manager.locations]
        self.link_dropdown["values"] = [location.name for location in self.location_manager.locations]

    def select_location(self, event=None):
        selected_location_name = self.location_var.get()
        self.current_location = self.location_manager.find_location(selected_location_name)
        self.update_linked_locations()

    def update_linked_locations(self):
        self.link_listbox.delete(0, tk.END)
        self.link_type_listbox.delete(0, tk.END)
        if self.current_location:
            for link, link_type in self.current_location.links:
                self.link_listbox.insert(tk.END, link.name)
                if link_type:  # Check if link type is not empty
                    self.link_type_listbox.insert(tk.END, link_type)
                else:
                    self.link_type_listbox.insert(tk.END, "N/A")  # Insert "N/A" if link type is empty

    def link_locations(self):
        selected_link_name = self.link_var.get()
        selected_link = self.location_manager.find_location(selected_link_name)
        link_type = self.link_type_entry.get()
        if self.current_location and selected_link:
            self.current_location.add_link(selected_link, link_type)
            self.update_linked_locations()

    def delete_link(self):
        selected_index = self.link_listbox.curselection()
        if selected_index:
            selected_link_name = self.link_listbox.get(selected_index)
            selected_link = self.location_manager.find_location(selected_link_name)
            if self.current_location and selected_link:
                self.current_location.remove_link(selected_link)
                self.update_linked_locations()

    def save_location(self):
        if self.current_location:
            self.current_location.save_to_file()

    def save_all_locations(self):
        for location in self.location_manager.locations:
            location.save_to_file()

    def save_and_quit(self):
        self.save_location()
        self.quit()


if __name__ == "__main__":
    if not os.path.exists("Locations"):
        os.makedirs("Locations")
    app = Application()
    app.mainloop()
