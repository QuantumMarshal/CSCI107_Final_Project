"""
Project Management System - TopLevel Windows

This module contains the pop-up (Toplevel) windows used for data entry, 
including the creation of new projects and new tasks within specific projects.

"""

import customtkinter as ctk


class CustomTopLevel(ctk.CTkToplevel):
    """
    Base class for all modal pop-up windows in the application.

    Attributes:
        manager: Instance of the data manager for saving input.
        refresh_callback: Method to trigger UI updates once data is submitted.
    """

    def __init__(self, parent, manager_instance, refresh_callback):
        super().__init__(parent)
        self.geometry("450x450")
        self.manager = manager_instance
        self.refresh_callback = refresh_callback

        # Set modal behavior: window stays on top and blocks interaction with parent
        self.attributes("-topmost", True)
        self.grab_set()


class CustomProjectLevel(CustomTopLevel):
    """
    Pop-up window designed for creating a new project entry.
    """

    def __init__(self, parent, manager_instance, refresh_callback):
        super().__init__(parent, manager_instance, refresh_callback)
        self.title("Create New Project")

        # --- UI Elements ---
        self.label = ctk.CTkLabel(self, text="Project Title", font=("DM Sans 14pt", 14, "bold"))
        self.label.pack(pady=(20, 5))

        # Project title entry field
        self.entry = ctk.CTkEntry(self, placeholder_text="e.g. Combat Robot Build", width=350)
        self.entry.pack(pady=10)

        self.desc_label = ctk.CTkLabel(self, text="Description", font=("DM Sans 14pt", 14, "bold"))
        self.desc_label.pack(pady=(10, 5))

        # Project description multi-line textbox
        self.desc_entry = ctk.CTkTextbox(self, width=350, height=120, corner_radius=8,
                                         border_width=2, border_color="#949a9f")
        self.desc_entry.pack(pady=10)
        self.desc_entry.insert("0.0", "")

        self.create_btn = ctk.CTkButton(self, text="Create Project", command=self.submit)
        self.create_btn.pack(pady=20)

    def submit(self):
        """Validates project input and saves it to the JSON database."""
        title = self.entry.get()

        # CTkTextbox requires a range to get text. "1.0" is start, "end-1c" removes trailing newline.
        description = self.desc_entry.get("1.0", "end-1c")

        if title.strip():
            # Save data via manager and trigger refresh
            self.manager.create_project(title, description)
            self.refresh_callback()
            self.destroy()
        else:
            # Highlight error if title is missing
            self.entry.configure(border_color="red")


class CustomTaskLevel(CustomTopLevel):
    """
    Pop-up window designed for adding a new task to an existing project.
    """

    def __init__(self, parent, manager_instance, refresh_callback, project_name):
        super().__init__(parent, manager_instance, refresh_callback)
        self.title(f"New Task: {project_name}")
        self.project_name = project_name

        # --- UI Elements ---
        self.label = ctk.CTkLabel(self, text="Task Title", font=("DM Sans", 14, "bold"))
        self.label.pack(pady=(20, 5))

        self.entry = ctk.CTkEntry(self, placeholder_text="e.g. Design motor mounts", width=350,
                                  border_width=2, border_color="#949a9f")
        self.entry.pack(pady=10)

        self.desc_label = ctk.CTkLabel(self, text="Description", font=("DM Sans", 14, "bold"))
        self.desc_label.pack(pady=(10, 5))

        self.desc_entry = ctk.CTkTextbox(self, width=350, height=80, corner_radius=8,
                                         border_width=2, border_color="#949a9f")
        self.desc_entry.pack(pady=10)

        # Due Date entry (YYYY-MM-DD)
        self.due_label = ctk.CTkLabel(self, text="Due Date", font=("DM Sans", 14, "bold"))
        self.due_label.pack(pady=(10, 5))

        self.due_entry = ctk.CTkEntry(self, placeholder_text="YYYY-MM-DD", width=350,
                                      border_width=2, border_color="#949a9f")
        self.due_entry.pack(pady=10)

        self.create_btn = ctk.CTkButton(self, text="Add Task", command=self.submit)
        self.create_btn.pack(pady=20)

    def submit(self):
        """Validates task title and date format before saving."""
        title = self.entry.get()
        description = self.desc_entry.get("1.0", "end-1c")
        due_date = self.due_entry.get()

        # Check for empty title
        if not title.strip():
            self.entry.configure(border_color="red")
            return

        # Check for valid date format using manager's logic
        if not self.manager.is_valid_date(due_date):
            self.due_entry.configure(border_color="#FF4C4C")  # Highlight Bright Red
            print(f"Invalid Date Format in {self.project_name}. Use YYYY-MM-DD.")
            return

        # Success: Save task via manager, refresh UI, and close popup
        self.manager.create_task(self.project_name, title, description, due_date)
        self.refresh_callback()
        self.destroy()