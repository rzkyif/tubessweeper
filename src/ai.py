import clips
import os
import re

class AI():
  def __init__(self, n, b, bc, functions):
    self.n = n
    self.b = b
    self.bc = bc

    self.log_function = functions[0]
    self.agenda_function = functions[1]
    self.facts_function = functions[2]

    self.iteration = 0
    self.env = clips.Environment()

    self.init_clips()


  # load file clips awal (tubessweeper.clp)
  def init_clips(self):
    self.env.batch_star(os.path.join(os.getcwd(), 'clips', 'tubessweeper.clp'))
    self.env.reset()
    self.refresh_agenda_and_facts()


  # kirim agenda dan fakta ke UI
  def refresh_agenda_and_facts(self):
    self.agenda_function([str(activation.name) for activation in self.env._agenda.activations()])
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
    self.iteration += 1

    self.generate_log()
    self.env._agenda.run(1)

    if (refresh):
      self.refresh_agenda_and_facts()

    try:
      next(self.env._agenda.activations())
    except StopIteration:
      return False

    return True


  # run program clips sampai selesai
  def run(self):
    return self.env._agenda.run()
  