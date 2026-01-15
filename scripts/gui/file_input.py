import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import font
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1) #makes tkinter not look like its the 1990s

lib = ctypes.CDLL('./scripts/c_scripts/handler.dll')


lib.say_hello.argtypes = [ctypes.c_char_p]
lib.say_hello.restype = None

s = "Daniel"
res = s.encode("utf-8")
lib.say_hello(res)

#for strings, encode to bytes before passing, EX:
#name_bytes = b"PythonUser"
#lib.greet(name_bytes)

def main() -> None:
    page = input_screen()
    page.mainloop()

class input_screen(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        for name in (
            "TkDefaultFont",
            "TkTextFont",
            "TkHeadingFont",
            "TkMenuFont"
        ):
            font.nametofont(name).configure(
                family="Consolas",
                size=11,
                weight="bold"
            )

        #configuring the page
        self.attributes('-fullscreen', True)
        self.title("LockBox")
        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        self.configure(bg="#272822")

        input_field = file_input_frame(self)
        input_field.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)


class file_input_frame(tk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        #configuring this frame
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=1)
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        style = ttk.Style()
        style.configure("Black.TFrame", background="#272822", foreground="#546c8f")
        
        self.import_button = tk.Button(self, text="Import File", command=self.import_file,
                                     bg="#34352F", fg="#D2D6BE")
        self.import_button.grid(row=0, column=0)

        self.exit_button = tk.Button(self, text="Exit", command=lambda: self.close(parent),
                                     bg="#34352F", fg="#D2D6BE")
        self.exit_button.grid(row=0, column=1, sticky="ne")

    def import_file(self):
        file_path = filedialog.askopenfilename(title="Select a file")
        if file_path:
            print("Selected file:", file_path)
    
    def close(self, parent):
        parent.destroy()

if __name__ == "__main__":
    main()