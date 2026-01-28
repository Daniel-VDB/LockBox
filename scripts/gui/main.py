import ctypes
import globals
import tkinter as tk
from tkinter import font
import home
import sqlite3
from datetime import datetime


ctypes.windll.shcore.SetProcessDpiAwareness(1) #makes tkinter not look like its the 1990s

def main() -> None:
    create_database()
    globals.light_mode()
    window = Window()
    window.mainloop()

class Window(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        for name in (
        "TkDefaultFont",
            "TkTextFont",
            "TkHeadingFont",
            "TkMenuFont"
        ):
            font.nametofont(name).configure(
                family="Satoshi",
                size=11,
            )
        self.title("LockBox")
        self.current_frame = None
        self.load_page(home.Home) 
        self.attributes('-fullscreen', True) 

    def load_page(self, page_class):
        if self.current_frame is not None:
            self.current_frame.destroy()
        self.current_frame = page_class(self)
        self.current_frame.pack(fill="both", expand=True)


def create_database():
    #connect to the database (or create it if it doesn't exist)
    conn = sqlite3.connect('password_manager.db')
    db = conn.cursor()

    #create a table for storing passwords and related data
    db.execute('''
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        service_name TEXT NOT NULL,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        email TEXT,
        notes TEXT,
        date_created TEXT NOT NULL,
        last_updated TEXT NOT NULL
    )
    ''')

    #commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()