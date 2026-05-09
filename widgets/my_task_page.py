import customtkinter as ctk


class MyTaskPage(ctk.CTkFrame):
    def __init__(self, parent, manager, refresh_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.manager = manager
        self.refresh_callback = refresh_callback
        self.configure(fg_color="transparent")

        # 1. Page Header
        self.label = ctk.CTkLabel(self, text="Task Manager",
                                  font=ctk.CTkFont("DM Sans", size=20, weight="bold"))
        self.label.pack(pady=(20, 10), anchor="w", padx=30)

        # 2. Table Container (The white box with border)
        self.table_container = ctk.CTkFrame(self, fg_color="#ffffff", border_width=1,
                                            border_color="#dee4e9", corner_radius=10)
        self.table_container.pack(fill="both", expand=True, padx=30, pady=20)

        # 3. Table Header Bar
        self.table_header = ctk.CTkFrame(self.table_container, fg_color="transparent", height=40)
        self.table_header.pack(fill="x", padx=10, pady=(10, 0))

        # Grid weights: Project(1), Title(1), Description(2), Due(1) + Scrollbar space
        self.table_header.grid_columnconfigure((0, 1, 3), weight=1)
        self.table_header.grid_columnconfigure(2, weight=2)
        self.table_header.grid_columnconfigure(4, minsize=20)  # Scrollbar offset

        headers = ["Project", "Title", "Description", "Due"]
        for i, h in enumerate(headers):
            # Align Project, Title, Desc to West(w), Due to East(e)
            sticky = "w" if i < 3 else "e"
            ctk.CTkLabel(self.table_header, text=h,
                         font=ctk.CTkFont("DM Sans 14pt", 14, "bold"),
                         text_color="#636e72").grid(row=0, column=i, sticky=sticky, padx=20)

        # 4. Scrollable Table Body
        self.scroll_frame = ctk.CTkScrollableFrame(self.table_container, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Match weights exactly
        self.scroll_frame.grid_columnconfigure((0, 1, 3), weight=1)
        self.scroll_frame.grid_columnconfigure(2, weight=2)

        # Initial Render
        self.render_all_tasks()

    def render_all_tasks(self):
        # Clear existing
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.manager.get_data()
        row_idx = 0

        # Loop through every project in your manager
        for project in self.manager.data:
            project_name = project.get_name()
            tasks = project.get_tasks()
            print(tasks)

            for task in tasks:
                # Column 0: Project Name
                ctk.CTkLabel(self.scroll_frame, text=project_name, font=("DM Sans 14pt", 14, "bold")).grid(
                    row=row_idx, column=0, sticky="nw", padx=20, pady=10)

                # Column 1: Task Title
                ctk.CTkLabel(self.scroll_frame, text=task[0], font=("DM Sans 14pt", 14, "bold")).grid(
                    row=row_idx, column=1, sticky="nw", padx=20, pady=10)

                # Column 2: Description (with wrapping)
                ctk.CTkLabel(self.scroll_frame, text=task[1], wraplength=350, justify="left",
                             font=("DM Sans 14pt", 14)).grid(row=row_idx, column=2, sticky="nw", padx=20, pady=10)

                # Column 3: Due Date
                ctk.CTkLabel(self.scroll_frame, text=task[2], font=("DM Sans 14pt", 14)).grid(
                    row=row_idx, column=3, sticky="ne", padx=20, pady=10)

                row_idx += 1
