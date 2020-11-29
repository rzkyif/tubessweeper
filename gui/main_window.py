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

    self.init_ai()
    self.connect_ui()


  #
  #  fungsi-fungsi umum
  #

  
  # inisialisasi AI
  def init_ai(self):
    self.ai = AI(self.n, self.b, self.bc, [self.log_function, self.agenda_function, self.facts_function, self.print_function])


  # konek UI ke kode
  def connect_ui(self):
    self.stepButton.clicked.connect(self.on_step_clicked)
    self.runButton.clicked.connect(self.on_run_clicked)
    self.restartButton.clicked.connect(self.on_restart_clicked)
    if (not self.ai.can_run()):
      self.stepButton.setDisabled(True)
      self.runButton.setDisabled(True)
  
  # refresh judul window
  def refresh_window_title(self):
    if (self.ai.iteration == 0):
      self.setWindowTitle("Kondisi Awal")
    else:
      self.setWindowTitle('Iterasi '+str(self.ai.iteration))


  #
  #  fungsi-fungsi yang dipanggil dari UI
  #


  # ketika "Lakukan 1 Iterasi" dipencet
  def on_step_clicked(self):
    self.ai.step(True)
    if (not self.ai.can_run()):
      self.stepButton.setDisabled(True)
      self.runButton.setDisabled(True)
    self.refresh_window_title()


  # ketika "Selesaikan" dipencet
  def on_run_clicked(self):
    self.ai.run()
    self.stepButton.setDisabled(True)
    self.runButton.setDisabled(True)
    self.refresh_window_title()

  
  # ketika "Restart" dipencet
  def on_restart_clicked(self):
    self.init_ai()
    self.logListWidget.clear()
    self.outputListWidget.clear()
    self.refresh_window_title()


  #
  #  fungsi-fungsi yang dipanggil dari AI
  #
  

  # fungsi yg dipanggil AI untuk nulis output
  def print_function(self, string):
    self.outputListWidget.addItem(string)
    self.outputListWidget.scrollToBottom()
  

  # fungsi yg dipanggil AI untuk nulis log
  def log_function(self, string):
    self.logListWidget.addItem("[Iteration "+str(self.ai.iteration)+"]\n"+string)
    self.logListWidget.scrollToBottom()
  

  # fungsi yg dipanggil AI untuk cetak daftar fact
  def facts_function(self, facts):
    self.factListWidget.clear()
    for fact in facts:
      self.factListWidget.addItem(fact)
  
  
  # fungsi yg dipanggil AI untuk cetak agenda (daftar aktivasi)
  def agenda_function(self, activations):
    self.agendaListWidget.clear()
    for activation in activations:
      self.agendaListWidget.addItem(activation)


  
