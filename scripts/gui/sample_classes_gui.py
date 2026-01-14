import tkinter as tk
from tkinter import ttk #themed tkinter

def main() -> None:
    app = Application()
    app.mainloop()

class Application(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        #configuring the page
        self.title("LockBox")
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        self.rowconfigure(0, weight = 1)
        
        #defining frames found in this page
        frame = input_form(self)
        frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        frame2 = input_form(self)
        frame2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)


#defining an input form frame
class input_form(ttk.Frame):

    def __init__(self, parent: Application) -> None:
        super().__init__(parent)

        #configuring this frame
        self.columnconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        
        #entry field
        self.entry = ttk.Entry(self)
        self.entry.grid(row=0,column=0, sticky ="ew")
        self.entry.bind("<Return>", self.submit)

        #button
        self.submit_btn = ttk.Button(self, text="Submit",command=self.submit)
        self.submit_btn.grid(row=0,column=1)

        #text list
        self.text_list = tk.Listbox(self)
        self.text_list.grid(row=1,column=0, columnspan=2, sticky="nsew") #cardinal directions east and west

    #function for what happens when submit button pressed
    def submit(self, event=None):
        text = self.entry.get()
        if text:
            self.text_list.insert(tk.END, text)
            self.entry.delete(0,tk.END)


if __name__ == "__main__":
    main()