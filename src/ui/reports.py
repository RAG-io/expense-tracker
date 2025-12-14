import tkinter as tk
import csv
from datetime import datetime
from tkinter import ttk, filedialog, messagebox
from database.db_connection import connect_to_db
from ui.styles import *

class ReportsPage:
    def __init__(self, parent, user_id):
        self.parent = parent
        self.user_id = user_id
        
        # Main Frame with Background
        main_frame = tk.Frame(self.parent, padx=20, pady=20, bg=BG_COLOR)
        main_frame.pack(fill="both", expand=True)

        # Header
        tk.Label(main_frame, text="Financial Reports", font=FONT_HEADER, bg=BG_COLOR, fg=THEME_COLOR).pack(pady=(0, 20), anchor="w")

        # Filter Container
        filter_container = tk.Frame(main_frame, bg=BG_COLOR)
        filter_container.pack(fill="x", pady=(10, 20))

        # Month
        tk.Label(filter_container, text="Month:", bg=BG_COLOR, font=FONT_BOLD).pack(side="left", padx=(0, 10))
        self.month_combobox = ttk.Combobox(filter_container, values=[str(i) for i in range(1, 13)], state="readonly", width=10, font=FONT_BODY)
        self.month_combobox.set(str(datetime.now().month))
        self.month_combobox.pack(side="left", padx=(0, 20))

        # Year
        tk.Label(filter_container, text="Year:", bg=BG_COLOR, font=FONT_BOLD).pack(side="left", padx=(0, 10))
        self.year_combobox = ttk.Combobox(filter_container, values=[str(i) for i in range(datetime.now().year - 5, datetime.now().year + 5)], state="readonly", width=10, font=FONT_BODY)
        self.year_combobox.set(str(datetime.now().year))
        self.year_combobox.pack(side="left", padx=(0, 20))

        tk.Button(filter_container, text="View Report", command=self.load_report, **BTN_STYLE).pack(side="left", padx=10)
        
        # Export Button (Right Aligned)
        tk.Button(filter_container, text="Export CSV", command=self.export_csv, bg="#2196F3", fg="white", font=FONT_BOLD, bd=0, padx=20, pady=12, cursor="hand2").pack(side="right")

        # Table Frame
        table_frame = tk.Frame(main_frame, bg="white", padx=10, pady=10)
        table_frame.pack(fill="both", expand=True)
        
        # Treeview
        columns = ("Category", "Amount")
        apply_tree_style()
        self.report_tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Treeview", height=15)
        
        for col in columns:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, anchor="center")
            
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.report_tree.yview)
        self.report_tree.configure(yscrollcommand=scrollbar.set)
        
        self.report_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Summary Label (Footer)
        self.total_label = tk.Label(main_frame, text="", font=FONT_SUBHEADER, bg=BG_COLOR, fg=THEME_COLOR)
        self.total_label.pack(pady=20, anchor="e")

        self.current_month_data = []
        self.load_report()

    def load_report(self):
        # Clear existing Treeview items
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)

        month = int(self.month_combobox.get())
        year = int(self.year_combobox.get())

        conn = connect_to_db()
        cursor = conn.cursor()

        # Get income
        cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM tbl_income WHERE user_id = %s AND YEAR(income_date) = %s AND MONTH(income_date) = %s", (self.user_id, year, month))
        income = cursor.fetchone()[0]

        # Get expenses
        cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM tbl_expenses WHERE user_id = %s AND YEAR(expense_date) = %s AND MONTH(expense_date) = %s", (self.user_id, year, month))
        expense = cursor.fetchone()[0]

        # Update Summary Label
        self.total_label.config(text=f"Income: ₹{income:.2f}   |   Expenses: ₹{expense:.2f}   |   Balance: ₹{income - expense:.2f}")

        # Get Category-wise breakdown
        cursor.execute("""
            SELECT c.category_name, SUM(e.amount)
            FROM tbl_expenses e
            JOIN tbl_categories c ON e.category_id = c.category_id
            WHERE e.user_id = %s AND YEAR(e.expense_date) = %s AND MONTH(e.expense_date) = %s
            GROUP BY c.category_name
        """, (self.user_id, year, month))
        
        cat_expenses = cursor.fetchall()
        self.current_month_data = cat_expenses 
        
        for cat, amt in cat_expenses:
            self.report_tree.insert("", "end", values=(cat, f"₹{amt:.2f}"))

        conn.close()

    def export_csv(self):
        if not hasattr(self, 'current_month_data') or not self.current_month_data:
            messagebox.showwarning("Warning", "No data to export!")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return

        try:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Category", "Amount"])
                writer.writerows(self.current_month_data)
            messagebox.showinfo("Success", "Data exported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export: {e}")
