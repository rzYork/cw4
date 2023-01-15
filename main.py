import tkinter
import tkinter as tk

from tkinter.ttk import Separator

from wall_calculation_ui import *
from floor_calculation_ui import *

root = tk.Tk()
notebook = tkinter.ttk.Notebook(root)
wall_frame = tkinter.Frame(notebook)
floor_frame = tkinter.Frame(notebook)
root.title("Comprehensive U-value calculator")
root.geometry('850x400')
root.resizable(0, 0)

notebook.add(get_wall_ui_frame(notebook), text='Wall Structure U-value calculation')
notebook.add(get_floor_ui_frame(notebook), text='Floor Structure U-value calculation')
notebook.pack(padx=10, pady=5, fill=tkinter.BOTH, expand=True)

root.mainloop()
