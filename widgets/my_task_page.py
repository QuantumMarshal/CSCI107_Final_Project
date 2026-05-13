"""
Project Management System - My Tasks Page

This module defines the MyTaskPage class, which provides a global overview
of all tasks across all existing projects. It serves as a master list for
tracking deadlines and completion status.

"""

import customtkinter as ctk


class MyTaskPage(ctk.CTkFrame):
    """
    A task list view that have all tasks from all projects.

    This page allows the user to see everything on their plate at once,
    maintaining strict grid alignment about task descriptions and due dates.
    """
    def __init__(self, parent, manager, refresh_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.manager = manager
        self.refresh_callback = refresh_callback

        # Ensure the frame blends with the MainApplication background
        self.configure(fg_color="transparent")

        self.sort_var = ctk.StringVar(value="Default")

        # # 1. Page Header
        # self.label = ctk.CTkLabel(self, text="Task Manager",
        #                           font=ctk.CTkFont("DM Sans 14pt", size=20, weight="bold"))
        # self.label.pack(pady=(20, 10), anchor="w", padx=30)

        # 1. Page Header & Sort Controls
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=30, pady=(20, 10))

        self.label = ctk.CTkLabel(self.header_frame, text="Task Manager",
                                  font=ctk.CTkFont("DM Sans", size=20, weight="bold"))
        self.label.pack(side="left")

        # --- 2. Design-Matched Sort Menu (Matching image_71b703.png) ---
        self.sort_menu = ctk.CTkSegmentedButton(
            self.header_frame,
            values=["Default", "Date"],
            command=lambda v: self.render_all_tasks(),
            variable=self.sort_var,
            font=ctk.CTkFont("DM Sans 14pt", size=12, weight="bold"),  # Slightly larger text
            fg_color="#e5e7eb",
            selected_color="#ffffff",
            selected_hover_color="#ffffff",
            unselected_color="#e5e7eb",
            unselected_hover_color="#dadddf",
            text_color="#000000",
            border_width=4,
            corner_radius=12,
            height=40
        )
        self.sort_menu.pack(side="right")


        # 2. Table Container (The white box with border)
        self.table_container = ctk.CTkFrame(self, fg_color="#ffffff", border_width=1,
                                            border_color="#dee4e9", corner_radius=10)
        self.table_container.pack(fill="both", expand=True, padx=30, pady=20)

        # 3. Table Header Bar
        self.table_header = ctk.CTkFrame(self.table_container, fg_color="transparent", height=40)
        self.table_header.pack(fill="x", padx=10, pady=(10, 0))

        # Grid weights: Project(1), Title(1), Description(2), Due(1) + Scrollbar space
        self.table_header.grid_columnconfigure(0, weight=0, minsize=50)  # Fixed Checkbox width
        self.table_header.grid_columnconfigure((1, 2, 4), weight=1)  # Equal widths
        self.table_header.grid_columnconfigure(3, weight=2)  # Double width for Desc
        self.table_header.grid_columnconfigure(5, minsize=20)  # Scrollbar buffer

        headers = ["", "Project", "Title", "Description", "Due"]
        for i, h in enumerate(headers):
            # Alignment logic: Titles and text are left-aligned; Due date is right-aligned
            sticky = "w"
            if i > 4: sticky = "e"
            ctk.CTkLabel(self.table_header, text=h,
                         font=ctk.CTkFont("DM Sans 14pt", 14, "bold"),
                         text_color="#636e72", justify="left").grid(row=0, column=i, sticky=sticky, padx=20)

        # 4. Scrollable Table Body
        self.scroll_frame = ctk.CTkScrollableFrame(self.table_container, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # MUST match the header weights exactly
        self.scroll_frame.grid_columnconfigure(0, weight=0, minsize=60)
        self.scroll_frame.grid_columnconfigure((1, 2, 4), weight=1)
        self.scroll_frame.grid_columnconfigure(3, weight=2)

        # Initial Render
        self.render_all_tasks()

    def render_all_tasks(self):
        """Clears the current view and iterates through all projects to list every task."""

        # 1. Clear existing task widgets from the scroll frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # 2. Sync with the data manager
        self.manager.get_data()
        row_idx = 0

        # 3. Nested loop: Iterate Projects -> Iterate Tasks within Projects
        all_tasks = []
        for project in self.manager.data:
            project_name = project.get_name()
            tasks = project.get_tasks()

            for task in tasks:
                # Task structure: [Title, Desc, Due, is_done]
                all_tasks.append({
                    "project_name": project_name,
                    "task_data": task
                })

        selection = self.sort_var.get()

        if selection == "Date":
            # Sort by date string; invalid dates go to bottom
            all_tasks.sort(key = lambda x: x["task_data"][2])

        for row_idx, item in enumerate(all_tasks):
            project_name = item["project_name"]
            task = item["task_data"]
            is_done = task[3]
            check_var = ctk.BooleanVar(value=is_done)

            # Column 0: Checkbox
            checkbox = ctk.CTkCheckBox(
                self.scroll_frame,
                text="",
                width=20,
                variable=check_var,
                command=lambda n=project_name, t=task[0]:
                        self.manager.update_task_status(n,t)
            )
            checkbox.grid(row=row_idx, column=0, sticky="nw", padx=(20, 0), pady=10)

            # Column 1: Project Name
            ctk.CTkLabel(self.scroll_frame, text=project_name, font=("DM Sans 14pt", 14, "bold")).grid(
                row=row_idx, column=1, sticky="nw", padx=20, pady=10)

            # Column 2: Task Title
            ctk.CTkLabel(self.scroll_frame, text=task[0], font=("DM Sans 14pt", 14, "bold")).grid(
                row=row_idx, column=2, sticky="nw", padx=20, pady=10)

            # Column 3: Description
            ctk.CTkLabel(self.scroll_frame, text=task[1], wraplength=350, justify="left",
                         font=("DM Sans 14pt", 14)).grid(row=row_idx, column=3, sticky="nw", padx=20, pady=10)

            # Column 4: Due Date
            ctk.CTkLabel(self.scroll_frame, text=task[2], font=("DM Sans 14pt", 14)).grid(
                row=row_idx, column=4, sticky="ne", padx=20, pady=10)

