import tkinter as tk
import globals
import home

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Window

class settings_screen(tk.Frame):
    def __init__(self, master: "Window"):
        super().__init__(master)
        self.master: "Window" = master
        self.configure(bg=globals.bg_colour)

        #top frame for title + home button
        top_frame = tk.Frame(self, bg=globals.bg_colour)
        top_frame.pack(fill="x", pady=10, padx=20)

        #title
        title_label = tk.Label(
            top_frame,
            text="Settings",
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

        #frame for content
        content_frame = tk.Frame(self, bg=globals.bg_colour)
        content_frame.pack(fill="both", expand=True, pady=50)

        #dark mode toggle button
        self.toggle_button = tk.Button(
            content_frame,
            text="Toggle Dark Mode",
            font=("Satoshi", 25, "bold"),
            bg=globals.secondary_colour,
            fg=globals.text_div_colour,
            width=20,
            command=self.toggle_dark_mode
        )
        self.toggle_button.pack(pady=20)

        #display current mode
        self.mode_label = tk.Label(
            content_frame,
            text=f"Current mode: {'Dark' if globals.is_dark else 'Light'}",
            font=("Satoshi", 20),
            bg=globals.bg_colour,
            fg=globals.text_div_colour
        )
        self.mode_label.pack(pady=10)

    def toggle_dark_mode(self):
        #toggle between dark and light mode, refresh the settings page
        if globals.is_dark:
            globals.light_mode()
        else:
            globals.dark_mode()

        # Reload the settings page to refresh colors
        self.master.load_page(settings_screen)
