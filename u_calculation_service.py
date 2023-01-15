def cal_wall_u(rsi, rso, materials):
  r_total = rsi + rso
  for m in materials:
    r_total += m[1] / m[2]
  return round(1 / r_total, 4)
