import os;

from src.ai import AI
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow

# dialog untuk input pengaturan awal
class MainWindow(QMainWindow):
  def __init__(self, n, b, bc):
    super().__init__()
    loadUi(os.path.join(os.getcwd(), 'gui', 'main_window.ui'), self)

    self.n = n
    self.b = b
    self.bc = bc
    self.ai = AI(n, b, bc, [self.log_function, self.agenda_function, self.facts_function])

    self.connect_ui()
  

  # fungsi yg dipanggil AI untuk nulis log
  def log_function(self, string):
    self.logListWidget.addItem("[Iteration "+str(self.ai.iteration)+"]\n"+string)
  
  
  # fungsi yg dipanggil AI untuk cetak agenda (daftar aktivasi)
  def agenda_function(self, activations):
    self.agendaListWidget.clear()
    for activation in activations:
      self.agendaListWidget.addItem(activation)
  

  # fungsi yg dipanggil AI untuk cetak daftar fact
  def facts_function(self, facts):
    self.factListWidget.clear()
    for fact in facts:
      self.factListWidget.addItem(fact)


  # konek UI ke kode
  def connect_ui(self):
    self.stepButton.clicked.connect(self.on_step_clicked)
    self.runButton.clicked.connect(self.on_run_clicked)


  # ketika "Lakukan 1 Iterasi" dipencet
  def on_step_clicked(self):
    self.ai.step(True)


  # ketika "Selesaikan" dipencet
  def on_run_clicked(self):
    self.ai.run()


  
