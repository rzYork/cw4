from tkinter import ttk
import tkinter as tk
from tkinter.ttk import Separator

import pandas as pd
from tkinter import ttk



from tkinter.messagebox import *
from tkinter import *


def is_numeric(s):
  s = s.strip()
  try:
    s = float(s)
    return True
  except:
    return False


def get_wall_ui_frame(_root):
  material_k_dic = {}
  df = pd.read_csv('k.csv', delimiter=',')

  for index, row in df.iterrows():
    x, y = row['material_name'], row['material_thermal_conductivity']
    material_k_dic[x] = y

  def select_m_name(e):
    input_m_k.delete(0, END)
    input_m_k.insert(0, material_k_dic.get(input_m_name.get()))

  def material_add():
    m_name = input_m_name.get()
    m_thickness = input_m_thickness.get()
    m_k = input_m_k.get()
    if len(m_name.strip()) == 0:
      showerror(message='Please enter the material name')
      return
    if m_name.find('/') != -1:
      showerror(message='Material name could not contain special characters backlash')
      return

    if len(m_thickness.strip()) == 0:
      showerror(message='Please enter the material thickness')
      return

    if not is_numeric(m_thickness):
      showerror(message='thickness should be digit!')
      return
    m_thickness = float(m_thickness)
    if len(m_k.strip()) == 0:
      showerror(message='Please enter the material thermal conductivity!')
      return
    if not is_numeric(m_k):
      showerror(message='thermal conductivity should be digit')
      return
    m_k = float(m_k)

    t_unit = input_m_thickness_unit.get();
    if t_unit == 'm':
      m_thickness = m_thickness
    elif t_unit == 'dm':
      m_thickness = m_thickness * 0.1
    elif t_unit == 'cm':
      m_thickness = m_thickness * 0.01
    elif t_unit == 'mm':
      m_thickness = m_thickness * 0.001
    else:
      showerror(message='Undefined Type of Unit')
      return
    m_thickness = round(m_thickness, 4)
    item = m_name + "/" + str(m_thickness) + "/" + str(m_k)
    list_material.insert(list_material.size(), item)

  def material_remove():
    i_item = list_material.curselection()
    if len(i_item) == 0:
      return
    list_material.delete(i_item)

  def cal_wall_u(rsi, rso, materials):
    r_total = rsi + rso
    for m in materials:
      r_total += m[1] / m[2]
    return round(1 / r_total, 4)

  def cal_u():
    rsi = input_rsi.get()
    rso = input_rso.get()
    if not is_numeric(rsi):
      showerror(message='Inside Surface Thermal Resistance Format Error')
      return
    if not is_numeric(rso):
      showerror(message='Outside Surface Thermal Resistance Format Error')
      return

    rsi = float(rsi)
    rso = float(rso)
    if list_material.size() < 1:
      showerror(message='You should add some wall-structure material')
      return
    materials = []
    for item in list_material.get(0, END):
      if len(item.strip()) == 0:
        continue
      sp = str.split(item, '/')
      materials.append(list((sp[0], float(sp[1]), float(sp[2]))))
    u = cal_wall_u(rsi, rso, materials)
    input_result.delete(0, END)
    input_result.insert(0, str(u))

  wall_frame = ttk.Frame(_root)
  text_title = tk.Label(wall_frame, text="Wall-Structure Value Calculate", fg="black", font=('Times', 20, 'bold'))
  label_rso = tk.Label(wall_frame, text="Outside Surface Thermal Resistance (in m^2k/W): ")
  label_rsi = tk.Label(wall_frame, text="Inside Surface Thermal Resistance (in m^2k/W): ")
  label_material_list = tk.Label(wall_frame, text="Name / Thickness (in meter) / Conductivity (in W/mk)",
                                 font=("Times", 12, "bold"))
  input_rso = tk.Entry(wall_frame, width=20)
  input_rsi = tk.Entry(wall_frame, width=20)
  input_m_name = ttk.Combobox(wall_frame, width=15)
  input_m_name["values"] = list(material_k_dic.keys())
  input_m_name.bind("<<ComboboxSelected>>", select_m_name)

  input_m_thickness_unit = ttk.Combobox(wall_frame, width=10, state="readonly")
  input_m_thickness_unit["values"] = ("mm", "cm", "dm", "m")
  input_m_thickness_unit.current(3)

  input_m_thickness = tk.Entry(wall_frame, width=18)
  input_m_k = tk.Entry(wall_frame, width=18)
  label_m_name = tk.Label(wall_frame, text="Material Name:")

  label_m_thickness = tk.Label(wall_frame, text="Thickness: ")
  label_m_k = tk.Label(wall_frame, text="Conductivity: ")
  label_m_k_unit = tk.Label(wall_frame, text='W/mk')

  btn_add = tk.Button(wall_frame, text="Add New Material", command=material_add)
  btn_remove = tk.Button(wall_frame, text="Remove Selected Material", command=material_remove)

  list_material = tk.Listbox(wall_frame)
  sep = Separator(wall_frame, orient=HORIZONTAL)
  sep2 = Separator(wall_frame, orient=HORIZONTAL)

  label_result = tk.Label(wall_frame, text="U-value: ", fg='red', font=('Times', 13, 'bold'))
  input_result = tk.Entry(wall_frame, state='normal', width=10)
  btn_quit = tk.Button(wall_frame, text="Quit", command=wall_frame.quit, width=10)
  btn_cal = tk.Button(wall_frame, text="Calculate U-value", fg="Red", width=15, command=cal_u)

  text_title.grid(row=1, column=1)

  label_rso.grid(row=2, column=1)
  input_rso.grid(row=2, column=2)

  label_rsi.grid(row=3, column=1)
  input_rsi.grid(row=3, column=2)

  label_material_list.grid(row=4, column=1)

  list_material.grid(row=5, column=1, rowspan=4, sticky='we')
  label_m_name.grid(row=5, column=2, sticky='e')
  input_m_name.grid(row=5, column=3, sticky='we')
  label_m_thickness.grid(row=6, column=2, sticky='e')
  input_m_thickness.grid(row=6, column=3, sticky='we')
  input_m_thickness_unit.grid(row=6, column=4, sticky='w')
  label_m_k.grid(row=7, column=2, sticky='e')
  input_m_k.grid(row=7, column=3, sticky='we')
  label_m_k_unit.grid(row=7, column=4, sticky='w')
  btn_add.grid(row=8, column=2, )
  btn_remove.grid(row=8, column=3, )

  sep.grid(row=9, column=1, columnspan=4, padx=100, pady=10)
  label_result.grid(row=10, column=1, sticky='e')
  input_result.grid(row=10, column=2, sticky='w')
  sep2.grid(row=11, column=1, columnspan=4, padx=100, pady=10)
  btn_cal.grid(row=12, column=1, sticky='we')
  btn_quit.grid(row=12, column=2, sticky='we', columnspan=3)

  print('wall_calculation_ui init ok')

  return wall_frame
