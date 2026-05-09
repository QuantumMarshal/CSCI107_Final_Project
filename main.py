"""
Project Management System - Main Window - MainApplication

A comprehensive project management solution designed to facilitate task
orchestration, resource allocation, and real-time collaboration. This
application serves as the central hub for managing the full lifecycle
of a project from initiation to delivery.

Author: Nguyen Quang Nhan Pham
Date: 05/13/2026
"""

# Import the library use in the project
import customtkinter as ctk     # GUI library

# Import all widget and page used in the App
from widgets.dashboard_page import DashboardPage
from widgets.sidebar import Sidebar

# Import the data manager
from manager import Manager

# Universal background color
bg_color = "#f8fafb"

"""
Main window --> Root that inherit from the customtkinter window

MainApplication attr:
*   Manager:                Data Manager
*   Sidebar:                Sidebar of the app
*   Main_Container:         Main Frame of the app

MainApplication methods:
*   init_configure:         config the window at the beginning of the application
*   create_widgets:         create the frame and widget
*   switch_page:            change the current page
*   reload_current_page:    reload the current page
"""
class MainApplication(ctk.CTk):
    # Constructor
    def __init__(self) -> None:
        super().__init__()
        self.manager = Manager()

        self.init_configure()

        self.create_widgets()

        self.sidebar.select_button("Dashboard")
        self.current_page = None
        self.switch_page(DashboardPage)

    def init_configure(self):
        self.title("Dashboard")
        self.geometry("1280x720")
        ctk.set_appearance_mode("light")
        self.resizable(False, False)

        self.grid_rowconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=1, weight=1)

        self.configure(fg_color=bg_color)

    def create_widgets(self):
        self.sidebar = Sidebar(self, self.manager, self.reload_current_page, width=400, corner_radius=0, fg_color=bg_color)
        self.sidebar.grid(column=0, row=0, sticky="nsew")

        # 2. Create the 'Main Frame' container
        # This remains static, but we change what is INSIDE it
        self.main_container = ctk.CTkFrame(self, fg_color=bg_color)
        self.main_container.grid(row=0, column=1, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

    def switch_page(self, page_class, project_name = None):
        print(f"Switch Page Function in MainApplication: Switch to {page_class.__name__}")

        if project_name is None:
            if self.current_page is not None:
                self.current_page.destroy()  # Remove the old page from memory

            # Create the new frame inside the main_container
            self.current_page = page_class(self.main_container, manager=self.manager,refresh_callback=self.reload_current_page,
                                           fg_color="#ffffff", corner_radius=20, border_color="#e7e9eb", border_width=2)
            self.current_page.grid(row=0, column=0, sticky="nsew", padx=(0,10), pady=(5, 10))
        elif project_name is not None:
            print(f"Switch Page Function in MainApplication: Switch to {project_name}")
            if self.current_page is not None:
                self.current_page.destroy()

            self.current_page = page_class(self.main_container, manager=self.manager, refresh_callback=self.reload_project_page, project_name=project_name,
                                           fg_color="#ffffff", corner_radius=20, border_color="#e7e9eb", border_width=2)
            self.current_page.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=(5, 10))

    def reload_current_page(self):
        self.sidebar.render_project_list()
        if self.current_page is not None and hasattr(self.current_page, "reload_dashboard"):
            self.current_page.reload_dashboard()

    def reload_project_page(self):
        pass

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()