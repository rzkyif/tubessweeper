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

    self.found_bombs = 0
    self.informed = set()

    self.map = [[0 for y in range(n)] for x in range(n)]
    self.init_internal_map()

    self.log_function = functions[0]
    self.agenda_function = functions[1]
    self.facts_function = functions[2]
    self.print_function = functions[3]
    self.map_function = functions[4]

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
      self.map[x][y] = 6
      # update sekitar bom
      for h in range(-1, 2):
        for v in range(-1, 2):
          xx = x+h
          yy = y+v
          if (h == 0 and v == 0) or (xx < 0 or xx >= self.n or yy < 0 or yy >= self.n):
            continue
          if (self.map[xx][yy] < 4):
            self.map[xx][yy] += 1


  # load file clips awal (tubessweeper.clp)
  def init_clips(self):
    # fungsi dari python
    self.env.define_function(self.print, name="python_print")
    self.env.define_function(self.mark, name="python_mark")
    self.env.define_function(self.probe, name="python_probe")
    self.env.define_function(self.nextto, name="python_is_next_to")
    # load clp
    self.env.batch_star(os.path.join(os.getcwd(), 'clips', CLIPS_FILE))
    self.env.reset()

    for rule in self.env._agenda.rules():
      print(rule.name)
    # asersi kondisi awal
    for x in range(self.n):
      for y in range(self.n):
        self.env.eval('(assert (tile (location x%dy%d)))' % (x, y))
    # refresh
    self.refresh()


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


  # kirim agenda, fakta, dan peta ke UI
  def refresh(self):
    self.agenda_function([re.sub(r'^[0123456789]+ *', '', str(activation)).replace(': ', ':\n') for activation in self.env._agenda.activations()])
    self.facts_function(['f-' + str(fact.index) + ": " + re.sub(r'^f-[0123456789]+ *', '', str(fact)) for fact in self.env._facts.facts()])
    current_map = [[-1 for y in range(self.n)] for x in range(self.n)]
    for fact in self.env._facts.facts():
      if fact.template.name == "tile":
        x, y = self.l_to_c(fact['location'])
        current_map[x][y] = fact['status']
    self.map_function(current_map)


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

    self.env._agenda.refresh()

    if (refresh):
      self.refresh()

    return self.can_run()


  # run program clips sampai selesai
  def run(self):
    while (self.can_run()):
      self.step()
    self.refresh()
    

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

  
  # fungsi mark suatu koordinat dari CLIPS
  def mark(self, location):
    x, y = self.l_to_c(location)
    if self.map[x][y] == 6:
      self.found_bombs += 1
      if self.found_bombs == self.b:
        print("Game Finished: Bot Won\nSending all non-bomb map info to KBS")
        for xx in range(self.n):
          for yy in range(self.n):
            if (xx != x) or (yy != y):
              if self.map[xx][yy] != 6:
                self.inform(xx, yy)
        self.env.eval('(assert (game-finished win))')
    return self.inform(x, y, 5)

  
  # fungsi coba klik suatu koordinat untuk ekspansi dari CLIPS
  def probe(self, location):
    x, y = self.l_to_c(location)
    if (self.map[x][y] != 0):
      if self.map[x][y] == 6:
        print("Game Finished: Bot Lost\nSending all map info to KBS")
        for xx in range(self.n):
          for yy in range(self.n):
            if (xx != x) or (yy != y):
              self.inform(xx, yy)
        self.env.eval('(assert (game-finished lose))')
      result = self.inform(x, y)
    else:
      self.inform_expansion(x,y,set())
      result = self.find_facts('tile', {'location': location})[0]
    return result
  

  # fungsi cek apakah dua lokasi bersebelahan
  def nextto(self, location1, location2):
    if location1 == location2:
      return False
    x1, y1 = self.l_to_c(location1)
    x2, y2 = self.l_to_c(location2)
    result = ((abs(x2-x1) <= 1) and (abs(y2-y1) <= 1))
    return result
    

  #
  #  fungsi-fungsi pembantu
  #


  # kirimkan informasi mengenai petak x, y dan petak sekitarnya ke KBS
  def inform_expansion(self, x, y, blacklist):
    if((x,y) in blacklist):
      return
    else:
      self.inform(x, y)
      for h in range(-1, 2):
        for v in range(-1, 2):
          xx = x+h
          yy = y+v
          if (h == 0 and v == 0) or (xx < 0 or xx >= self.n or yy < 0 or yy >= self.n):
            continue
          if self.map[xx][yy] != 0:
            self.inform(xx,yy)
          elif (xx,yy) not in blacklist:
            blacklist.add((x, y))
            self.inform_expansion(xx, yy, blacklist)

  
  # kirimkan informasi mengenai petak x, y ke KBS. kembalikan fakta baru
  def inform(self, x, y, status=None):
    if((x,y) not in self.informed):
      print('Informing about (%d, %d) to KBS' % (x, y))
      location = self.c_to_l(x, y)
      fact = self.find_facts('tile', {'location': location})[0]
      new_fact = self.copy_tile(fact)
      if status is None:
        new_fact['status'] = self.map[x][y]
        self.informed.add((x,y))
      else:
        new_fact['status'] = status
      fact.retract()
      new_fact.assertit()
      return new_fact


  # cari fakta
  def find_facts(self, type, properties):
    result = []
    for fact in self.env._facts.facts():
      if fact.template.name == type:
        same = True
        for key in properties.keys():
          if fact[key] != properties[key]:
            same = False
        if same:
          result.append(fact)
    return result

  
  # duplikat fakta
  def copy_tile(self, tile):
      new_fact = tile.template.new_fact()
      new_fact['location'] = tile['location']
      new_fact['status'] = tile['status']
      new_fact['iteration'] = tile['iteration']
      return new_fact

  
  # location to coordinates
  def l_to_c(self, location):
    split = location.split('y')
    x = int(split[0].strip('x'))
    y = int(split[1])
    return x, y

  
  # coordinates to location
  def c_to_l(self, x, y):
    return 'x'+str(x)+'y'+str(y)