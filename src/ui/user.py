
import tkinter as tk
from tkinter import ttk, messagebox
from database.db_connection import connect_to_db
from ui.styles import *

class UserManagement:
    def __init__(self, parent):
        self.parent = parent
        
        # Main Frame with Background
        main_frame = tk.Frame(self.parent, padx=20, pady=20, bg=BG_COLOR)
        main_frame.pack(fill="both", expand=True)

        # Header
        tk.Label(main_frame, text="User Management", font=FONT_HEADER, bg=BG_COLOR, fg=THEME_COLOR).pack(pady=(0, 20), anchor="w")

        # Delete Button (Centered and Red)
        tk.Button(main_frame, text="DELETE SELECTED USER", command=self.delete_user, bg="#d9534f", fg="white", font=FONT_BOLD, bd=0, padx=20, pady=12, cursor="hand2").pack(side="bottom", fill="x", pady=20)

        # Table Frame
        table_frame = tk.Frame(main_frame, bg="white", padx=10, pady=10)
        table_frame.pack(fill="both", expand=True)

        columns = ("ID", "Username", "Phone", "Address")
        apply_tree_style()
        self.user_table = ttk.Treeview(table_frame, columns=columns, show="headings", style="Treeview", height=20)

        for col in columns:
            self.user_table.heading(col, text=col)
            self.user_table.column(col, anchor="center")
            
        scrollbar_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.user_table.yview)
        scrollbar_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.user_table.xview)
        self.user_table.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # Pack Scrollbars
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.user_table.pack(side="left", fill="both", expand=True)

        # Load Users
        self.load_users()

    def load_users(self):
        """Fetch and display users from the database."""
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, username, phone, address FROM tbl_users")
            rows = cursor.fetchall()
            conn.close()

            self.user_table.delete(*self.user_table.get_children())  # Clear existing data

            for row in rows:
                self.user_table.insert("", "end", values=row)

    def delete_user(self):
        """Delete selected user from the database and login table."""
        selected_item = self.user_table.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a user to delete.")
            return

        # Get User ID and Username from the selected row
        values = self.user_table.item(selected_item, "values")
        user_id = values[0]
        username = values[1]

        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to permanently delete user '{username}'?\n\nThis will delete ALL their data (expenses, income, budget).")
        if confirm:
            conn = connect_to_db()
            if conn:
                try:
                    cursor = conn.cursor()
                    
                    # Delete from tbl_login (Removes access)
                    cursor.execute("DELETE FROM tbl_login WHERE username = %s", (username,))
                    
                    # Delete from tbl_users (Cascades to other tables)
                    cursor.execute("DELETE FROM tbl_users WHERE user_id = %s", (user_id,))
                    
                    conn.commit()
                    messagebox.showinfo("Success", f"User '{username}' deleted successfully.")
                    self.load_users()  # Refresh table
                except Exception as e:
                    conn.rollback()
                    messagebox.showerror("Error", f"Failed to delete user: {e}")
                finally:
                    conn.close()

