import tkinter as tk
from tkinter import font
import globals
import file_input
import settings
import passwords

class Home(tk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.master = master

        self.configure(bg=globals.bg_colour)

        for i in range(3):
            self.columnconfigure(i, weight=1)
        for i in range(2):
            self.rowconfigure(i, weight=1)

        self.title_label = RoundedLabel(
                                self,
                                text="LockBox",
                                bg=globals.primary_colour,
                                font=("Satoshi", 50, "bold"))
        self.title_label.grid(row=0, column=1)

        self.button_frame = Home_buttons(self, master)
        self.button_frame.grid(row=1, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

        self.exit_button = tk.Button(self, text="Exit", command=lambda: self.close(),
                                     bg=globals.secondary_colour, fg=globals.text_div_colour)
        self.exit_button.grid(row=0, column=2, sticky="ne")

    def close(self):
        self.master.destroy()


class Home_buttons(tk.Frame):
    def __init__(self, master, parent):
        super().__init__(master)
        self.parent = parent
        self.configure(bg = globals.bg_colour)

        for i in range(3):
            self.columnconfigure(i, weight = 1, uniform="buttons")

        self.compression_button =  tk.Button(self, text="File compression", 
                                            bg=globals.secondary_colour, 
                                            fg = globals.text_div_colour,
                                            font = ("Satoshi", 25, "bold"),
                                            command=lambda: parent.load_page(file_input.input_screen))
        self.compression_button.grid(row=0, column=0, sticky="ew", padx=40, pady=5)

        self.passwords_button =  tk.Button(self, text="Passwords", 
                                            bg=globals.secondary_colour, 
                                            fg = globals.text_div_colour,
                                            font = ("Satoshi", 25, "bold"),
                                            command=lambda: parent.load_page(passwords.passwords_screen))
        self.passwords_button.grid(row=0, column=1, sticky="ew", padx=40, pady=5)
            
        self.settings_button =  tk.Button(self, text="Settings", 
                                            bg=globals.secondary_colour, 
                                            fg = globals.text_div_colour,
                                            font = ("Satoshi", 25, "bold"),
                                            command=lambda: parent.load_page(settings.settings_screen))
        self.settings_button.grid(row=0, column=2, sticky="ew", padx=40, pady=5)
                 

class RoundedLabel(tk.Canvas):
    def __init__(
        self, parent, text, radius=20,
        bg="#1F6AE1", fg="white", font=None, padding=10
    ):
        super().__init__(parent, highlightthickness=0, bg=parent["bg"])

        self.text = text
        self.radius = radius
        self.bg_color = bg
        self.fg = fg
        self.font = font
        self.padding = padding

        self.draw()

    def draw(self):
        self.delete("all")

        f = font.Font(font=self.font or ("Satoshi", 25, "bold"))

        text_width = f.measure(self.text)
        text_height = f.metrics("linespace")

        w = text_width + self.padding * 2
        h = text_height + self.padding * 2

        self.config(width=w, height=h)

        r = self.radius

        self.create_arc(0, 0, r*2, r*2, start=90, extent=90, fill=self.bg_color, outline="")
        self.create_arc(w-r*2, 0, w, r*2, start=0, extent=90, fill=self.bg_color, outline="")
        self.create_arc(0, h-r*2, r*2, h, start=180, extent=90, fill=self.bg_color, outline="")
        self.create_arc(w-r*2, h-r*2, w, h, start=270, extent=90, fill=self.bg_color, outline="")

        self.create_rectangle(r, 0, w-r, h, fill=self.bg_color, outline="")
        self.create_rectangle(0, r, w, h-r, fill=self.bg_color, outline="")

        self.create_text(
            w // 2, h // 2,
            text=self.text,
            fill=self.fg,
            font=f
        )