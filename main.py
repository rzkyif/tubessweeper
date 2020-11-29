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
    if (sys.argv[1] in ['-g', '--no-gui']):
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
    sys.exit(0)
  
  print("N:", n)
  print("B:", b)
  print("BC:", bc)

  # mulai app
  main_window = MainWindow(n, b, bc)
  main_window.show()
  sys.exit(app.exec_())
