import tkinter as tk
from tkinter import PhotoImage
from ui.expense import ExpensePage
from ui.profile import ProfilePage
from ui.budget import BudgetPage
from PIL import Image, ImageTk

class HomePage:
    def __init__(self, parent, username, user_id):
        self.parent = parent
        self.username = username
        self.user_id = user_id  

        # Clear parent (main_frame)
        for widget in self.parent.winfo_children():
            widget.destroy()

        # Content Frame
        self.content_frame = tk.Frame(self.parent)
        self.content_frame.pack(fill="both", expand=True)

        self.create_navbar() # Creates navbar inside content_frame or parent?
        # Navbar should be top of content_frame? 
        # But wait, original code put navbar in self.root (parent) and content_frame below it?
        # Let's put navbar in self.parent (main_frame) for simplicity, or top of content_frame.
        
        # Top of content_frame is safer as we own it.
        
        self.show_home()

    def create_navbar(self):
        navbar = tk.Frame(self.content_frame, bg="#083013", height=70)
        navbar.pack(side="top", fill="x")

        btn_style = {"bg": "#083013", "fg": "white", "font": ("Arial", 14, "bold"), 
                     "bd": 0, "padx": 20, "pady": 15, "cursor": "hand2"}

        btn_frame = tk.Frame(navbar, bg="#083013")
        btn_frame.pack(anchor='center')

        tk.Button(btn_frame, text="Home", command=self.show_home, **btn_style).pack(side="left", padx=15)
        tk.Button(btn_frame, text="About", command=self.show_about, **btn_style).pack(side="left", padx=15)
        tk.Button(btn_frame, text="Expense", command=self.open_expense, **btn_style).pack(side="left", padx=15)
        tk.Button(btn_frame, text="Budget", command=self.open_budget, **btn_style).pack(side="left", padx=15)
        tk.Button(btn_frame, text="Reports", command=self.open_reports, **btn_style).pack(side="left", padx=15)
        tk.Button(btn_frame, text="Profile", command=self.open_profile, **btn_style).pack(side="left", padx=15)
        tk.Button(btn_frame, text="Logout", command=self.logout, **btn_style).pack(side="right", padx=15)

        # Container for pages (below navbar)
        self.page_container = tk.Frame(self.content_frame)
        self.page_container.pack(fill="both", expand=True)

    def clear_page_container(self):
        for widget in self.page_container.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_page_container()

        # Canvas for background
        self.canvas = tk.Canvas(self.page_container)
        self.canvas.pack(fill="both", expand=True)
        self.update_background_image()
        self.canvas.bind("<Configure>", self.update_background_image)

    def update_background_image(self, event=None):
        if not hasattr(self, 'canvas') or not self.canvas.winfo_exists():
            return
        
        try:
            import os
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            img_path = os.path.join(base_dir, "assets", "home_icon.png")
            original_image = Image.open(img_path)

            if event:
                width = event.width
                height = event.height
            else:
                width = self.page_container.winfo_width()
                height = self.page_container.winfo_height()
            
            if width < 10 or height < 10: # Fallback if not mapped yet
                width = self.parent.winfo_screenwidth()
                height = self.parent.winfo_screenheight()

            resized_image = original_image.resize((width, height), Image.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(resized_image)

            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")
            self.canvas.create_text(width // 2, height // 4, text=f"Welcome, {self.username}!",
                                    font=("Arial", 30, "bold"), fill="white")
        except Exception:
            pass

    def show_about(self):
        self.clear_page_container()
        tk.Label(self.page_container, text="Track your daily expenses with ease!", 
                 font=("Arial", 24, "bold"), fg="#083013").pack(pady=100)

    def open_expense(self):
        self.clear_page_container()
        from ui.expense import ExpensePage
        self.current_page = ExpensePage(self.page_container, self.username, self.user_id)

    def open_budget(self):
        self.clear_page_container()
        self.current_page = BudgetPage(self.page_container, self.user_id)

    def open_reports(self):
        self.clear_page_container()
        from ui.reports import ReportsPage
        self.current_page = ReportsPage(self.page_container, self.user_id)

    def open_profile(self):
        self.clear_page_container()
        self.current_page = ProfilePage(self.page_container, self.user_id)

    def logout(self):
        self.parent.winfo_toplevel().destroy()
        import os, sys, subprocess
        subprocess.Popen([sys.executable, "src/main.py"])
        sys.exit()
