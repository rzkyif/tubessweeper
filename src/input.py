from gui.input_dialog import InputDialog

# ambil masukan dari console
def get_input_from_console():
  # besar papan (format: "n")
  n = int(input("Masukkan besar papan (n): "))

  # banyak bom (format: "b")
  b = int(input("Masukkan banyak bom (b): "))

  # koordinat tiap bom (format: "x, y")
  bc = []
  for i in range(b):
    parts = input().split(',')
    bc.append((int(parts[0].strip()), int(parts[1].strip())))
  
  return n, b, bc

# ambil masukan lewat gui
def get_input_from_gui():
  result = [None, None, None]

  dialog = InputDialog(result)
  dialog.exec_()

  return result[0], result[1], result[2]

# ambil masukan dari file
def get_input_from_file(path):
  n, b, bc = None, None, None
  
  with open(path, 'r') as f:
    n = int(f.readline())
    b = int(f.readline())
    bc = []
    for i in range(b):
      parts = f.readline().split(',')
      bc.append((int(parts[0].strip()), int(parts[1].strip())))
      
  return n, b, bc