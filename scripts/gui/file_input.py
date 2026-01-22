import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from pathlib import Path
import ctypes
from ctypes import CDLL, c_char_p, c_int
import globals

ctypes.windll.shcore.SetProcessDpiAwareness(1)  #makes tkinter look sharp on high DPI

dll_path = Path(__file__).parent.parent / "c_scripts" / "handler.dll"
dll = CDLL(str(dll_path))

dll.process_file.argtypes = [c_char_p, c_char_p, c_char_p]
dll.process_file.restype = c_int

dll.deprocess_file.argtypes = [c_char_p, c_char_p, c_char_p]
dll.deprocess_file.restype = c_int

def deprocess(src_file, dst_file, password):
    return dll.deprocess_file(src_file.encode(), dst_file.encode(), password.encode())

def process(src_file, dst_file, password):
    return dll.process_file(src_file.encode(), dst_file.encode(), password.encode())

#-------------------- Main Screen --------------------
class input_screen(tk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master)
        self.master = master
        self.configure(bg=globals.bg_colour)

        # page layout
        self.grid(row=0, column=0, sticky="nsew")
        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)

        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)

        # exit button
        exit_button = tk.Button(
            self,
            text="Exit",
            command=self.master.destroy,
            bg=globals.secondary_colour,
            fg=globals.text_div_colour
        )
        exit_button.grid(row=0, column=0, sticky="ne", padx=10, pady=10)

        # center container
        center_container = tk.Frame(self, bg=globals.bg_colour)
        center_container.grid(row=1, column=0)
        center_container.columnconfigure(0, weight=1)
        center_container.columnconfigure(1, weight=1)

        # top box: file input
        top_box = file_input_frame(center_container)
        top_box.grid(row=0, column=0, padx=20, pady=20)

        # bottom box: statistics
        bottom_box = stats_frame(center_container)
        bottom_box.grid(row=2, column=0, padx=20, pady=20)

        # middle box: encryption/decryption
        middle_box = encryption_frame(center_container, top_box, bottom_box)
        middle_box.grid(row=1, column=0, padx=20, pady=20)

# -------------------- File Input Frame --------------------
class file_input_frame(tk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master, bg=globals.bg_colour)
        self.files = {}
        self.file_rows = []

        self.configure(width=800, height=200, highlightbackground=globals.primary_colour, highlightthickness=1)
        self.grid_propagate(False)

        #column weights
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

        #header labels
        tk.Label(self, text="File Name", bg=globals.secondary_colour, fg=globals.text_div_colour).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        tk.Label(self, text="Extension", bg=globals.secondary_colour, fg=globals.text_div_colour).grid(row=1, column=1, padx=10, pady=5, sticky="w")
        tk.Label(self, text="Size", bg=globals.secondary_colour, fg=globals.text_div_colour).grid(row=1, column=2, padx=10, pady=5, sticky="w")

    def append_file_display(self, path):
        row = len(self.file_rows) + 2

        file_name = path.stem if len(path.name) <= 30 else path.stem[:28] + "..."

        #defining labels
        name_label = tk.Label(self, text=file_name, bg=globals.bg_colour, fg=globals.text_high_contrast, anchor="w")
        extension_label = tk.Label(self, text=path.suffix, bg=globals.bg_colour, fg=globals.text_high_contrast, anchor="w")
        size_label = tk.Label(self, text=human_readable_size(path.stat().st_size), bg=globals.bg_colour, fg=globals.text_high_contrast, anchor="w")

        #gridding labels
        name_label.grid(row=row, column=0, sticky="w", padx=10, pady=2)
        extension_label.grid(row=row, column=1, sticky="w", padx=10, pady=2)
        size_label.grid(row=row, column=2, sticky="w", padx=10, pady=2)

        #appending the file
        self.file_rows.append((name_label, extension_label, size_label))

    def import_file(self):
        file_path = filedialog.askopenfilename(title="Select a file")
        if file_path:
            path = Path(file_path)
            file_index = len(self.file_rows)
            if path not in self.files.values():
                self.files[file_index] = path
                self.append_file_display(path)

    def clear_files(self):
        for row in self.file_rows:
            for widget in row:
                widget.destroy()
        self.file_rows.clear()
        self.files.clear()


