
import tkinter as tk
from tkinter import ttk, messagebox
from database.db_connection import connect_to_db
from ui.styles import *

class BudgetPage:
    def __init__(self, parent, user_id):
        self.parent = parent
        self.user_id = user_id
        
        # Main Frame with Background
        main_frame = tk.Frame(self.parent, padx=20, pady=20, bg=BG_COLOR)
        main_frame.pack(fill="both", expand=True)

        # Header
        tk.Label(main_frame, text="Budget Tracking", font=FONT_HEADER, bg=BG_COLOR, fg=THEME_COLOR).pack(pady=(0, 20), anchor="w")

        # Content Container
        content_container = tk.Frame(main_frame, bg=BG_COLOR)
        content_container.pack(fill="both", expand=True)

        # ---------------- LEFT FRAME (Set Budget) ----------------
        self.form_frame = tk.Frame(content_container, bd=0, bg="white", padx=20, pady=20)
        self.form_frame.pack(side="left", fill="y", padx=(0, 20))

        tk.Label(self.form_frame, text="Set Monthly Budget", font=FONT_SUBHEADER, bg="white").pack(pady=(0, 20), anchor="w")

        # Table Frame
        self.table_frame = tk.Frame(content_container, bg="white")
        self.table_frame.pack(side="right", fill="both", expand=True, padx=20)

        self.create_form()
        # self.create_table() # Table is created in __init__, no separate method
        self.load_budgets()

    def create_form(self):
        # Category
        tk.Label(self.form_frame, text="Category:", bg="white", font=FONT_BOLD).pack(anchor="w")
        self.category_combobox = ttk.Combobox(self.form_frame, state="readonly", width=28, font=FONT_BODY)
        self.category_combobox.pack(pady=5)
        self.load_categories()

        # Month
        tk.Label(self.form_frame, text="Month:", bg="white", font=FONT_BOLD).pack(anchor="w")
        self.month_combobox = ttk.Combobox(self.form_frame, values=[str(i) for i in range(1, 13)], state="readonly", width=28, font=FONT_BODY)
        self.month_combobox.current(0)
        self.month_combobox.pack(pady=5)

        # Year
        tk.Label(self.form_frame, text="Year:", bg="white", font=FONT_BOLD).pack(anchor="w")
        self.year_combobox = ttk.Combobox(self.form_frame, values=[str(i) for i in range(2023, 2030)], state="readonly", width=28, font=FONT_BODY)
        self.year_combobox.current(0)
        self.year_combobox.pack(pady=5)

        # Amount
        tk.Label(self.form_frame, text="Budget Amount:", bg="white", font=FONT_BOLD).pack(anchor="w")
        self.amount_entry = tk.Entry(self.form_frame, width=30, font=FONT_BODY, bd=2, relief="groove")
        self.amount_entry.pack(pady=5)

        tk.Button(self.form_frame, text="Set Budget", command=self.save_budget, **BTN_STYLE).pack(pady=20, fill="x")

        # ---------------- RIGHT FRAME (Table) ----------------
        right_frame = tk.Frame(self.parent.nametowidget(self.form_frame.winfo_parent()), bd=0, bg=BG_COLOR)
        right_frame.pack(side="right", fill="both", expand=True)

        table_frame = tk.Frame(right_frame, bg="white", padx=10, pady=10)
        table_frame.pack(fill="both", expand=True)

        tk.Label(table_frame, text="Budget Overview", font=FONT_SUBHEADER, bg="white").pack(pady=(0, 10), anchor="w")

        apply_tree_style()
        columns = ("Category", "Month", "Budget", "Actual", "Status")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Treeview", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def load_categories(self):
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT category_id, category_name FROM tbl_categories WHERE user_id = %s", (self.user_id,))
            cats = cursor.fetchall()
            conn.close()
            
            self.categories = {name: cid for cid, name in cats}
            # Use 'category_combobox' as per create_form
            self.category_combobox['values'] = list(self.categories.keys())

    def save_budget(self):
        cat_name = self.category_combobox.get()
        month = self.month_combobox.get()
        year = self.year_combobox.get()
        amount = self.amount_entry.get()

        if not cat_name or not amount:
            messagebox.showerror("Error", "All fields are required!")
            return

        cat_id = self.categories.get(cat_name)

        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            try:
                query = """
                    INSERT INTO tbl_budget (user_id, category_id, monthly_budget, month, year)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE monthly_budget = VALUES(monthly_budget)
                """
                # Note: Schema had 'amount', assuming 'monthly_budget' or updating schema to match.
                # In Step 67 I named it 'amount'. Let me check.
                # Yes, Step 67: `amount DECIMAL(10, 2) NOT NULL`.
                # So I should use `amount` here.
                
                query = """
                    INSERT INTO tbl_budget (user_id, category_id, amount, month, year)
                    VALUES (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE amount = VALUES(amount)
                """
                cursor.execute(query, (self.user_id, cat_id, amount, month, year))
                conn.commit()
                messagebox.showinfo("Success", "Budget set successfully!")
                self.load_budgets()
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

    def load_budgets(self):
        self.tree.delete(*self.tree.get_children())
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            # Fetch Budget vs Actual
            query = """
                SELECT c.category_name, b.month, b.year, b.amount, 
                       COALESCE(SUM(e.amount), 0) as actual
                FROM tbl_budget b
                JOIN tbl_categories c ON b.category_id = c.category_id
                LEFT JOIN tbl_expenses e ON b.category_id = e.category_id 
                                         AND MONTH(e.expense_date) = b.month 
                                         AND YEAR(e.expense_date) = b.year
                WHERE b.user_id = %s
                GROUP BY b.budget_id
                ORDER BY b.year DESC, b.month DESC
            """
            cursor.execute(query, (self.user_id,))
            rows = cursor.fetchall()
            
            for row in rows:
                cat, month, year, budget, actual = row
                status = "Over Budget" if actual > budget else "On Track"
                color = "red" if actual > budget else "green"
                
                item_id = self.tree.insert("", "end", values=(cat, f"{month}/{year}", f"₹{budget}", f"₹{actual}", status))
                # Note: formatting row color requires tags, simplified here.
            
            conn.close()
