"""
Project Management System - Project Specific Page

This module defines the ProjectPage class, which displays detailed information
about a single project, including its description and a managed list of tasks
with status tracking.

Author: Nguyen Quang Nhan Pham
Date: 05/13/2026
"""

import customtkinter as ctk
from .toplevel import CustomTaskLevel


class ProjectPage(ctk.CTkFrame):
    """
    A detailed view for an individual project.

    This frame serves as a central hub for specific project orchestration,
    allowing users to view descriptions, add new tasks, and toggle task completion
    statuses through a persistent database interface.
    """

    def __init__(self, parent, manager, refresh_callback, project_name="Project Name", **kwargs):
        super().__init__(parent, **kwargs)
        self.manager = manager
        self.refresh_callback = refresh_callback

        # Initialize project data from the Manager engine
        self.project_name = project_name
        self.project_description = self.manager.get_description(project_name)

        # Build UI and populate task data
        self.create_widgets()
        self.render_tasks()

    def create_widgets(self):
        """Constructs the visual hierarchy including headers, descriptions, and the task table."""

        # 1. Header Section: Project Title and Task Creation
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=(20, 8))

        # Column configuration to push 'New Task' button to the far right
        self.header_frame.grid_columnconfigure(0, weight=0)  # Title
        self.header_frame.grid_columnconfigure(1, weight=1)  # Spacer
        self.header_frame.grid_columnconfigure(2, weight=0)  # Button

        self.title_label = ctk.CTkLabel(self.header_frame, text=self.project_name,
                                        font=ctk.CTkFont("DM Sans 14pt", 20, "bold"))
        self.title_label.grid(row=0, column=0, sticky="w")

        self.new_task_btn = ctk.CTkButton(self.header_frame, text="New Task ＋",
                                          fg_color="#ffffff",
                                          text_color="#212124",
                                          hover_color="#dee4e9",
                                          corner_radius=8,
                                          height=40,
                                          border_width=2,
                                          border_color="#e7e9eb",
                                          font=ctk.CTkFont("DM Sans 14pt", size=14, weight="bold"),
                                          command=self.open_new_task_popup)
        self.new_task_btn.grid(row=0, column=2, padx=20, sticky="e")

        # Decorative separator line
        ctk.CTkFrame(self, height=2, fg_color="#dee4e9").pack(fill="x")

        # 2. Project Description Section
        desc_text = f"Description: {self.project_description if self.project_description else 'None'}"
        self.desc_label = ctk.CTkLabel(self, text=desc_text,
                                       font=ctk.CTkFont("DM Sans 14pt", 14),
                                       anchor="w",
                                       wraplength=1000,
                                       justify="left")
        self.desc_label.pack(fill="x", padx=20, pady=(20, 20))

        # 3. Task Table Container: Bordered and Rounded
        self.table_container = ctk.CTkFrame(self, fg_color="#ffffff", border_width=1,
                                            border_color="#e7e9eb", corner_radius=10)
        self.table_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # 4. Table Static Header
        self.table_header = ctk.CTkFrame(self.table_container, fg_color="transparent", height=40)
        self.table_header.pack(fill="x", padx=10, pady=(10, 0))

        # Configure columns: 0(Check), 1(Title), 2(Description), 3(Due)
        self.table_header.grid_columnconfigure(0, weight=0, minsize=50)
        self.table_header.grid_columnconfigure((1, 3), weight=1)
        self.table_header.grid_columnconfigure(2, weight=2)
        self.table_header.grid_columnconfigure(4, minsize=20)  # Space for scrollbar

        headers = ["", "Title", "Description", "Due"]
        for i, h in enumerate(headers):
            # Align checkbox/title/desc to the left, due date to the right
            sticky = "w" if i < 2 else "e"
            ctk.CTkLabel(self.table_header, text=h,
                         font=ctk.CTkFont("DM Sans 14pt", 14, "bold"),
                         text_color="#636e72").grid(row=0, column=i, sticky=sticky, padx=20)

        # 5. Dynamic Scrollable Table Body
        self.scroll_frame = ctk.CTkScrollableFrame(self.table_container, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Maintain grid alignment with the header
        self.scroll_frame.grid_columnconfigure(0, weight=0, minsize=50)
        self.scroll_frame.grid_columnconfigure((1, 3), weight=1)
        self.scroll_frame.grid_columnconfigure(2, weight=2)

    def open_new_task_popup(self):
        """Launches the Toplevel entry window for adding a task to this project."""
        print(f"ProjectPage: Initializing task creation for {self.project_name}")
        CustomTaskLevel(self, self.manager, self.render_tasks, self.project_name)

    def render_tasks(self):
        """Fetches latest data and re-populates the scrollable task list."""
        # Clear current row widgets to avoid duplicates or memory leaks
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Sync with manager data engine
        self.manager.get_data()

        # Locate the specific project object within the manager's dataset
        project_data = None

        # Iterate through data list
        for p in self.manager.data:
            if p.get_name() == self.project_name:
                project_data = p
                break  # Exit the loop once the project is found

        idx = 0

        for task in project_data.get_tasks():
            # task array structure: [Title, Desc, Due Date, Status]
            t_title, t_desc, t_due, is_done = task[0], task[1], task[2], task[3]
            self.add_task_row(idx, t_title, t_desc, t_due, is_done)
            idx += 1

    def add_task_row(self, row_index, title, description, due, is_done):
        """
        Creates a single task row in the scrollable table.

        Args:
            row_index (int): The vertical grid position.
            title (str): The task name identifier.
            description (str): Detailed text about the task.
            due (str): The formatted date string.
            is_done (bool): The completion status for the checkbox.
        """
        check_var = ctk.BooleanVar(value=is_done)

        # Column 0: Checkbox
        checkbox = ctk.CTkCheckBox(
            self.scroll_frame, text="", width=20, variable=check_var,
            command=lambda name=title: self.manager.update_task_status(self.project_name, name)
        )
        checkbox.grid(row=row_index, column=0, sticky="nw", padx=20, pady=10)

        # Column 1: Title
        ctk.CTkLabel(self.scroll_frame, text=title, font=("DM Sans 14pt", 14, "bold")).grid(
            row=row_index, column=1, sticky="nw", padx=20, pady=10
        )

        # Column 2: Description
        desc_label = ctk.CTkLabel(
            self.scroll_frame,
            text=description,
            wraplength=500,
            justify="left",
            font=("DM Sans 14pt", 14)
        )
        desc_label.grid(row=row_index, column=2, sticky="nw", padx=20, pady=10)

        # Column 3: Due Date
        ctk.CTkLabel(self.scroll_frame, text=due, font=("DM Sans 14pt", 14)).grid(
            row=row_index, column=3, sticky="ne", padx=20, pady=10
        )