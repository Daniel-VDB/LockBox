import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import globals
from password_editor import password_editor_screen
import home

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Window

class passwords_screen(tk.Frame):
    def __init__(self, master: "Window"):
        super().__init__(master)
        self.master: "Window" = master
        self.configure(bg=globals.bg_colour)

        style = ttk.Style()
        style.theme_use("default")

        style.configure("Custom.Treeview",
                background=globals.secondary_colour,     #background of rows
                foreground=globals.text_div_colour,           #text color
                fieldbackground=globals.secondary_colour, #background of the treeview itself
                font=("Satoshi", 12))
        
        style.configure("Custom.Treeview.Heading",
                background=globals.primary_colour,
                foreground=globals.text_div_colour,
                font=("Satoshi", 12, "bold"))

        top_frame = tk.Frame(self, bg=globals.bg_colour)
        top_frame.pack(fill="x", pady=10, padx=20)

        #title
        title_label = tk.Label(
            top_frame,
            text="Your Passwords",
            font=("Satoshi", 40, "bold"),
            bg=globals.primary_colour,
            fg=globals.text_div_colour
        )
        title_label.grid(row=0, column=0, sticky="w", padx=(0, 10))

        #home button
        home_button = tk.Button(
            top_frame,
            text="Home",
            font=("Satoshi", 20, "bold"),
            bg=globals.secondary_colour,
            fg=globals.text_div_colour,
            command=lambda: self.master.load_page(home.Home)
        )
        home_button.grid(row=0, column=1, sticky="e")
        top_frame.columnconfigure(0, weight=1)

        #frame for table and scrollbar
        table_frame = tk.Frame(self, bg=globals.bg_colour)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        #scrollbar
        self.scrollbar = tk.Scrollbar(table_frame)
        self.scrollbar.pack(side="right", fill="y")

        #treeview (table)
        self.tree = ttk.Treeview(
            table_frame,
            columns=("Service", "Username", "Password", "Email", "Notes", "Last Updated"),
            show="headings",
            yscrollcommand=self.scrollbar.set,
            selectmode="browse",
            style="Custom.Treeview"  
        )
        self.tree.pack(fill="both", expand=True)
        self.scrollbar.config(command=self.tree.yview)

        #define headings
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        #buttons
        button_frame = tk.Frame(self, bg=globals.bg_colour)
        button_frame.pack(pady=10)

        add_button = tk.Button(
            button_frame,
            text="Add New Password",
            font=("Satoshi", 20, "bold"),
            bg=globals.secondary_colour,
            fg=globals.text_div_colour,
            command=self.add_password
        )
        add_button.grid(row=0, column=0, padx=10)

        edit_button = tk.Button(
            button_frame,
            text="Edit Selected Password",
            font=("Satoshi", 20, "bold"),
            bg=globals.secondary_colour,
            fg=globals.text_div_colour,
            command=self.edit_password
        )
        edit_button.grid(row=0, column=1, padx=10)

        refresh_button = tk.Button(
            button_frame,
            text="Refresh",
            font=("Satoshi", 20, "bold"),
            bg=globals.secondary_colour,
            fg=globals.text_div_colour,
            command=self.load_passwords
        )
        refresh_button.grid(row=0, column=2, padx=10)
        
        show_button = tk.Button(
        button_frame,
        text="Show Password",
        font=("Satoshi", 20, "bold"),
        bg="#1F6AE1",  #blue button
        fg="white",
        command=self.show_password
        )
        show_button.grid(row=0, column=3, padx=10)


        #get passwords from database
        self.load_passwords()

    def load_passwords(self):
        #clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        conn = sqlite3.connect("password_manager.db")
        db = conn.cursor()

        #fetch passwords but mask them in the display
        db.execute("SELECT id, service_name, username, password, email, notes, last_updated FROM passwords")
        for row in db.fetchall():
            masked_password = "******"  # mask the password
            display_values = [row[1], row[2], masked_password, row[4], row[5], row[6]]
            self.tree.insert("", "end", iid=row[0], values=display_values)
        conn.close()

    def add_password(self):
        self.master.load_page(lambda master: password_editor_screen(master, new=True))

    def edit_password(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a password to edit.")
            return
        self.master.load_page(lambda master: password_editor_screen(master, new=False, password_id=selected))
    
    def show_password(self):
        #Show the password for the selected row in a popup
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a password to show.")
            return

        conn = sqlite3.connect("password_manager.db")
        db = conn.cursor()
        db.execute("SELECT password FROM passwords WHERE id = ?", (selected,))
        row = db.fetchone()
        conn.close()

        if row:
            password = row[0]
            messagebox.showinfo("Password", f"The password is:\n\n{password}")
        else:
            messagebox.showerror("Error", "Password not found.")


