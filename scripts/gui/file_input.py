import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import font
import ctypes
import globals
from pathlib import Path

ctypes.windll.shcore.SetProcessDpiAwareness(1) #makes tkinter not look like its the 1990s

if __name__ == "__main__":
    lib = ctypes.CDLL('./scripts/c_scripts/handler.dll')


    lib.say_hello.argtypes = [ctypes.c_char_p]
    lib.say_hello.restype = None

    s = "Daniel"
    res = s.encode("utf-8")
    lib.say_hello(res)

#for strings, encode to bytes before passing, EX:
#name_bytes = b"PythonUser"
#lib.greet(name_bytes)


class input_screen(tk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.master = master
        self.configure(bg=globals.bg_colour)

        #page
        self.grid(row=0, column=0, sticky="nsew")
        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)
        
        self.rowconfigure(0, weight=0)   
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)

        #exit button (top-right)
        exit_btn = tk.Button(
            self,
            text="Exit",
            command=self.master.destroy,
            bg=globals.secondary_colour,
            fg=globals.text_div_colour
        )
        exit_btn.grid(row=0, column=0, sticky="ne", padx=10, pady=10)

        #center container
        center_container = tk.Frame(self, bg=globals.bg_colour)
        center_container.grid(row=1, column=0)
        
        center_container.columnconfigure(0, weight=1)
        center_container.columnconfigure(1, weight=1)

        #top box
        top_box = file_input_frame(center_container)
        top_box.grid(row=0, column=0, padx=20, pady=20)

        #middle box (placeholder)
        middle_box = tk.Frame(
            center_container,
            bg=globals.secondary_colour,
            width=800,
            height=200,
            highlightbackground=globals.primary_colour,
            highlightthickness=1
        )
        middle_box.grid(row=1, column=0, padx=20, pady=20)
        middle_box.grid_propagate(False)

        #bottom box (placeholder)
        bottom_box = tk.Frame(
            center_container,
            bg=globals.secondary_colour,
            width=800,
            height=200,
            highlightbackground=globals.primary_colour,
            highlightthickness=1
        )
        bottom_box.grid(row=2, column=0, padx=20, pady=20)
        bottom_box.grid_propagate(False)

class file_input_frame(tk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master, bg=globals.bg_colour)  # table background grey

        self.files = {}
        self.file_rows = []

        self.configure(
            width=800,
            height=200,
            highlightbackground=globals.primary_colour,
            highlightthickness=1
        )
        self.grid_propagate(False)
        
        #column weights for table columns
        for i in range(3):
            self.columnconfigure(i, weight=1)

        #import button
        self.import_button = tk.Button(
            self,
            text="Import File",
            command=self.import_file,
            bg=globals.secondary_colour,
            fg=globals.text_div_colour,
            relief="raised",
            borderwidth=1
        )
        self.import_button.grid(row=0, column=0, sticky="ns", pady=5)

        self.compress_button = tk.Button(
            self,
            text="Compress",
            command=self.import_file,
            bg=globals.secondary_colour,
            fg=globals.text_div_colour,
            relief="raised",
            borderwidth=1
        )
        self.compress_button.grid(row=0, column=2, sticky="ns", pady=5)

        #header row
        tk.Label(self, text="File Name", bg=globals.secondary_colour, fg=globals.text_div_colour).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Label(self, text="Extension", bg=globals.secondary_colour, fg=globals.text_div_colour).grid(row=1, column=1, padx=10, pady=5, sticky="w")
        tk.Label(self, text="Size", bg=globals.secondary_colour, fg=globals.text_div_colour).grid(row=1, column=2, padx=10, pady=5, sticky="w")

    def append_file_display(self, path):
        #row number: header=1, import button=0
        row = len(self.file_rows) + 2

        #shorten long file names
        if len(path.name) > 30:
            file_name = path.name[:28] + "..."
        else:
            file_name = path.name

        #labels go directly in parent grid to stay aligned
        name_label = tk.Label(self, text=file_name, bg=globals.bg_colour, fg=globals.text_high_contrast, anchor="w")
        extension_label = tk.Label(self, text=path.suffix, bg=globals.bg_colour, fg=globals.text_high_contrast, anchor="w")
        size_label = tk.Label(self, text="3mb", bg=globals.bg_colour, fg=globals.text_high_contrast, anchor="w")

        name_label.grid(row=row, column=0, sticky="w", padx=10, pady=2)
        extension_label.grid(row=row, column=1, sticky="w", padx=10, pady=2)
        size_label.grid(row=row, column=2, sticky="w", padx=10, pady=2)

        self.file_rows.append((name_label, extension_label, size_label))

    def import_file(self):
        file_path = filedialog.askopenfilename(title="Select a file")
        if file_path:
            path = Path(file_path)
            file_index = len(self.file_rows)
            if path not in self.files.values():
                self.files[file_index] = path
                self.append_file_display(path)
