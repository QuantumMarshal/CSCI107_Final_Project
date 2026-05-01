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
                    size=(24, 24)  # Adjust size to match your font
                )

                btn = ctk.CTkButton(self, text=item[0], fg_color="transparent",
                                    text_color="#505b62", hover_color="#dee4e9", anchor="w",
                                    font=ctk.CTkFont("DM Sans 14pt Medium", size=14),
                                    corner_radius=10, height=40,
                                    image=icon_image, compound="left",  # Icon next to text
                                    command=item[1],
                                    )
                btn.pack(fill="x", padx=20, pady=5)
        except Exception as e:
            print(e)

    def dashboard_clicked(self):
        print("Dashboard clicked")

    def my_tasks_clicked(self):
        print("My tasks clicked")

    def documents_clicked(self):
        print("Documents clicked")