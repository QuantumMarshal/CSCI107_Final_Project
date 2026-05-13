import customtkinter as ctk

class CustomCard(ctk.CTkFrame):
    def __init__(self, parent, title, value, **kwargs):
        super().__init__(parent, **kwargs)

        self.parent = parent

        # Configure grid for the card
        self.grid_columnconfigure(0, weight=1)

        # Top Section: Title and Arrow Button
        self.title_label = ctk.CTkLabel(
            self, text=title,
            font=ctk.CTkFont("DM Sans 14pt Medium", size=14,),
        )
        self.title_label.grid(row=0, column=0, sticky="nw", padx=(20, 45), pady=(20,10))

        # Arrow Button (Circle)
        self.arrow_btn = ctk.CTkButton(
            self, text="↗", width=10, height=25,
            corner_radius=20, fg_color="white",
            text_color="black", hover_color="#e0e0e0",
            font=ctk.CTkFont(size=16)
        )
        self.arrow_btn.grid(row=0, column=1, sticky="ne", padx=20, pady=(20,10))

        self.count_projects = ctk.CTkLabel(self, text=str(value), font=ctk.CTkFont("DM Sans 14pt", size=60, weight="bold"))
        self.count_projects.grid(row=1, column=0, padx=5, pady=(0,20), columnspan=2)

    def set_value(self, value):
        self.count_projects.configure(text=str(value))