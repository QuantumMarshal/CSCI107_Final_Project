import customtkinter as ctk
from PIL import Image, ImageTk
import os

from widgets.sidebar import Sidebar


class MainApplication(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        # self.sidebar = CustomSidebar(self)

        self.title("Dashboard")
        self.geometry("1280x720")
        ctk.set_appearance_mode("light")
        self.resizable(False, False)

        self.init_configure()

        self.create_widgets()

    def init_configure(self):
        self.grid_rowconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=1, weight=1)

    def create_widgets(self):
        self.sidebar = Sidebar(self, width=400, corner_radius=0)
        self.sidebar.grid(column=0, row=0, sticky="nsew")

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()