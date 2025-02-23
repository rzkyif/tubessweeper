import sys

from gui.main_window import MainWindow
from PyQt5.QtWidgets import QApplication
from src.input import get_input_from_console, get_input_from_gui, get_input_from_file

if __name__ == '__main__':
  app = QApplication(sys.argv)

  # deklarasi
  n, b, bc = None, None, None

  # mode input awal: 0 = gui (DEFAULT), 1 = console, 2 = file
  mode = 0
  if (len(sys.argv) > 1):
    if (sys.argv[1] in ['-ng', '--no-gui']):
      mode = 1
    elif (len(sys.argv) > 2 and sys.argv[1] in ['-f', '--file']):
      mode = 2
  
  if (mode == 0):
    # input dari gui
    try:
      n, b, bc = get_input_from_gui()
    except:
      pass
  elif (mode == 1):
    # input dari console
    try:
      n, b, bc = get_input_from_console()
    except:
      pass
  elif (mode == 2):
    # input dari file
    try:
      n, b, bc = get_input_from_file(sys.argv[2].strip('"').strip())
    except:
      pass

  # syarat: n, b, dan bc valid
  if n is None or b is None or bc is None or b >= (n*n) or (0,0) in bc:
    print('Input tidak valid!')
    sys.exit(0)

  # syarat: maks bom disekitar satu titik 4
  map = [[0 for y in range(n)] for x in range(n)]
  for x, y in bc:
    map[x][y] = 6
    # update sekitar bom
    for h in range(-1, 2):
      for v in range(-1, 2):
        xx = x+h
        yy = y+v
        if (h == 0 and v == 0) or (xx < 0 or xx >= n or yy < 0 or yy >= n):
          continue
        if (map[xx][yy] <= 4):
          map[xx][yy] += 1
          if map[xx][yy] == 5:
            print('Input tidak valid!')
            sys.exit(0)

  
  print("N:", n)
  print("B:", b)
  print("BC:", bc)

  # mulai app
  main_window = MainWindow(n, b, bc)
  main_window.show()
  sys.exit(app.exec_())