#-------------------- Encryption Frame --------------------
class encryption_frame(tk.Frame):
    def __init__(self, master, file_frame: file_input_frame, stats_box: stats_frame) -> None:
        super().__init__(master, bg=globals.secondary_colour)
        self.file_frame = file_frame
        self.stats_box = stats_box  # <- store stats box reference

        self.configure(width=800, height=200, highlightbackground=globals.primary_colour, highlightthickness=1)
        self.grid_propagate(False)

        # layout columns
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=1)

        # password entry
        self.password_label = tk.Label(self, text="Encryption Password", bg=globals.secondary_colour, fg=globals.text_div_colour)
        self.password_label.grid(row=0, column=0, padx=20, pady=10, sticky="e")

        self.password_entry = tk.Entry(self, width=30)
        self.password_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # encode/decode mode toggle
        self.encode_mode = tk.BooleanVar(value=True)
        self.mode_checkbox = tk.Checkbutton(
            self,
            text="Change mode",
            variable=self.encode_mode,
            bg=globals.secondary_colour,
            fg=globals.text_div_colour,
            activebackground=globals.secondary_colour,
            command=self.update_button_text
        )
        self.mode_checkbox.grid(row=1, column=1, sticky="w", padx=10)

        # action button
        self.action_button = tk.Button(
            self,
            text="Compress & Encrypt file",
            bg=globals.primary_colour,
            fg=globals.text_div_colour,
            command=self.run_action
        )
        self.action_button.grid(row=0, column=2, padx=20, pady=10)

    def update_button_text(self):
        if self.encode_mode.get():
            self.action_button.config(text="Compress & Encrypt file")
        else:
            self.action_button.config(text="Restore file")

    def run_action(self):
        password = self.password_entry.get()
        is_encode = self.encode_mode.get()
        file_paths = list(self.file_frame.files.values())

        # check for password
        if not password:
            ctypes.windll.user32.MessageBoxW(0, "Password required", "Input error", 0x10)
            return

        # check for files
        if not file_paths:
            ctypes.windll.user32.MessageBoxW(0, "No files selected", "Input error", 0x10)
            return

        # file extension check
        if not is_encode:
            invalid = [p for p in file_paths if p.suffix.lower() != ".zst"]
            if invalid:
                msg = "Decode mode requires .zst files only:\n\n" + "\n".join(p.name for p in invalid)
                ctypes.windll.user32.MessageBoxW(0, msg, "Invalid file type", 0x10)
                return

        # choose destination
        destination = filedialog.askdirectory(title="Select output destination")
        if not destination:
            return

        # call encode/decode and pass stats_box
        try:
            encode(
                password=password,
                is_encode=is_encode,
                file_paths=file_paths,
                destination=Path(destination),
                stats_box=self.stats_box  # <- pass stats frame here
            )
        except ValueError as e:
            ctypes.windll.user32.MessageBoxW(0, str(e), "Input error", 0x10)
            return

        # clear top box after processing
        self.file_frame.clear_files()

# -------------------- Encode/Decode Function --------------------
def encode(password: str, is_encode: bool, file_paths: list, destination: Path, stats_box=None):
    initial_total_size = sum(path.stat().st_size for path in file_paths)
    final_total_size = 0
    success = True

    for path in file_paths:
        try:
            if is_encode:
                # Keep original extension and add .zst
                # Handles filenames with multiple dots correctly
                original_name = path.name  # e.g., 'lorem.ipsum.txt'
                destination_name = destination / f"{original_name}.zst"

                result = process(str(path.resolve()), str(destination_name.resolve()), password)
                if result != 0:
                    success = False

                if Path(destination_name).exists():
                    final_total_size += Path(destination_name).stat().st_size

            else:
                # Remove only the last .zst, keep everything else
                if path.suffix.lower() == ".zst":
                    original_name = path.name[:-4]  # removes last 4 chars ".zst"
                    destination_name = destination / original_name
                else:
                    destination_name = destination / path.name

                result = deprocess(str(path.resolve()), str(destination_name.resolve()), password)
                if result != 0:
                    success = False

                if Path(destination_name).exists():
                    final_total_size += Path(destination_name).stat().st_size

        except Exception as e:
            print(f"Error processing {path}: {e}")
            success = False

    # Update statistics frame
    if stats_box:
        stats_box.update_stats(
            initial_size=initial_total_size,
            final_size=final_total_size,
            password=password,
            num_files=len(file_paths),
            success=success
        )


def human_readable_size(size_bytes) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f}{unit}"
        size_bytes /= 1024
    return "0B"

# -------------------- Statistics Frame --------------------
class stats_frame(tk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master, bg=globals.bg_colour)
        self.configure(width=800, height=200, highlightbackground=globals.primary_colour, highlightthickness=1)
        self.grid_propagate(False)

        #labels dictionary for easy updating
        self.labels = {}

        stats = [
            "Files Processed",
            "Initial Total Size",
            "Final Total Size",
            "Compression (%)",
            "Encryption Password",
            "Status"
        ]

        for i, stat in enumerate(stats):
            label_name = tk.Label(self, text=stat + ":", anchor="w", bg=globals.secondary_colour, fg=globals.text_div_colour, width=20)
            label_value = tk.Label(self, text="", anchor="w", bg=globals.bg_colour, fg=globals.text_high_contrast)
            label_name.grid(row=i, column=0, padx=10, pady=2, sticky="w")
            label_value.grid(row=i, column=1, padx=10, pady=2, sticky="w")
            self.labels[stat] = label_value

    def update_stats(self, initial_size: int, final_size: int, password: str, num_files: int, success: bool):
        self.labels["Files Processed"].config(text=str(num_files))
        self.labels["Initial Total Size"].config(text=human_readable_size(initial_size))
        self.labels["Final Total Size"].config(text=human_readable_size(final_size))
        if initial_size > 0:
            compression = 100 - (final_size / initial_size * 100)
            self.labels["Compression (%)"].config(text=f"{compression:.2f}%")
        else:
            self.labels["Compression (%)"].config(text="0%")
        self.labels["Encryption Password"].config(text=password)
        self.labels["Status"].config(text="Success" if success else "Failed")
