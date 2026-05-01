import customtkinter as ctk
from PIL import Image, ImageTk
import os

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent

        self.create_widgets()

    def create_widgets(self):
        self.logo_label = ctk.CTkLabel(self, text="Project.",
                                       font=ctk.CTkFont("DM Sans 14pt", size=20, weight="bold"))
        self.logo_label.pack(pady=(20, 20), padx=(35, 35), anchor="w")

        self.menu_buttons = {}

        menu_items = [("Dashboard", self.dashboard_clicked),
                      ("My tasks", self.my_tasks_clicked),
                      ("Documents", self.documents_clicked)]

        try:
            # 1. Get the directory of the current file (widgets folder)
            current_dir = os.path.dirname(os.path.realpath(__file__))

            # 2. Go up one level to the Project Root
            project_root = os.path.dirname(current_dir)

            # 3. Join with the icons folder
            image_path = os.path.join(project_root, "icons")

            for item in menu_items:
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

                self.menu_buttons[item[0]] = btn

        except Exception as e:
            print(e)

    def dashboard_clicked(self):
        print("Dashboard clicked")

    def my_tasks_clicked(self):
        print("My tasks clicked")

    def documents_clicked(self):
        print("Documents clicked")

    def handle_click(self, button_name, command_func):
        """Update visuals and then run the original command."""
        self.select_button(button_name)
        command_func()

    def select_button(self, name):
        """Highlights the chosen button and resets others."""
        for btn_name, btn_obj in self.menu_buttons.items():
            if btn_name == name:
                btn_obj.configure(fg_color="#ffffff", text_color="#212124",
                                  border_width = 2,  # Defines the thickness
                                  border_color = "#e7e9eb",
                                  font=ctk.CTkFont("DM Sans 14pt Semibold", size=12, weight="bold")
                                  )  # Active color

            else:
                btn_obj.configure(fg_color="transparent", text_color="#4c515f",
                                  border_width=0,
                                  font=ctk.CTkFont("DM Sans 14pt Medium", size=12, weight="bold")
                                  )  # Normal color