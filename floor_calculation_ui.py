import tkinter as tk
from tkinter import ttk, END
from tkinter.messagebox import showerror, showinfo

import pandas as pd
import numpy as np

perimeter_unit = ('m', 'cm')
area_unit = ('m^2', 'cm^2')
thickness_unit = ('mm', 'cm', 'dm', 'm')

df_data = pd.read_csv('floor_u_table.csv', header=None, sep=',', dtype='float')
x = np.array(df_data.iloc[0, :])
y = np.array(df_data.iloc[:, 0])
z = np.array(df_data.iloc[:, :])


def double_linear_interpolation(x, y, z, inputx, inputy):
  i, j = 1, 1
  while inputy > y[j]:
    j += 1
  while inputx > x[i]:
    i += 1
  i-=1
  j-=1
  z00, z01, z10, z11 = z[j][i], z[j + 1][i], z[j][i + 1], z[j + 1][i + 1]
  ztop = (x[i + 1] - inputx) / (x[i + 1] - x[i]) * z00 + (inputx - x[i]) / (x[i + 1] - x[i]) * z10
  zbottom = (x[i + 1] - inputx) / (x[i + 1] - x[i]) * z01 + (inputx - x[i]) / (x[i + 1] - x[i]) * z11
  ztotal = (y[j + 1] - inputy) / (y[j + 1] - y[j]) * ztop + (inputy - y[j]) / (y[j + 1] - y[j]) * zbottom
  return round(ztotal,4)


def is_numeric(s):
  s = s.strip()
  try:
    s = float(s)
    return True
  except:
    return False


def get_floor_ui_frame(_root):
  def cal_u():
    p = i_p.get()
    a = i_a.get()
    pu = p_unit.get()
    au = a_unit.get()
    ln = i_name.get()
    t = i_thickness.get()
    tu = i_thickness_unit.get()
    k = i_k.get()
    if len(p.strip()) == 0:
      showerror(message='You should enter the perimeter of the floor')
      return
    elif not is_numeric(p):
      showerror(message='Perimeter should be numeric')
      return
    p = float(p)
    if len(a.strip()) == 0:
      showerror(message='You should enter the area of the floor')
      return
    elif not is_numeric(a):
      showerror(message='Area should be numeric')
      return
    a = float(a)

    if len(t.strip()) == 0:
      showerror(message='You should enter the thickness of the insulation layer')
      return
    elif not is_numeric(t):
      showerror(message='Thickness of the insulation layer should be numeric')
      return
    t = float(t)
    if len(k.strip()) == 0:
      showerror(message='You should enter the thermal conductivity of the insulation layer')
      return
    elif not is_numeric(k):
      showerror(message='Thermal Conductivity of the insulation layer should be numeric')
      return
    k = float(k)
    if pu == 'm':
      p = p * 1
    elif pu == 'cm':
      p = p * 0.01
    else:
      showerror('Undefined perimeter unit')
      return
    if au == 'm^2':
      a = a * 1
    elif au == 'cm^2':
      a = a * 0.0001
    else:
      showerror(message='Undefined Area unit')
      return
    if tu == 'mm':
      t = t * 0.001
    elif tu == 'cm':
      t = t * 0.01
    elif tu == 'dm':
      t = t * 0.1
    elif tu == 'm':
      t = t * 1
    else:
      showerror(message='Undefined Thickness unit')
      return
    par = p / a
    r = t / k
    u = find_u(par, r)
    i_result.delete(0, END)
    i_result.insert(0, u)

  def find_u(par, r):
    u = double_linear_interpolation(x, y, z, r, par)
    return u

  root = ttk.Frame(_root)

  label_title = tk.Label(root, text='Floor Structure U-value calculation', font=('Times', 16, 'bold'))
  l_p = tk.Label(root, text='Floor Structure Perimeter :')
  l_a = tk.Label(root, text='Floor Structure Area         :')
  i_p = ttk.Entry(root, width=15)
  i_a = ttk.Entry(root, width=15)
  p_unit = ttk.Combobox(root, width=10, state='readonly')
  p_unit['values'] = perimeter_unit
  a_unit = ttk.Combobox(root, width=10, state='readonly')
  a_unit['values'] = area_unit
  p_unit.current(0)
  a_unit.current(0)
  l_name = tk.Label(root, text='Insulation Layer Name(Optional): ')
  i_name = tk.Entry(root, width=15)
  l_thickness = tk.Label(root, text='Insulation Layer Thickness:')
  i_thickness = tk.Entry(root, width=15)
  i_thickness_unit = ttk.Combobox(root, width=10, state='readonly')
  i_thickness_unit['values'] = thickness_unit
  i_thickness_unit.current(0)
  l_k = tk.Label(root, text='Insulation Layer Thermal Conductivity:')
  i_k = tk.Entry(root, width=15)
  btn_cal = tk.Button(root, text='Calculate', fg='red', command=cal_u, width=10)
  i_result = tk.Entry(root, width=15)
  l_result = tk.Label(root, text='U-value of floor structure:')

  label_title.grid(row=1, column=1, columnspan=3)
  l_p.grid(row=2, column=1, sticky='w')
  i_p.grid(row=2, column=2, sticky='w')
  p_unit.grid(row=2, column=3, sticky='w')
  l_a.grid(row=3, column=1, sticky='w')
  i_a.grid(row=3, column=2, sticky='w')
  a_unit.grid(row=3, column=3, sticky='w')
  l_name.grid(row=4, column=1, sticky='w')
  i_name.grid(row=4, column=2, sticky='w', columnspan=2)
  l_thickness.grid(row=5, column=1, sticky='w')
  i_thickness.grid(row=5, column=2, sticky='w')
  i_thickness_unit.grid(row=5, column=3, sticky='w')
  l_k.grid(row=6, column=1, sticky='w')
  i_k.grid(row=6, column=2, sticky='w')
  btn_cal.grid(row=7, column=3, sticky='w')
  i_result.grid(row=7, column=2, sticky='w')
  l_result.grid(row=7, column=1, sticky='w')
  print('floor calculation ui init ok')

  return root
