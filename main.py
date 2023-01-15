import tkinter
import tkinter as tk

from tkinter.ttk import Separator

import floor_calculation_ui
import wall_calculation_ui
from wall_calculation_ui import *
from floor_calculation_ui import *
from tkinter import filedialog as fd


def open_k():
  filename = fd.askopenfilename(title='Open New Conductivity Table File',
                                filetypes=[('CSV Database', '*.csv'), ('All files', '*')], initialdir='./')
  if len(filename) == 0:
    return
  wall_calculation_ui.load_k_table(file_path=filename)

  return


def open_u():
  filename = fd.askopenfilename(title='Open New U-value Table File',
                                filetypes=[('CSV Database', '*.csv'), ('All files', '*')], initialdir='./')
  if len(filename) == 0:
    return
  floor_calculation_ui.load_u_table(file_path=filename)
  return


def root_quit():
  root.destroy()


root = tk.Tk()
notebook = tkinter.ttk.Notebook(root)
wall_frame = tkinter.Frame(notebook)
floor_frame = tkinter.Frame(notebook)
root.title("Comprehensive U-value calculator")
root.geometry('770x380')
root.resizable(0, 0)

notebook.add(get_wall_ui_frame(notebook), text='Wall Structure U-value calculation')
notebook.add(get_floor_ui_frame(notebook), text='Floor Structure U-value calculation')
notebook.pack(padx=10, pady=5, fill=tkinter.BOTH, expand=True)

mmenu = Menu(root)
fmenu = Menu(mmenu)
fmenu.add_command(label='Open another K-value table', command=open_k)
fmenu.add_command(label='Open another U solid ground floor table', command=open_u)
fmenu.add_separator()
fmenu.add_command(label='Exit', command=root_quit)
mmenu.add_cascade(label='File', menu=fmenu)

root['menu'] = mmenu

root.mainloop()
