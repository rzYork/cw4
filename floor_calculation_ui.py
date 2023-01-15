import tkinter as tk
from tkinter import ttk


def get_floor_ui_frame(_root):
  floor_frame = ttk.Frame(_root)

  label_title = tk.Label(floor_frame, text='Floor Structure U-value calculation', font=('Times', 16, 'bold'))

  label_title.grid(row=1, column=1)

  print('floor calculation ui init ok')

  return floor_frame
