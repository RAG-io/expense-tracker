import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database.db_connection import connect_to_db

from ui.styles import *

class Dashboard:
    def __init__(self, parent):
        self.frame = tk.Frame(parent, bg=BG_COLOR)
        self.frame.pack(fill="both", expand=True)

        # Scrollable Canvas
        canvas = tk.Canvas(self.frame, bg=BG_COLOR, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = tk.Frame(canvas, bg=BG_COLOR)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        scrollbar.pack(side="right", fill="y")

        # Header
        tk.Label(self.scrollable_frame, text="Admin Dashboard", font=FONT_HEADER, bg=BG_COLOR, fg=THEME_COLOR).pack(pady=(0, 20), anchor="w")

        # ---------------- UPPER DIVISION (Stats) ----------------
        self.upper_frame = tk.Frame(self.scrollable_frame, bg=BG_COLOR)
        self.upper_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(self.upper_frame, text="Overview", font=FONT_SUBHEADER, bg=BG_COLOR, fg="#555").pack(anchor="w", padx=20)
        
        # Stats Container
        stats_container = tk.Frame(self.upper_frame, bg=BG_COLOR)
        stats_container.pack(fill="x", pady=10)

        # Fetch Data
        total_users, total_expenses, total_income, category_expenses = self.fetch_data()

        # Stats Cards
        self.create_stat_card(stats_container, "Total Users", total_users, "#007BFF")
        self.create_stat_card(stats_container, "Total Expenses", f"₹{total_expenses}", "#DC3545")
        self.create_stat_card(stats_container, "Total Income", f"₹{total_income}", "#28A745")

        # ---------------- LOWER DIVISION (Visualizations) ----------------
        self.lower_frame = tk.Frame(self.scrollable_frame, bg="white", padx=20, pady=20)
        self.lower_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(self.lower_frame, text="Visual Analytics", font=FONT_SUBHEADER, bg="white", fg="#555").pack(anchor="w", pady=(0, 20))

        # Chart Grid
        chart_grid = tk.Frame(self.lower_frame, bg="white")
        chart_grid.pack(fill="both", expand=True)

        # Pie Chart (Left)
        self.display_pie_chart(chart_grid, category_expenses)
        
        # Bar Chart (Right)
        self.display_bar_chart(chart_grid)
        
        # Line Chart (Bottom, Full Width)
        self.display_line_chart(self.lower_frame)

    def create_stat_card(self, parent, title, value, color):
        """Creates a stat box with a title and value"""
        card = tk.Frame(parent, bg="white", width=250, height=120, padx=20, pady=15)
        card.pack(side="left", padx=15, pady=10)
        
        # Add a colored strip on the left
        strip = tk.Frame(card, bg=color, width=5, height=120)
        strip.place(x=0, y=0, relheight=1)

        tk.Label(card, text=title, font=("Arial", 10, "bold"), fg="gray", bg="white").pack(anchor="w", padx=(10, 0))
        tk.Label(card, text=value, font=("Arial", 20, "bold"), fg=TEXT_COLOR, bg="white").pack(anchor="w", padx=(10, 0), pady=(5, 0))
        
        # Prevent card from shrinking
        card.pack_propagate(False)

    def fetch_data(self):
        """Fetch total users, expenses, and income from the database"""
        conn = connect_to_db()
        cursor = conn.cursor()

        # Get total users
        cursor.execute("SELECT COUNT(*) FROM tbl_users")
        total_users = cursor.fetchone()[0]

        # Get total expenses
        cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM tbl_expenses")
        total_expenses = cursor.fetchone()[0]

        # Get total income
        cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM tbl_income")
        total_income = cursor.fetchone()[0]

        # Get expenses by category
        cursor.execute("""
            SELECT c.category_name, COALESCE(SUM(e.amount), 0)
            FROM tbl_categories c
            LEFT JOIN tbl_expenses e ON c.category_id = e.category_id
            GROUP BY c.category_name
        """)
        category_expenses = cursor.fetchall()

        conn.close()
        return total_users, total_expenses, total_income, category_expenses

    def display_pie_chart(self, parent, category_expenses):
        if not category_expenses:
            return

        categories, amounts = zip(*category_expenses) if category_expenses else ([], [])

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.pie(amounts, labels=categories, autopct='%1.1f%%', colors=plt.cm.Paired.colors, startangle=140)
        ax.set_title("Expenses by Category")

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.get_tk_widget().pack(side="left", fill="both", expand=True, padx=10)
        canvas.draw()
        
    def display_bar_chart(self, parent):
        conn = connect_to_db()
        cursor = conn.cursor()
        
        # Monthly Income vs Expense
        cursor.execute("""
            SELECT MONTHNAME(expense_date), SUM(amount) FROM tbl_expenses 
            GROUP BY YEAR(expense_date), MONTH(expense_date)
            ORDER BY expense_date DESC LIMIT 6
        """)
        expenses = dict(cursor.fetchall())
        
        cursor.execute("""
            SELECT MONTHNAME(income_date), SUM(amount) FROM tbl_income
            GROUP BY YEAR(income_date), MONTH(income_date)
            ORDER BY income_date DESC LIMIT 6
        """)
        income = dict(cursor.fetchall())
        conn.close()
        
        if not expenses and not income:
            return

        months = list(set(expenses.keys()) | set(income.keys()))
        expense_vals = [expenses.get(m, 0) for m in months]
        income_vals = [income.get(m, 0) for m in months]

        fig, ax = plt.subplots(figsize=(5, 4))
        x = range(len(months))
        width = 0.4
        
        ax.bar([i - width/2 for i in x], income_vals, width, label='Income', color='green')
        ax.bar([i + width/2 for i in x], expense_vals, width, label='Expense', color='red')
        
        ax.set_xticks(x)
        ax.set_xticklabels(months)
        ax.legend()
        ax.set_title("Income vs Expense")
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.get_tk_widget().pack(side="right", fill="both", expand=True, padx=10)
        canvas.draw()

    def display_line_chart(self, parent):
        conn = connect_to_db()
        cursor = conn.cursor()
        
        # Daily Expense Trend (Last 30 Days)
        cursor.execute("""
            SELECT date(expense_date), SUM(amount) FROM tbl_expenses 
            WHERE expense_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            GROUP BY date(expense_date)
            ORDER BY date(expense_date)
        """)
        data = cursor.fetchall()
        conn.close()
        
        if not data:
            return
            
        dates, amounts = zip(*data)
        
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot(dates, amounts, marker='o', linestyle='-', color='blue')
        ax.set_title("Daily Expense Trend (Last 30 Days)")
        ax.tick_params(axis='x', rotation=45)
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.get_tk_widget().pack(fill="x",  pady=20)
        canvas.draw()

# Example Usage
if __name__ == "__main__":
    root = tk.Tk()
    Dashboard(root)
    root.mainloop()
