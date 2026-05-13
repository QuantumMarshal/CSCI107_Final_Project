"""
Project Management System - Sidebar Navigation

This module defines the Sidebar class, which serves as the primary navigation
hub. it manages static menu items (Dashboard, Tasks) and dynamically renders
the list of active projects from the database.

"""
import customtkinter as ctk
from PIL import Image
import os

from .my_task_page import MyTaskPage
from .dashboard_page import DashboardPage
from .toplevel import CustomProjectLevel
from .project_page import ProjectPage

class Sidebar(ctk.CTkFrame):
    """
    The Sidebar widget provides global navigation and project switching logic.

    Attributes:
        parent: The MainApplication instance for page switching.
        manager: The data engine for retrieving project names.
        refresh_callback: Callback used to update UI components globally.
    """
    def __init__(self, parent, manager, refresh_callback, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.manager = manager
        self.refresh_callback = refresh_callback

        # Initialize UI components
        self.create_widgets()

    def create_widgets(self):
        """
        Constructs the sidebar layout, menu items, and dynamic project list.
        Don't have logo yet so using label
        If have logo --> Change to canvas
        """
        # Application Branding
        self.logo_label = ctk.CTkLabel(self, text="Project.",
                                       font=ctk.CTkFont("DM Sans 14pt", size=20, weight="bold"))
        self.logo_label.pack(pady=(25, 0), padx=(35, 35), anchor="w")

        # Decorative separator
        ctk.CTkFrame(self, height=2, fg_color="#dee4e9").pack(fill="x", pady=20)

        # Container for tracking button objects for state management (selection highlights)
        self.menu_buttons = {}

        # Static Navigation Items
        menu_items = [("Dashboard", self.dashboard_clicked),
                      ("My tasks", self.my_tasks_clicked),
                      # ("Documents", self.documents_clicked)
                      ]

        try:
            # Asset Path Resolution for icons
            current_dir = os.path.dirname(os.path.realpath(__file__))
            project_root = os.path.dirname(current_dir)
            image_path = os.path.join(project_root, "icons")

            for item in menu_items:
                # Load and scale icons for menu items
                icon_image = ctk.CTkImage(
                    light_image=Image.open(os.path.join(image_path, f"{item[0].lower()}.png")),
                    size=(16, 16)  # Adjust size to match your font
                )

                btn = ctk.CTkButton(self, text=item[0], fg_color="transparent",
                                    text_color="#505b62", hover_color="#dee4e9", anchor="w",
                                    corner_radius=10, height=40,
                                    image=icon_image, compound="left",  # Icon next to text
                                    command=item[1],
                                    )
                btn.pack(fill="x", padx=20, pady=5)

                # Store reference for selection styling
                self.menu_buttons[item[0]] = btn

        except Exception as e:
            print(e)

        ctk.CTkFrame(self, height=2, fg_color="#dee4e9").pack(fill="x", padx=(5, 5), pady=10)

        # --- Projects Section Header ---
        project_header_frame = ctk.CTkFrame(self, fg_color="transparent")
        project_header_frame.pack(fill="x", padx=30, pady=(10, 10))

        project_lbl = ctk.CTkLabel(
            project_header_frame,
            text="Projects",
            font=ctk.CTkFont("DM Sans", size=14, weight="bold"),
            text_color="#505b62"
        )
        project_lbl.pack(side="left")

        # Add project button (+)
        add_project_btn = ctk.CTkButton(
            project_header_frame,
            text="+",
            width=25,  # Small width
            height=25,  # Small height
            fg_color="transparent",
            text_color="#505b62",
            hover_color="#dee4e9",
            corner_radius=6,
            font=ctk.CTkFont(size=18),
            command=self.open_create_popup
        )

        add_project_btn.pack(side="right")

        # Dynamic Project List Container
        self.project_list_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.project_list_frame.pack(fill="x")

        self.render_project_list()

    def dashboard_clicked(self):
        """Navigate to the Dashboard view."""
        self.select_button("Dashboard")
        self.parent.switch_page(DashboardPage)

    def my_tasks_clicked(self):
        """Navigate to the My Tasks view."""
        self.select_button("My tasks")
        self.parent.switch_page(MyTaskPage)

    def select_button(self, name):
        """
        Updates the visual state of buttons to highlight the active selection.

        Args:
            name (str): The name/text of the button to be highlighted.
        """

        for btn_name, btn_obj in self.menu_buttons.items():
            if btn_name == name:
                # Active Style: White background with border and bold font
                btn_obj.configure(fg_color="#ffffff", text_color="#212124",
                                  border_width = 2,  # Defines the thickness
                                  border_color = "#e7e9eb",
                                  font=ctk.CTkFont("DM Sans 14pt Semibold", size=12, weight="bold")
                                  )  # Active color

            else:
                # Normal Style: Transparent background, no border
                btn_obj.configure(fg_color="transparent", text_color="#4c515f",
                                  border_width=0,
                                  font=ctk.CTkFont("DM Sans 14pt Medium", size=12, weight="bold")
                                  )  # Normal color

    def open_create_popup(self):
        """Launches the Toplevel window to add a new project."""
        CustomProjectLevel(self, self.manager, self.refresh_callback)

    def render_project_list(self):
        """Clears and re-builds the project buttons based on the latest JSON data."""
        # Clean existing project widgets
        for widget in self.project_list_frame.winfo_children():
            widget.destroy()

        self.manager.get_data()

        # Instantiate a navigation button for every project in the database
        for project in self.manager.data:
            name = project.get_name()

            item_btn = ctk.CTkButton(
                self.project_list_frame,
                text=name,
                fg_color="transparent",
                text_color="#505b62",
                hover_color="#dee4e9",
                anchor="w",
                font=ctk.CTkFont("DM Sans 14pt", size=14),
                height=35,
                corner_radius=8,
                command=lambda n=name: self.switch_project_page(n)  # Add logic later
            )
            item_btn.pack(fill="x", padx=20, pady=2)

            # Add to tracking dict so it can be highlighted when active
            self.menu_buttons[name] = item_btn

    def switch_project_page(self, project_name):
        """
        Handles the logic for switching to a specific project's detail page.

        Args:
            project_name (str): Identifier for the project to display.
        """
        print(f"Switch Project Page in Sidebar: Switching to {project_name}")
        self.select_button(project_name)
        self.parent.switch_page(ProjectPage, project_name=project_name)