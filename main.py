"""
Project Management System - Main Window - MainApplication

A comprehensive project management solution designed to facilitate task
orchestration, resource allocation, and real-time collaboration. This
application serves as the central hub for managing the full lifecycle
of a project from initiation to delivery.

Author: Nguyen Quang Nhan Pham
Date: 05/13/2026
"""

import customtkinter as ctk     # GUI framework for modern Python interfaces

# Internal widget and page imports
from widgets.dashboard_page import DashboardPage
from widgets.sidebar import Sidebar
from manager import Manager     # Handles JSON data persistence

# Global styling configuration
bg_color = "#f8fafb"

class MainApplication(ctk.CTk):
    """
    The root window class for the Project Management System.

    Inherits from ctk.CTk and manages the top-level orchestration of
    data and UI state.
    """

    def __init__(self) -> None:
        """Initialize data manager, window configuration, and default view."""
        super().__init__()

        # Initialize the core data engine
        self.manager = Manager()

        # Set up window properties (title, size, grid)
        self.init_configure()

        # Build the permanent UI structure (Sidebar and Main Container)
        self.create_widgets()

        # App state management
        self.current_page = None
        self.sidebar.select_button("Dashboard") # Default selection visual
        self.switch_page(DashboardPage)         # Initial page load

    def init_configure(self):
        """Standardizes the application window settings."""
        self.title("Project Management System") # Updated for professional branding
        self.geometry("1280x720")
        ctk.set_appearance_mode("light")
        self.resizable(False, False)

        # 0: Sidebar (fixed), 1: Content (expanding)
        self.grid_rowconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=1, weight=1)

        self.configure(fg_color=bg_color)

    def create_widgets(self):
        """Instantiates the primary layout components."""
        # Sidebar manages navigation and project lists
        self.sidebar = Sidebar(self,
                               self.manager,
                               self.reload_current_page,
                               width=400,
                               corner_radius=0,
                               fg_color=bg_color
                              )
        self.sidebar.grid(column=0, row=0, sticky="nsew")

        # Main Frame acts as a dynamic viewport for different pages
        self.main_container = ctk.CTkFrame(self, fg_color=bg_color)
        self.main_container.grid(row=0, column=1, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

    def switch_page(self, page_class, project_name=None):
        """
        Swaps the content of the main container with a new page.

        Args:
            page_class: The class of the frame to instantiate.
            project_name (str, optional): The name of the project if loading a ProjectPage.
        """
        print(f"Navigation: Switching to {page_class.__name__}")

        # Clean up existing page to prevent memory leaks
        if self.current_page is not None:
            self.current_page.destroy()

        # Define common layout parameters for pages
        page_params = {
            "manager": self.manager,
            "fg_color": "#ffffff",
            "corner_radius": 20,
            "border_color": "#e7e9eb",
            "border_width": 2
        }

        # Logic for project-specific pages vs general pages
        if project_name:
            self.current_page = page_class(
                self.main_container,
                refresh_callback=self.reload_project_page,
                project_name=project_name,
                **page_params
            )
        else:
            self.current_page = page_class(
                self.main_container,
                refresh_callback=self.reload_current_page,
                **page_params
            )

        self.current_page.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(5, 10))

    def reload_current_page(self):
        """Refreshes the sidebar and triggers a data reload on the current dashboard."""
        self.sidebar.render_project_list()
        if self.current_page and hasattr(self.current_page, "reload_dashboard"):
            self.current_page.reload_dashboard()

    def reload_project_page(self):
        """Placeholder for specific project page refresh logic."""
        # Since you are an ENTJ who values efficiency, we'll keep this ready
        # for when you need to trigger specific project view refreshes.
        pass

if __name__ == "__main__":
    # Launch the application
    app = MainApplication()
    app.mainloop()