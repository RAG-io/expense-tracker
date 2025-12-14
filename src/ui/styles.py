# src/ui/styles.py
import tkinter as tk
from tkinter import ttk

THEME_COLOR = "#083013"
TEXT_COLOR = "#333333"
BG_COLOR = "#f4f4f4"
WHITE = "#ffffff"

FONT_HEADER = ("Arial", 22, "bold")
FONT_SUBHEADER = ("Arial", 16, "bold")
FONT_BODY = ("Arial", 12)
FONT_BOLD = ("Arial", 12, "bold")

# Button Styles
BTN_STYLE = {
    "bg": THEME_COLOR,
    "fg": WHITE,
    "font": FONT_BOLD,
    "bd": 0,
    "padx": 20,
    "pady": 12,
    "cursor": "hand2",
    "activebackground": "#0a401a",
    "activeforeground": WHITE
}

SIDEBAR_BTN_STYLE = {
    "bg": "#e0e0e0",
    "fg": "black",
    "font": FONT_BOLD,
    "bd": 0,
    "padx": 20,
    "pady": 15,
    "width": 18,
    "cursor": "hand2",
    "anchor": "w"
}

# Styles for Widgets
def apply_tree_style():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", 
                    background=WHITE, 
                    foreground=TEXT_COLOR, 
                    rowheight=35, 
                    fieldbackground=WHITE,
                    font=FONT_BODY)
    style.configure("Treeview.Heading", 
                    font=FONT_BOLD, 
                    background="#d9d9d9", 
                    foreground="black")
    style.map("Treeview", background=[("selected", THEME_COLOR)])
