import os;

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog

# dialog untuk input pengaturan awal
class InputDialog(QDialog):
  def __init__(self, result=""):
    super().__init__()
    loadUi(os.path.join(os.getcwd(), 'gui', 'input_dialog.ui'), self)

    self.result = result

    self.connect_ui()


  # konek UI ke kode
  def connect_ui(self):
    self.nSpinBox.valueChanged.connect(self.on_n_changed)
    self.buttonBox.accepted.connect(self.on_accept)
    self.buttonBox.rejected.connect(self.on_reject)
  

  # ketika Ok dipencet
  def on_accept(self):
    self.result[0] = self.nSpinBox.value()
    self.result[1] = self.bSpinBox.value()
    self.result[2] = []
    for coordinate in self.bcPlainTextEdit.toPlainText().split(';'):
      try:
        parts = coordinate.split(',')
        self.result[2].append((int(parts[0].strip()), int(parts[1].strip())))
      except:
        pass
    self.accept()


  # ketika Cancel dipencet
  def on_reject(self):
    self.reject()
  
  
  # ketika n berubah, jumlah bom maksimal jadi (n*n)-1 karena gaboleh bom 0,0
  def on_n_changed(self, n):
    self.bSpinBox.setMaximum((n*n)-1)

  
