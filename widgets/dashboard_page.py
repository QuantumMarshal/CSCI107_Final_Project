import customtkinter as ctk
from .card import CustomCard
from .toplevel import CustomProjectLevel
from .project_page import ProjectPage

from manager import Manager

class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, manager, refresh_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.manager = manager
        self.refresh_callback = refresh_callback

        self.create_widget()

        print(f"DashboardPage created successfully")

    def create_widget(self):
        self.label = ctk.CTkLabel(self, text="Good morning, Harry",
                                  font=ctk.CTkFont("DM Sans 14pt", size=20, weight="bold"), justify="left")
        self.label.pack(pady=20, anchor="w", padx=20)

        self.header_frame = ctk.CTkFrame(self, fg_color="#f8fafb", corner_radius=0, border_width=2,
                                         border_color="#e7e9eb")
        self.header_frame.pack(fill="x")

        self.header_frame_label1 = ctk.CTkLabel(self.header_frame, text="Dashboard",
                                                font=ctk.CTkFont("DM Sans 14pt", size=14, weight="bold"), height=15)
        self.header_frame_label1.grid(row=0, column=0, sticky="w", padx=20, pady=(10, 0))

        self.header_frame_label2 = ctk.CTkLabel(self.header_frame, text="Manage your projects and tasks",
                                                font=ctk.CTkFont("DM Sans 14pt Medium", size=12), text_color="#4c515f",
                                                height=15)
        self.header_frame_label2.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 10))

        self.header_frame.columnconfigure(1, weight=1)

        self.new_project_btn = ctk.CTkButton(
            self.header_frame,
            text="New Project ＋",
            font=ctk.CTkFont("DM Sans 14pt", size=14, weight="bold"),  # Increased size
            fg_color="#ffffff",
            text_color="#212124",
            hover_color="#dee4e9",
            corner_radius=8,
            height=40,  # Slightly taller for a 'bigger' feel
            border_width=2,
            border_color="#e7e9eb",
            command=self.open_create_window
        )
        self.new_project_btn.grid(row=0, column=2, rowspan=2, padx=20, sticky="e")

        self.main_frame = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=0)
        self.main_frame.pack(fill="both", padx=2, pady=10)

        self.card_title = ["Total Projects", "Ended Projects", "Running Projects", "Pending Projects"]
        self.card_value = [self.manager.cal_project(), 0, self.manager.cal_project(), 0]
        self.card = []
        self.reload_card()

        self.projects_list = ctk.CTkScrollableFrame(
            self.main_frame,
            fg_color="#ffffff",
            label_text="Projects",
            label_font=ctk.CTkFont("DM Sans 14pt", 16, weight="bold"),
            label_text_color="#212124",
            label_fg_color="#e7e9eb",
            border_width=2,
            border_color="#e7e9eb",
            corner_radius=15,
            scrollbar_button_color="#e7e9eb",
            scrollbar_button_hover_color="#dee4e9",
            scrollbar_fg_color="transparent"
        )

        self.projects_list.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=(10, 0), pady=10)

        # 1. Pushes the content (the list) away from the right edge
        # This uses the high-level CTk method which is safer
        self.projects_list.configure(width=0)

        # 2. Reach the scrollbar and give it some breathing room
        # CustomTkinter uses grid to place the scrollbar inside the frame
        self.projects_list._scrollbar.grid_configure(padx=(0, 10), pady=10)

        # 3. Add internal padding to the content area (where projects appear)
        # We do this by targeting the internal 'view' frame
        self.projects_list._parent_canvas.xview_moveto(0)  # Reset view
        self.projects_list._parent_canvas.configure(highlightthickness=0)  # Remove ugly focus ring

        # 3. Create the Upcoming Tasks Frame (Right Side)
        self.tasks_panel = ctk.CTkFrame(
            self.main_frame,
            fg_color="#ffffff",
            border_width=2,
            border_color="#e7e9eb",
            corner_radius=15
        )
        self.tasks_panel.grid(row=1, column=3, sticky="nsew", padx=(10, 0), pady=10)

        # Add the title for the tasks panel
        self.tasks_label = ctk.CTkLabel(
            self.tasks_panel,
            text="Upcoming Tasks",
            font=ctk.CTkFont("DM Sans", 16, "bold")
        )
        self.tasks_label.pack(pady=15)

        self.reload_dashboard()


    def open_create_window(self):
        CustomProjectLevel(self, self.manager, self.refresh_callback)

    def reload_card(self):
        for i in range(0, 4):
            self.card.append(CustomCard(self.main_frame, fg_color="#F8FAFB", corner_radius=10,
                                        title=self.card_title[i], value=self.card_value[i],
                                        border_color="#e7e9eb", border_width=2))
            self.card[i].grid(row=0, column=i, padx=(10, 0), pady=(10, 0))

    def reload_dashboard(self):
        # 1. Clear existing widgets in the scrollable frame
        for widget in self.projects_list.winfo_children():
            widget.destroy()

        # 2. Get latest data from the Manager
        self.manager.get_data()

        # 3. Create a button for every project in the JSON database
        for project in self.manager.data:
            project_name = project.get_name()

            # Create the button
            project_btn = ctk.CTkButton(
                self.projects_list,
                text=f"  {project_name}",  # Space for 'icon' feel
                font=ctk.CTkFont("DM Sans 14pt", 14, "bold"),
                anchor="w",  # Align text to the left
                fg_color="#F8FAFB",
                text_color="#212124",
                hover_color="#dee4e9",
                height=60,
                corner_radius=10,
                border_width=2,
                border_color="#e7e9eb",
                # Use a lambda with a default value to capture the specific project name
                command=lambda p=project_name: self.switch_project_page(p)
            )

            # Pack with padding to create the list look
            project_btn.pack(fill="x", padx=10, pady=5)

        self.card_value = [self.manager.cal_project(), 0, self.manager.cal_project(), 0]

    def switch_project_page(self, project_name):
        print(f"Switch Project Page in DashboardPage: Switching to {project_name}")
        self.parent.master.sidebar.select_button(project_name)
        self.parent.master.switch_page(ProjectPage, project_name=project_name)

