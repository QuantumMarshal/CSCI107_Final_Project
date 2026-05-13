"""
Project Management System - Dashboard Page

This module defines the DashboardPage class, which serves as the primary
user interface for viewing project statistics, navigating active projects,
and monitoring upcoming tasks.

"""

import customtkinter as ctk
from .card import CustomCard
from .toplevel import CustomProjectLevel
from .project_page import ProjectPage

from manager import Manager

class DashboardPage(ctk.CTkFrame):
    """
    A frame representing the dashboard view of the application.

    Attributes:
        parent: The master container (MainApplication).
        manager: Instance of the Manager class for data operations.
        refresh_callback: Function to trigger UI updates across the app.
    """
    def __init__(self, parent, manager, refresh_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.manager = manager
        self.refresh_callback = refresh_callback

        # Initialize UI components
        self.create_widget()

        print(f"DashboardPage created successfully")

    def create_widget(self):
        """Initializes and packs all widgets within the Dashboard view."""

        # User Greeting
        self.label = ctk.CTkLabel(self, text="Good morning, Harry",
                                  font=ctk.CTkFont("DM Sans 14pt", size=20, weight="bold"), justify="left")
        self.label.pack(pady=20, anchor="w", padx=20)

        # Header Section (Title and New Project Button)
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

        # Button to trigger New Project Toplevel
        self.new_project_btn = ctk.CTkButton(
            self.header_frame,
            text="New Project ＋",
            font=ctk.CTkFont("DM Sans 14pt", size=14, weight="bold"),
            fg_color="#ffffff",
            text_color="#212124",
            hover_color="#dee4e9",
            corner_radius=8,
            height=40,
            border_width=2,
            border_color="#e7e9eb",
            command=self.open_create_window
        )
        self.new_project_btn.grid(row=0, column=2, rowspan=2, padx=20, sticky="e")

        # Main Content Area
        self.main_frame = ctk.CTkFrame(self, fg_color="#ffffff", corner_radius=0)
        self.main_frame.pack(fill="both", padx=2, pady=10)

        # Statistics Cards (Total, Ended, Running, Pending)
        self.card_title = ["Total Projects", "Ended Projects", "Running Projects", "Pending Projects"]
        self.card_value = [self.manager.cal_project(), 0, self.manager.cal_project(), 0]
        self.card = []
        self.reload_card()

        # Scrollable Project List
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
        self.projects_list.configure(width=0)

        # UI Adjustments for scrollbar spacing and focus rings
        self.projects_list._scrollbar.grid_configure(padx=(0, 10), pady=10)
        self.projects_list._parent_canvas.xview_moveto(0)
        self.projects_list._parent_canvas.configure(highlightthickness=0)

        # Upcoming Tasks Panel (Sidebar-style panel on the right)
        self.tasks_panel = ctk.CTkFrame(
            self.main_frame,
            fg_color="#ffffff",
            border_width=2,
            border_color="#e7e9eb",
            corner_radius=15
        )
        self.tasks_panel.grid(row=1, column=3, sticky="nsew", padx=(10, 0), pady=10)

        self.tasks_label = ctk.CTkLabel(
            self.tasks_panel,
            text="Upcoming Tasks",
            font=ctk.CTkFont("DM Sans", 16, "bold")
        )
        self.tasks_label.pack(pady=15)

        # Initial data render
        self.reload_dashboard()


    def open_create_window(self):
        """Opens the Toplevel window to add a new project."""
        CustomProjectLevel(self, self.manager, self.refresh_callback)

    def reload_card(self):
        """Instantiates the metric cards at the top of the dashboard."""
        for i in range(0, 4):
            self.card.append(CustomCard(self.main_frame, fg_color="#F8FAFB", corner_radius=10,
                                        title=self.card_title[i], value=self.card_value[i],
                                        border_color="#e7e9eb", border_width=2))
            self.card[i].grid(row=0, column=i, padx=(10, 0), pady=(10, 0))

    def reload_dashboard(self):
        """Clears the project list and re-renders buttons based on the current JSON data."""
        # 1. Clear existing widgets
        for widget in self.projects_list.winfo_children():
            widget.destroy()

        # 2. Get latest data
        self.manager.get_data()

        # 3. Create navigation buttons for each project
        for project in self.manager.data:
            project_name = project.get_name()

            project_btn = ctk.CTkButton(
                self.projects_list,
                text=f"  {project_name}",
                font=ctk.CTkFont("DM Sans 14pt", 14, "bold"),
                anchor="w",
                fg_color="#F8FAFB",
                text_color="#212124",
                hover_color="#dee4e9",
                height=60,
                corner_radius=10,
                border_width=2,
                border_color="#e7e9eb",
                command=lambda p=project_name: self.switch_project_page(p)
            )
            project_btn.pack(fill="x", padx=10, pady=5)

        # Update card values (running logic currently mirrors total projects)
        self.card_value = [self.manager.cal_project(), 0, self.manager.cal_project(), 0]

    def switch_project_page(self, project_name):
        """Communicates with MainApplication to swap the current view to a ProjectPage."""
        print(f"Switch Project Page in DashboardPage: Switching to {project_name}")
        self.parent.master.sidebar.select_button(project_name)
        self.parent.master.switch_page(ProjectPage, project_name=project_name)