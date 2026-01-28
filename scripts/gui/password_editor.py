import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import globals

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Window

class password_editor_screen(tk.Frame):
    def __init__(self, master: "Window", new=False, password_id=None):
        super().__init__(master)
        self.master: "Window" = master
        self.new = new
        self.password_id = password_id
        self.configure(bg=globals.bg_colour)

        #title
        title_text = "Add New Password" if self.new else "Edit Password"
        tk.Label(
            self,
            text=title_text,
            font=("Satoshi", 40, "bold"),
            bg=globals.primary_colour,
            fg=globals.text_div_colour
        ).pack(pady=20)

        #form fields
        form_frame = tk.Frame(self, bg=globals.bg_colour)
        form_frame.pack(padx=50, pady=20)

        tk.Label(form_frame, text="Service Name:", font=("Satoshi", 20), bg=globals.bg_colour, fg=globals.text_div_colour).grid(row=0, column=0, sticky="e", pady=5)
        self.service_entry = tk.Entry(form_frame, font=("Satoshi", 20), width=30)
        self.service_entry.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Username:", font=("Satoshi", 20), bg=globals.bg_colour, fg=globals.text_div_colour).grid(row=1, column=0, sticky="e", pady=5)
        self.username_entry = tk.Entry(form_frame, font=("Satoshi", 20), width=30)
        self.username_entry.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Email:", font=("Satoshi", 20), bg=globals.bg_colour, fg=globals.text_div_colour).grid(row=2, column=0, sticky="e", pady=5)
        self.email_entry = tk.Entry(form_frame, font=("Satoshi", 20), width=30)
        self.email_entry.grid(row=2, column=1, pady=5)

        tk.Label(form_frame, text="Password:", font=("Satoshi", 20), bg=globals.bg_colour, fg=globals.text_div_colour).grid(row=3, column=0, sticky="e", pady=5)
        self.password_entry = tk.Entry(form_frame, font=("Satoshi", 20), width=30)
        self.password_entry.grid(row=3, column=1, pady=5)

        tk.Label(form_frame, text="Notes:", font=("Satoshi", 20), bg=globals.bg_colour, fg=globals.text_div_colour).grid(row=4, column=0, sticky="ne", pady=5)
        self.notes_entry = tk.Text(form_frame, font=("Satoshi", 18), width=30, height=5)
        self.notes_entry.grid(row=4, column=1, pady=5)

        #buttons
        button_frame = tk.Frame(self, bg=globals.bg_colour)
        button_frame.pack(pady=20)

        save_button = tk.Button(
            button_frame,
            text="Save",
            font=("Satoshi", 20, "bold"),
            bg=globals.secondary_colour,
            fg=globals.text_div_colour,
            command=self.save_password
        )
        save_button.grid(row=0, column=0, padx=10)

        cancel_button = tk.Button(
            button_frame,
            text="Cancel",
            font=("Satoshi", 20, "bold"),
            bg=globals.secondary_colour,
            fg=globals.text_div_colour,
            command=lambda: self.master.load_page(lambda master: __import__('passwords').passwords_screen(master))
        )
        cancel_button.grid(row=0, column=1, padx=10)

        #delete button (only if editing an existing password)
        if not self.new and self.password_id is not None:
            delete_button = tk.Button(
                button_frame,
                text="Delete",
                font=("Satoshi", 20, "bold"),
                bg="#E53935",  # red
                fg="white",
                command=self.delete_password
            )
            delete_button.grid(row=0, column=2, padx=10)

        #if editing, load existing data
        if not self.new and self.password_id is not None:
            self.load_existing_password()

    def load_existing_password(self):
        #load data for the password being edited
        conn = sqlite3.connect("password_manager.db")
        db = conn.cursor()
        db.execute("SELECT service_name, username, email, password, notes FROM passwords WHERE id = ?", (self.password_id,))
        row = db.fetchone()
        conn.close()

        if row:
            self.service_entry.insert(0, row[0])
            self.username_entry.insert(0, row[1])
            self.email_entry.insert(0, row[2])
            self.password_entry.insert(0, row[3])
            self.notes_entry.insert("1.0", row[4])

    def save_password(self):
        #insert or update password in the database
        service = self.service_entry.get().strip()
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        notes = self.notes_entry.get("1.0", "end").strip()

        if not service or not username or not password:
            messagebox.showerror("Missing Data", "Service, Username, and Password are required.")
            return

        conn = sqlite3.connect("password_manager.db")
        db = conn.cursor()
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if self.new:
            db.execute("""
                INSERT INTO passwords (service_name, username, password, email, notes, date_created, last_updated)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (service, username, password, email, notes, now, now))
        else:
            db.execute("""
                UPDATE passwords
                SET service_name = ?, username = ?, password = ?, email = ?, notes = ?, last_updated = ?
                WHERE id = ?
            """, (service, username, password, email, notes, now, self.password_id))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Password saved successfully!")
        self.master.load_page(lambda master: __import__('passwords').passwords_screen(master))

    def delete_password(self):
        #Delete the current password from the database
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this password?")
        if not confirm:
            return

        conn = sqlite3.connect("password_manager.db")
        db = conn.cursor()
        db.execute("DELETE FROM passwords WHERE id = ?", (self.password_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Deleted", "Password deleted successfully!")
        self.master.load_page(lambda master: __import__('passwords').passwords_screen(master))
