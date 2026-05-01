import customtkinter as ctk
from PIL import Image, ImageTk
import os

class MainApplication(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        # self.sidebar = CustomSidebar(self)

        self.title("Dashboard")
        self.geometry("1280x720")
        ctk.set_appearance_mode("light")
        self.resizable(False, False)

        self.init_configure()

    def init_configure(self):
        self.grid_rowconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=1, weight=1)

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()