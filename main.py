import tkinter as tk
from tkinter.messagebox import *
from tkinter import *
import pandas as pd
from tkinter import ttk

material_k_dic = {}
df = pd.read_csv('k.csv', delimiter=',')

for index, row in df.iterrows():
  x, y = row['material_name'], row['material_thermal_conductivity']
  material_k_dic[x] = y


def is_numeric(s):
  s = s.strip()
  try:
    s = float(s)
    return True
  except:
    return False


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

  item = m_name + "/" + str(m_thickness) + "/" + str(m_k)
  list_material.insert(list_material.size(), item)


def material_remove():
  i_item = list_material.curselection()
  if len(i_item) == 0:
    return
  list_material.delete(i_item)


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
  showinfo(title='calculating', message='rsi=' + str(rsi) + ', rso=' + str(rso) + ', materials=' + str(materials))


root = tk.Tk()

root.title("Comprehensive U-value calculator")
root.geometry('850x400')
root.resizable(0, 0)

text_title = tk.Label(root, text="Wall-Structure Value Calculate", fg="black", font=('Times', 20, 'bold'))
label_rso = tk.Label(root, text="Outside Surface Thermal Resistance (in m^2k/W): ")
label_rsi = tk.Label(root, text="Inside Surface Thermal Resistance (in m^2k/W): ")
label_material_list = tk.Label(root, text="Name / Thickness (in meter) / Conductivity (in W/mk)",
                               font=("Times", 16, "bold"))
input_rso = tk.Entry(root, width=20)
input_rsi = tk.Entry(root, width=20)
input_m_name = ttk.Combobox(root, width=15)
input_m_name["values"] = list(material_k_dic.keys())
input_m_name.bind("<<ComboboxSelected>>", select_m_name)

input_m_thickness_unit = ttk.Combobox(root, width=10, state="readonly")
input_m_thickness_unit["values"] = ("mm", "cm", "dm", "m")
input_m_thickness_unit.current(3)

input_m_thickness = tk.Entry(root, width=18)
input_m_k = tk.Entry(root, width=18)
label_m_name = tk.Label(root, text="Material Name:")

label_m_thickness = tk.Label(root, text="Thickness: ")
label_m_k = tk.Label(root, text="Conductivity: ")
label_m_k_unit = tk.Label(root, text='W/mk')

btn_add = tk.Button(root, text="Add New Material", command=material_add)
btn_remove = tk.Button(root, text="Remove Selected Material", command=material_remove)

list_material = tk.Listbox(root)
btn_quit = tk.Button(root, text="Quit", command=root.quit, width=10)
btn_cal = tk.Button(root, text="Calculate U-value", fg="Red", width=15, command=cal_u)

text_title.grid(row=1, column=1)

label_rso.grid(row=2, column=1)
input_rso.grid(row=2, column=2)

label_rsi.grid(row=3, column=1)
input_rsi.grid(row=3, column=2)

label_material_list.grid(row=4, column=1)

list_material.grid(row=5, column=1, rowspan=4, sticky='we')
label_m_name.grid(row=5, column=2, sticky='e')
input_m_name.grid(row=5, column=3, sticky='w')
label_m_thickness.grid(row=6, column=2, sticky='e')
input_m_thickness.grid(row=6, column=3, sticky='w')
input_m_thickness_unit.grid(row=6, column=4, sticky='w')
label_m_k.grid(row=7, column=2, sticky='e')
input_m_k.grid(row=7, column=3, sticky='w')
label_m_k_unit.grid(row=7, column=4, sticky='w')
btn_add.grid(row=8, column=2, )
btn_remove.grid(row=8, column=3, )
btn_cal.grid(row=10, column=1, sticky='we')
btn_quit.grid(row=10, column=2, sticky='we', columnspan=3)

root.mainloop()
