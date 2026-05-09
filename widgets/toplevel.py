import customtkinter as ctk

class CustomTopLevel(ctk.CTkToplevel):
    def __init__(self, parent, manager_instance, refresh_callback):
        super().__init__(parent)
        self.geometry("450x450")
        self.manager = manager_instance
        self.refresh_callback = refresh_callback

        self.attributes("-topmost", True)
        self.grab_set()

class CustomProjectLevel(CustomTopLevel):
    def __init__(self, parent, manager_instance, refresh_callback):
        super().__init__(parent, manager_instance, refresh_callback)
        self.title("Create New Project")

        # UI Elements
        self.label = ctk.CTkLabel(self, text="Project Title", font=("DM Sans 14pt", 14, "bold"))
        self.label.pack(pady=(20, 5))

        self.entry = ctk.CTkEntry(self, placeholder_text="e.g. Combat Robot Build", width=350)
        self.entry.pack(pady=10)

        self.desc_label = ctk.CTkLabel(self, text="Description", font=("DM Sans 14pt", 14, "bold"))
        self.desc_label.pack(pady=(10, 5))

        self.desc_entry = ctk.CTkTextbox(self, width=350, height=120, corner_radius=8,
                                         border_width=2, border_color="#949a9f")
        self.desc_entry.pack(pady=10)

        self.desc_entry.insert("0.0", "")

        self.create_btn = ctk.CTkButton(self, text="Create Project", command=self.submit)
        self.create_btn.pack(pady=20)

    def submit(self):
        title = self.entry.get()

        # CTkTextbox requires a range to get text. "1.0" is start, "end-1c" removes trailing newline.
        description = self.desc_entry.get("1.0", "end-1c")

        if title.strip():
            self.manager.create_project(title, description)
            self.refresh_callback()
            self.destroy()
        else:
            self.entry.configure(border_color="red")

class CustomTaskLevel(CustomTopLevel):
    def __init__(self, parent, manager_instance, refresh_callback, project_name):
        super().__init__(parent, manager_instance, refresh_callback)
        self.title(f"New Task: {project_name}")
        self.project_name = project_name

        # UI Elements
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

        # Added Due Date field to match your Project Page layout
        self.due_label = ctk.CTkLabel(self, text="Due Date", font=("DM Sans", 14, "bold"))
        self.due_label.pack(pady=(10, 5))

        self.due_entry = ctk.CTkEntry(self, placeholder_text="YYYY-MM-DD", width=350,
                                      border_width=2, border_color="#949a9f")
        self.due_entry.pack(pady=10)

        self.create_btn = ctk.CTkButton(self, text="Add Task", command=self.submit)
        self.create_btn.pack(pady=20)

    def submit(self):
        title = self.entry.get()
        description = self.desc_entry.get("1.0", "end-1c")
        due_date = self.due_entry.get()

        # Check for empty title
        if not title.strip():
            self.entry.configure(border_color="red")
            return

        # Check for valid date format
        if not self.manager.is_valid_date(due_date):
            self.due_entry.configure(border_color="#FF4C4C")  # Bright Red
            # Optional: Add a small error label or tooltip here
            print("Invalid Date Format. Please use YYYY-MM-DD.")
            return

        # If both are valid, proceed to save
        self.manager.create_task(self.project_name, title, description, due_date)
        self.refresh_callback()
        self.destroy()
