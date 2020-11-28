import sys

from PyQt5.QtWidgets import QApplication
from src.input import get_input_from_console, get_input_from_gui
from src.app import App

if __name__ == '__main__':
  app = QApplication(sys.argv)

  # deklarasi
  n, b, bc = None, None, None
  gui = not (len(sys.argv) > 1 and (sys.argv[1] in ['--no-gui', '-ng']))
  
  if (gui):
    # input dari gui
    try:
      n, b, bc = get_input_from_gui()
    except:
      pass
  else:
    # input dari console
    try:
      n, b, bc = get_input_from_console()
    except:
      pass

  # syarat: n, b, dan bc valid
  if n is None or b is None or bc is None or bc >= (n*n) or (0,0) in bc:
    sys.exit(0)
  
  print("N:", n)
  print("B:", b)
  print("BC:", bc)

  # mulai app
  app = App(n, b, bc, gui)
  app.run()
