import tkinter as tk

class AdminPage:
    def __init__(self, parent, username):
        self.parent = parent
        self.username = username
        self.theme_color = "#083013"

        # Clear parent (main_frame)
        for widget in self.parent.winfo_children():
            widget.destroy()

        # ======= Navbar =======
        navbar = tk.Frame(self.parent, bg=self.theme_color, height=90)
        navbar.pack(side="top", fill="x")

        tk.Label(navbar, text="Admin Panel", font=("Arial", 20, "bold"), fg="white", bg=self.theme_color).pack(side="left", padx=30, pady=20)

        # ======= Sidebar =======
        # We need a container for Sidebar + Content since parent is a Frame (main_frame)
        container = tk.Frame(self.parent, bg="#f4f4f4")
        container.pack(fill="both", expand=True)

        sidebar = tk.Frame(container, bg=self.theme_color, width=220)
        sidebar.pack(side="left", fill="y")

        # Button Style
        btn_style = {
            "bg": "#f1f1f1",
            "fg": "black",
            "font": ("Arial", 12, "bold"),
            "bd": 1,
            "padx": 12,
            "pady": 10,
            "width": 18
        }

        # Sidebar Buttons
        tk.Frame(sidebar, height=30, bg=self.theme_color).pack()  # Spacer

        self.home_btn = tk.Button(sidebar, text="Home", **btn_style, command=lambda: self.load_content("Home"))
        self.home_btn.pack(pady=10)

        self.users_btn = tk.Button(sidebar, text="Users", **btn_style, command=lambda: self.load_content("Users"))
        self.users_btn.pack(pady=10)

        self.logout_btn = tk.Button(sidebar, text="Logout", command=self.logout, **btn_style)
        self.logout_btn.pack(pady=10)

        # ======= Content Frame =======
        self.content_frame = tk.Frame(container, bg="white")
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.current_page = None
        self.load_content("Home")

    def load_content(self, page):
        """Update content area based on button click."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if page == "Home":
            from ui.dashboard import Dashboard
            self.current_page = Dashboard(self.content_frame)

        elif page == "Users":
            from ui.user import UserManagement
            self.current_page = UserManagement(self.content_frame)

    def logout(self):
        # To logout, we need to notify the main app.
        # Since we don't have a callback, we can restart the app or simple clear frame and rebuild main?
        # Accessing main app viawinfo_toplevel might not work if parent is frame.
        # But we are in main_frame -> root.
        # Simplest: Restart app logic
        self.parent.winfo_toplevel().destroy()
        import os, sys
        import subprocess
        subprocess.Popen([sys.executable, "src/main.py"]) # Detach and restart
        sys.exit()

# Example Usage
if __name__ == "__main__":
    root = tk.Tk()
    app = AdminPage(root, "admin")
    root.mainloop()
