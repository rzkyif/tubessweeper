import clips
import os
import re

CLIPS_FILE = 'tubessweeper.clp'
CLIPS_IGNORE_PRINT = ['crlf']

class AI():
  def __init__(self, n, b, bc, functions):
    self.n = n
    self.b = b
    self.bc = bc

    self.map = [[0 for y in range(n)] for x in range(n)]
    self.init_internal_map()

    self.log_function = functions[0]
    self.agenda_function = functions[1]
    self.facts_function = functions[2]
    self.print_function = functions[3]

    self.iteration = 0
    self.env = clips.Environment()

    self.init_clips()


  #
  #  fungsi-fungsi umum
  #


  # bikin peta yg ga diketahui clips
  def init_internal_map(self):
    # taro bom
    for x, y in self.bc:
      self.map[x][y] = 5
      # update sekitar bom
      for h in range(-1, 2):
        for v in range(-1, 2):
          xx = x+h
          yy = y+v
          if (h == 0 and v == 0) or (xx < 0 or xx >= self.n or yy < 0 or yy >= self.n):
            continue
          self.map[xx][yy] += 1


  # load file clips awal (tubessweeper.clp)
  def init_clips(self):
    # fungsi dari python
    self.env.define_function(self.print, name="python_print")
    self.env.define_function(self.info, name="python_info")
    self.env.define_function(self.probe, name="python_probe")
    self.env.define_function(self.nextto, name="python_is_next_to")
    # load clp
    self.env.batch_star(os.path.join(os.getcwd(), 'clips', CLIPS_FILE))
    self.env.reset()
    # asersi kondisi awal
    for x in range(self.n):
      for y in range(self.n):
        self.env.eval('(assert (tile (location x%dy%d)))' % (x, y))
    # refresh
    self.refresh_agenda_and_facts()


  # cek bisa run atau udah kelar
  def can_run(self):
    try:
      next(self.env._agenda.activations())
    except StopIteration:
      return False
    return True
    

  #
  #  fungsi-fungsi UI
  #


  # kirim agenda dan fakta ke UI
  def refresh_agenda_and_facts(self):
    self.agenda_function([re.sub(r'^[0123456789]+ *', '', str(activation)).replace(': ', ':\n') for activation in self.env._agenda.activations()])
    self.facts_function(['f-' + str(i) + ": " + re.sub(r'^f-[0123456789]+ *', '', str(fact)) for i, fact in enumerate(self.env._facts.facts())])


  # print rule paling tinggi di agenda + fact yg terkait
  def generate_log(self):
    activation = next(self.env._agenda.activations())
    rule = activation.name
    fact_strings = re.findall(r'f-[0123456789]+', str(activation))
    fact_indexes = [int(fact.replace('f-', '')) for fact in fact_strings]
    facts = []
    for fact in self.env._facts.facts():
      if fact.index in fact_indexes:
        facts.append((fact.index, fact))
    log = "[Rule]\n "
    log += rule
    if (len(facts) > 0):
      log += "\n[Facts]"
      for i, fact in facts:
        log += '\n f-' + str(i) + ': ' + re.sub(r'^f-[0123456789]+ *', '', str(fact))
    log += '\n'
    self.log_function(log)


  # run satu kali, return masih bisa run atau ngga
  def step(self, refresh = False):
    if (not self.can_run()):
      return

    self.iteration += 1

    self.generate_log()
    self.env._agenda.run(1)

    if (refresh):
      self.refresh_agenda_and_facts()

    return self.can_run()


  # run program clips sampai selesai
  def run(self):
    while (self.can_run()):
      self.step()
    self.refresh_agenda_and_facts()
    

  #
  #  fungsi-fungsi CLIPS
  #

  
  # fungsi print untuk CLIPS
  def print(self, *args):
    joined = ""
    for arg in args:
      string = str(arg)
      if string not in CLIPS_IGNORE_PRINT:
        joined += str(arg)
    self.print_function(joined)

  
  # fungsi cek info suatu koordinat untuk CLIPS
  def info(self, location):
    split = location.split('y')
    x = int(split[0].strip('x'))
    y = int(split[1])
    return self.map[x][y]

  
  # fungsi coba klik suatu koordinat untuk ekspansi dari CLIPS
  def probe(self, location):
    split = location.split('y')
    x = int(split[0].strip('x'))
    y = int(split[1])
    if (self.map[x][y] != 0):
      result = self.inform(x, y)
    else:
      self.inform_expansion(x,y,set())
      result = self.env.eval("(nth$ 1 (find-fact ((?tile tile)) (eq ?tile:location "+location+")))")
    return result
  

  # fungsi cek apakah dua lokasi bersebelahan
  def nextto(self, location1, location2):
    split = location1.split('y')
    x1 = int(split[0].strip('x'))
    y1 = int(split[1])
    split = location2.split('y')
    x2 = int(split[0].strip('x'))
    y2 = int(split[1])
    return (abs(x2-x1) <= 1) and (abs(y2-y1) <= 1)
    

  #
  #  fungsi-fungsi pembantu
  #


  # kirimkan informasi mengenai petak x, y dan petak sekitarnya ke KBS
  def inform_expansion(self, x, y, blacklist):
    self.inform(x, y)
    for h in range(-1, 2):
      for v in range(-1, 2):
        xx = x+h
        yy = y+v
        if (h == 0 and v == 0) or (xx < 0 or xx >= self.n or yy < 0 or yy >= self.n):
          continue
        if self.map[xx][yy] != 0:
          self.inform(xx,yy)
        else:
          nextlist = set(blacklist)
          nextlist.add((x, y))
          self.inform_expansion(xx, yy, nextlist)


  
  # kirimkan informasi mengenai petak x, y ke KBS. kembalikan fakta baru
  def inform(self, x, y):
    location = 'x'+str(x)+'y'+str(y)
    for f in self.env._facts.facts():
      pass
    return self.env.eval("(modify (nth$ 1 (find-fact ((?tile tile)) (eq ?tile:location "+location+"))) (status "+str(self.map[x][y])+"))")