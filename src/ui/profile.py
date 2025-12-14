import tkinter as tk
from tkinter import messagebox
import mysql.connector
from database.db_connection import connect_to_db
from ui.styles import *

class ProfilePage:
    def __init__(self, parent, user_id):
        self.parent = parent
        self.user_id = user_id

        # Main Frame with Background
        main_frame = tk.Frame(self.parent, padx=50, pady=50, bg=BG_COLOR)
        main_frame.pack(fill="both", expand=True)

        # Header
        tk.Label(main_frame, text="My Profile", font=FONT_HEADER, bg=BG_COLOR, fg=THEME_COLOR).pack(pady=(0, 40))

        # Card Frame
        card = tk.Frame(main_frame, bg="white", padx=40, pady=40, bd=0)
        card.pack()

        # Input Variables
        self.phone_var = tk.StringVar()
        self.address_var = tk.StringVar()

        # Phone
        tk.Label(card, text="Phone Number", font=FONT_BOLD, bg="white").pack(anchor="w", pady=(10, 5))
        tk.Entry(card, textvariable=self.phone_var, font=FONT_BODY, width=30, bd=2, relief="groove").pack(pady=5, ipady=3)

        # Address
        tk.Label(card, text="Address", font=FONT_BOLD, bg="white").pack(anchor="w", pady=(20, 5))
        tk.Entry(card, textvariable=self.address_var, font=FONT_BODY, width=30, bd=2, relief="groove").pack(pady=5, ipady=3)

        # Update Button
        tk.Button(card, text="Update Profile", command=self.update_profile, **BTN_STYLE).pack(pady=30, fill="x")

        self.load_user_details()

    def load_user_details(self):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT username, phone, address FROM tbl_users WHERE user_id = %s", (self.user_id,))
        user = cursor.fetchone()
        conn.close()

        if user:
            # self.username = user[0] # Username is not displayed as an editable field in the new design
            self.phone_var.set(user[1])
            self.address_var.set(user[2])

    def update_profile(self):
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tbl_users 
            SET phone = %s, address = %s 
            WHERE user_id = %s
        """, (self.phone_var.get(), self.address_var.get(), self.user_id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Profile updated successfully!")
