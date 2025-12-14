import tkinter as tk
from tkinter import messagebox, Toplevel
from PIL import Image, ImageTk  # For background image support
import re  # For validation
import os
from database.db_connection import connect_to_db
from ui.home import HomePage
from ui.admin import AdminPage
from ui.styles import *

# --- Main Application Class ---
class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Expense Tracker")
        try:
            self.root.state("zoomed")
        except tk.TclError:
            self.root.attributes("-zoomed", True)
        
        self.bg_photo = None
        self.user_id = None
        self.username = None

        self.create_navbar()
        
        # Main Content Container
        self.main_frame = tk.Frame(self.root, bg="#f4f4f4")
        self.main_frame.pack(fill="both", expand=True)

        self.current_page = None 
        self.show_home_initial()
        self.show_login_popup()

    # --- Navigation Bar ---
    def create_navbar(self):
        self.navbar = tk.Frame(self.root, bg="#083013", height=70)
        self.navbar.pack(side="top", fill="x")

        btn_style = {"bg": "#083013", "fg": "white", "font": ("Arial", 14, "bold"), "bd": 0, "padx": 20, "pady": 15, "cursor": "hand2"}

        btn_frame = tk.Frame(self.navbar, bg="#083013")
        btn_frame.pack(anchor='center')

        tk.Button(btn_frame, text="Home", command=self.show_home, **btn_style).pack(side="left", padx=15)
        tk.Button(btn_frame, text="About", command=self.show_about, **btn_style).pack(side="left", padx=15)
        tk.Button(btn_frame, text="Signup", command=self.show_signup_popup, **btn_style).pack(side="right", padx=15)
        tk.Button(btn_frame, text="Login", command=self.show_login_popup, **btn_style).pack(side="right", padx=15)

    # --- Landing Page Content ---
    def show_home_initial(self):
        self.clear_frame()

        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            img_path = os.path.join(base_dir, "assets", "home.jpg")
            bg_image = Image.open(img_path) 
            bg_image = bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)

            canvas = tk.Canvas(self.main_frame, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
            canvas.pack(fill="both", expand=True)
            canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")

            # Welcome Text
            canvas.create_text(self.root.winfo_screenwidth() // 2, 100, text="Welcome to Personal Expense Tracker", 
                               font=("Arial", 30, "bold"), fill="white")
        except Exception as e:
            print(f"Error loading image: {e}")
            tk.Label(self.main_frame, text="Welcome to Personal Expense Tracker", 
                     font=("Arial", 30, "bold"), fg="#083013").pack(pady=50)

    def show_home(self):
        self.clear_frame()
        if self.user_id:
            self.navbar.pack_forget() # Hide main navbar
            from ui.home import HomePage
            self.current_page = HomePage(self.main_frame, self.username, self.user_id)
        else:
            self.show_home_initial()

    def show_admin(self):
        self.clear_frame()
        if self.username:
            self.navbar.pack_forget() # Hide main navbar
            from ui.admin import AdminPage
            self.current_page = AdminPage(self.main_frame, self.username)
        else:
            self.show_home_initial()

    def show_about(self):
        self.clear_frame()
        frame = tk.Frame(self.main_frame, bg="white", padx=50, pady=50)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text="About the Expense Tracker", font=("Arial", 28, "bold"), fg="#083013", bg="white").pack(pady=20)
        
        desc = ("Welcome to your personal financial companion.\n\n"
                "This application allows you to:\n"
                "- Track Income & Expenses with ease.\n"
                "- Set Monthly Budgets to stay on track.\n"
                "- Visualize your spending with interactive charts.\n"
                "- Export your financial reports for external analysis.\n\n"
                "Developed with precision to help you manage your wealth.")
        
        tk.Label(frame, text=desc, font=("Arial", 14), fg="#333", bg="white", justify="left").pack(pady=20)
        
        tk.Label(frame, text="Version 2.0 | Premium Edition", font=("Arial", 10, "italic"), fg="gray", bg="white").pack(side="bottom", pady=20)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # --- Login Form Popup ---
    def show_login_popup(self):
        if self.user_id: # Already logged in
            return
            
        login_win = Toplevel(self.root)
        login_win.title("Login")
        login_win.geometry("400x350")
        login_win.configure(bg="white")
        
        tk.Label(login_win, text="Welcome Back", font=("Arial", 20, "bold"), bg="white", fg="#083013").pack(pady=20)

        tk.Label(login_win, text="Username", bg="white", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        login_username = tk.Entry(login_win, font=("Arial", 12), bd=2, relief="groove")
        login_username.pack(pady=5, ipadx=5, ipady=3)

        tk.Label(login_win, text="Password", bg="white", font=("Arial", 10, "bold")).pack(pady=(10, 5))
        login_password = tk.Entry(login_win, show="*", font=("Arial", 12), bd=2, relief="groove")
        login_password.pack(pady=5, ipadx=5, ipady=3)

        tk.Button(login_win, text="Login", command=lambda: self.login_user(login_username.get(), login_password.get(), login_win),
                  bg="#083013", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10, cursor="hand2", bd=0).pack(pady=30)

    # --- Signup Form Popup ---
    def show_signup_popup(self):
        signup_win = Toplevel(self.root)
        signup_win.title("Create Account")
        signup_win.geometry("450x550")
        signup_win.configure(bg="white")

        tk.Label(signup_win, text="Join Us", font=("Arial", 20, "bold"), bg="white", fg="#083013").pack(pady=20)

        fields = ["Username", "Password", "Phone", "Address"]
        entries = {}

        for field in fields:
            tk.Label(signup_win, text=field, bg="white", font=("Arial", 10, "bold")).pack(pady=(10, 2))
            entry = tk.Entry(signup_win, font=("Arial", 12), bd=2, relief="groove")
            if field == "Password":
                entry.config(show="*")
            entry.pack(pady=2, ipadx=5, ipady=3)
            entries[field] = entry

        tk.Button(signup_win, text="CREATE ACCOUNT", command=lambda: self.validate_and_register(entries["Username"].get(), entries["Password"].get(),
                                                                                         entries["Phone"].get(), entries["Address"].get(), signup_win),
                  bg="#083013", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10, cursor="hand2", bd=0).pack(pady=30)

    # --- Signup Validation ---
    def validate_and_register(self, username, password, phone, address, signup_win):
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            messagebox.showerror("Error", "Password must contain at least one special character!")
            return

        if not re.fullmatch(r'\d{10}', phone):
            messagebox.showerror("Error", "Phone number must be exactly 10 digits!")
            return

        self.register_user(username, password, phone, address, signup_win)

    # --- Register User ---
    def register_user(self, username, password, phone, address, signup_win):
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO tbl_login (username, password, login_type) VALUES (%s, %s, %s)", (username, password, "User"))
                cursor.execute("INSERT INTO tbl_users (username, phone, address) VALUES (%s, %s, %s)", (username, phone, address))
                conn.commit()
                messagebox.showinfo("Success", "Signup Successful!")
                signup_win.destroy()
            except Exception as e:
                conn.rollback()
                messagebox.showerror("Error", f"Signup Failed: {e}")
            finally:
                conn.close()
        else:
            messagebox.showerror("Error", "Database Connection Failed!")

    # --- User Login ---
    def login_user(self, username, password, login_win):
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()

            cursor.execute("SELECT username, login_type FROM tbl_login WHERE username = %s AND password = %s AND login_type = 'Admin'", (username, password))
            admin = cursor.fetchone()

            if admin:
                login_win.destroy()
                self.username = username # Set session
                self.open_admin_dashboard(username)
            else:
                cursor.execute("""
                    SELECT tbl_users.user_id, tbl_login.username, tbl_login.login_type 
                    FROM tbl_login 
                    INNER JOIN tbl_users ON tbl_login.username = tbl_users.username 
                    WHERE tbl_login.username = %s AND tbl_login.password = %s
                """, (username, password))
                user = cursor.fetchone()

                if user:
                    login_win.destroy()
                    self.username = username # Set session
                    self.user_id = user[0]   # Set session
                    self.open_user_dashboard(username, user[0])
                else:
                    messagebox.showerror("Error", "Invalid Credentials!")

            conn.close()
        else:
            messagebox.showerror("Error", "Database Connection Failed!")

    def open_user_dashboard(self, username, user_id):
        self.show_home() # This will use self.user_id to load the HomePage

    def open_admin_dashboard(self, username):
        self.show_admin() # This will load AdminPage

# --- Main Application Execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
