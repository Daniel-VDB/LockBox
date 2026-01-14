import tkinter as tk
from tkinter import ttk #themed tkinter

root = tk.Tk()
root.title("LockBox")

def submit(event=None)->None:
    text = entry.get()
    if text:
        text_list.insert(tk.END, text)
        entry.delete(0,tk.END)

root.columnconfigure(0,weight=1)
root.columnconfigure(1,weight=1)
root.rowconfigure(0,weight=1)

frame = ttk.Frame(root)
frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

frame.columnconfigure(0,weight=1)
frame.rowconfigure(1,weight=1)

entry = ttk.Entry(frame)
entry.grid(row=0,column=0, sticky ="ew")

entry.bind("<Return>", submit)

submit_btn = ttk.Button(frame,text="Submit",command=submit)
submit_btn.grid(row=0,column=1)

text_list = tk.Listbox(frame)
text_list.grid(row=1,column=0, columnspan=2, sticky="nsew") #cardinal directions east and west

#---

frame2 = tk.Frame(root)
frame2.grid(row=0, column=1, sticky="nsew")

frame2.columnconfigure(0,weight=1)
frame2.rowconfigure(1,weight=1)

entry2 = tk.Entry(frame2)
entry2.grid(row=0,column=0, sticky ="ew")

entry2.bind("<Return>", submit)

submit_btn2 = tk.Button(frame2,text="Submit",command=submit)
submit_btn2.grid(row=0,column=1)

text_list2 = tk.Listbox(frame2)
text_list2.grid(row=1,column=0, columnspan=2, sticky="nsew") #cardinal directions east and west

root.mainloop()