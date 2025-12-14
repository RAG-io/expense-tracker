import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database.db_connection import connect_to_db
from ui.styles import *


from ui.styles import *

class ExpensePage:
    def __init__(self, parent, username, user_id):
        self.parent = parent  # Use parent frame instead of root
        # self.parent.winfo_toplevel().title("Expense & Income Manager") # Don't reset title, might flicker
        self.username = username
        self.user_id = user_id

        # Outer Frame (Main Container)
        outer_frame = tk.Frame(self.parent, bg=BG_COLOR)
        outer_frame.pack(fill="both", expand=True)

        # Scrollable Canvas
        canvas = tk.Canvas(outer_frame, bg=BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer_frame, orient="vertical", command=canvas.yview)
        
        # This frame sits inside the canvas
        main_frame = tk.Frame(canvas, bg=BG_COLOR)

        main_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=main_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Main Frame with Background (now scrollable)
        main_frame.config(padx=20, pady=20) # Apply padding to inner frame
        
        # Header
        tk.Label(main_frame, text="Expense & Income Manager", font=FONT_HEADER, bg=BG_COLOR, fg=THEME_COLOR).pack(pady=(0, 20), anchor="w")

        # Content Container (Grid Layout)
        content_container = tk.Frame(main_frame, bg=BG_COLOR)
        content_container.pack(fill="both", expand=True)

        # ---------------- LEFT FRAME (Forms) ----------------
        left_frame = tk.Frame(content_container, bd=0, bg="white", padx=20, pady=20)
        left_frame.pack(side="left", fill="y", padx=(0, 20))

        # Category Form
        tk.Label(left_frame, text="Add Category", font=FONT_SUBHEADER, bg="white").pack(pady=(0, 10), anchor="w")
        self.category_entry = tk.Entry(left_frame, width=30, font=FONT_BODY, bd=2, relief="groove")
        self.category_entry.pack(pady=5)
        tk.Button(left_frame, text="Add Category", command=self.add_category, **BTN_STYLE).pack(pady=10, fill="x")

        # Divider
        tk.Frame(left_frame, height=1, bg="#e0e0e0").pack(fill="x", pady=20)

        # Expense Form
        tk.Label(left_frame, text="Add Expense", font=FONT_SUBHEADER, bg="white").pack(pady=(0, 10), anchor="w")
        
        tk.Label(left_frame, text="Amount:", bg="white", font=FONT_BOLD).pack(anchor="w")
        self.expense_amount_entry = tk.Entry(left_frame, width=35, font=FONT_BODY, bd=2, relief="groove")
        self.expense_amount_entry.pack(pady=5)

        tk.Label(left_frame, text="Category:", bg="white", font=FONT_BOLD).pack(anchor="w")
        self.category_combobox = ttk.Combobox(left_frame, state="readonly", width=33, font=FONT_BODY)
        self.category_combobox.pack(pady=5)

        tk.Label(left_frame, text="Description:", bg="white", font=FONT_BOLD).pack(anchor="w")
        self.expense_description_entry = tk.Entry(left_frame, width=35, font=FONT_BODY, bd=2, relief="groove")
        self.expense_description_entry.pack(pady=5)

        tk.Label(left_frame, text="Date:", bg="white", font=FONT_BOLD).pack(anchor="w")
        self.expense_date_entry = DateEntry(left_frame, date_pattern='yyyy-mm-dd', width=33, font=FONT_BODY)
        self.expense_date_entry.pack(pady=5)

        tk.Button(left_frame, text="Save Expense", command=self.save_expense, **BTN_STYLE).pack(pady=10, fill="x")

        # Divider
        tk.Frame(left_frame, height=1, bg="#e0e0e0").pack(fill="x", pady=20)

        # Income Form
        tk.Label(left_frame, text="Add Income", font=FONT_SUBHEADER, bg="white").pack(pady=(0, 10), anchor="w")

        tk.Label(left_frame, text="Amount:", bg="white", font=FONT_BOLD).pack(anchor="w")
        self.income_amount_entry = tk.Entry(left_frame, width=35, font=FONT_BODY, bd=2, relief="groove")
        self.income_amount_entry.pack(pady=5)

        tk.Label(left_frame, text="Source:", bg="white", font=FONT_BOLD).pack(anchor="w")
        self.income_source_entry = tk.Entry(left_frame, width=35, font=FONT_BODY, bd=2, relief="groove")
        self.income_source_entry.pack(pady=5)

        tk.Label(left_frame, text="Date:", bg="white", font=FONT_BOLD).pack(anchor="w")
        self.income_date_entry = DateEntry(left_frame, date_pattern='yyyy-mm-dd', width=33, font=FONT_BODY)
        self.income_date_entry.pack(pady=5)
        self.income_date_entry.pack(pady=5)

        tk.Button(left_frame, text="Save Income", command=self.save_income, **BTN_STYLE).pack(pady=10, fill="x")

        # ---------------- RIGHT FRAME (Table + Pie Chart) ----------------
        right_frame = tk.Frame(content_container, bd=0, bg=BG_COLOR)
        right_frame.pack(side="right", fill="both", expand=True)

        # Table Frame
        table_frame = tk.Frame(right_frame, bg="white", padx=10, pady=10)
        table_frame.pack(fill="both", expand=True)

        tk.Label(table_frame, text="Transaction History", font=FONT_SUBHEADER, bg="white").pack(pady=(0, 10), anchor="w")

        # Unified Table with Type Column
        columns = ("Type", "Amount", "Category/Source", "Description", "Date")
        
        # Apply Tree Style
        apply_tree_style()
        
        self.summary_tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Treeview", height=12)

        for col in columns:
            self.summary_tree.heading(col, text=col)
            self.summary_tree.column(col, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.summary_tree.yview)
        self.summary_tree.configure(yscrollcommand=scrollbar.set)
        
        self.summary_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Pie Chart Frame (Below the Table)
        self.chart_frame = tk.Frame(right_frame, bg="white", padx=10, pady=10)
        self.chart_frame.pack(fill="both", expand=True, pady=(20, 0))

        # Load Data
        self.load_categories()
        self.load_data()

    def load_categories(self):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT category_id, category_name FROM tbl_categories WHERE user_id = %s", (self.user_id,))
        categories = cursor.fetchall()
        conn.close()
        self.category_combobox["values"] = [cat[1] for cat in categories]
        self.category_map = {str(cat[0]): cat[1] for cat in categories}

    def add_category(self):
        category_name = self.category_entry.get()
        if not category_name:
            messagebox.showerror("Error", "Category name cannot be empty!")
            return

        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tbl_categories (user_id, category_name) VALUES (%s, %s)", (self.user_id, category_name))
        conn.commit()
        conn.close()

        self.load_categories()
        messagebox.showinfo("Success", "Category Added Successfully!")
        self.category_entry.delete(0, tk.END)

    def save_expense(self):
        amount = self.expense_amount_entry.get()
        category_name = self.category_combobox.get()
        description = self.expense_description_entry.get()
        expense_date = self.expense_date_entry.get()

        category_id = [k for k, v in self.category_map.items() if v == category_name][0]

        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tbl_expenses (user_id, category_id, amount, description, expense_date) VALUES (%s, %s, %s, %s, %s)",
                       (self.user_id, category_id, amount, description, expense_date))
        conn.commit()
        conn.close()

        self.load_data()

    def save_income(self):
        amount = self.income_amount_entry.get()
        source = self.income_source_entry.get()
        income_date = self.income_date_entry.get()

        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tbl_income (user_id, amount, source, income_date) VALUES (%s, %s, %s, %s)",
                       (self.user_id, amount, source, income_date))
        conn.commit()
        conn.close()

        self.load_data()

    def load_data(self):
        self.summary_tree.delete(*self.summary_tree.get_children())
        conn = connect_to_db()
        cursor = conn.cursor()

        query = """
            SELECT 'Income', i.amount, i.source, '', i.income_date FROM tbl_income i WHERE i.user_id = %s
            UNION
            SELECT 'Expense', e.amount, c.category_name, e.description, e.expense_date
            FROM tbl_expenses e JOIN tbl_categories c ON e.category_id = c.category_id
            WHERE e.user_id = %s ORDER BY 5 DESC
        """
        cursor.execute(query, (self.user_id, self.user_id))
        for row in cursor.fetchall():
            self.summary_tree.insert("", "end", values=row)
        conn.close()

        self.draw_pie_chart()

    def draw_pie_chart(self):
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.category_name, SUM(e.amount) 
            FROM tbl_expenses e JOIN tbl_categories c ON e.category_id = c.category_id 
            WHERE e.user_id = %s GROUP BY c.category_name
        """, (self.user_id,))
        data = cursor.fetchall()
        conn.close()

        if data:
            categories, amounts = zip(*data)
            fig, ax = plt.subplots()
            ax.pie(amounts, labels=categories, autopct='%1.1f%%')
            ax.set_title("Expense Distribution")

            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()


if __name__ == "__main__":
    root = tk.Tk()
    ExpensePage(root, username="test_user", user_id=1)
    root.mainloop()