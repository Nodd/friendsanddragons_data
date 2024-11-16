import tkinter as tk
from tkinter import ttk

from db import db


root = tk.Tk()
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

for row, hero in enumerate(db.heroes):
    tk.Label(root, text=hero.name).grid(row=row, column=0)

root.mainloop()
