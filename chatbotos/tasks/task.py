from chatbotos.tokenizers import SplitTokenizer
from dataclasses import dataclass
from abc import abstractmethod
from nltk import pos_tag
import random


class Task:
  @dataclass
  class EntryInfo:
    field: str | None = None
    mandatory: bool = True
    acceptance_responses: tuple = ()
    rejection_responses: tuple = ()
    questions: tuple = ()
    matches: str | None = None

  @staticmethod
  def reply(rep):
    print("[\033[38;2;255;215;0mEVE\033[0m] : " + rep)

  @abstractmethod
  def build(self) -> str: ...

  def set_field(self, fieldname, value):
    def is_truthy(ans) -> bool: return ans == 'yes'

    val = self.collectors[fieldname](value)
    response = random.choice(self[fieldname].acceptance_responses)
    
    confirms = (
      "I will use \"{}\" right? ",
      "Can we consider using \"{}\"? ",
      "Is \"{}\" the final answer? "
    )
    
    self.reply(response + ". " + random.choice(confirms).format(val))

    prompt = input(">> ")

    if is_truthy(prompt):
      self[fieldname].field = val
      response = random.choice(self[fieldname].acceptance_responses)
    else: 
      response = random.choice(self[fieldname].rejection_responses)

    self.reply(response)

  def fill(self, prompt: str):
    def mapper(pair): 
      return pair[0]
    
    sentence = SplitTokenizer.tokenize(prompt)
    tagged_sentence = pos_tag(sentence, tagset = 'universal')

    inputs = {
      fieldname : list(map(mapper, filter(predicate, tagged_sentence))) 
      for (fieldname, predicate) in self.predicates.items()
    }

    for fieldname, values in inputs.items():
      if len(values) == 1:
        self.set_field(fieldname, values[0])

    while len([1 for (_, v) in self.frame.items() if v.mandatory and v.field == None]) > 0:
      # Check for fields yet to fill
      to_fill = [fieldname for (fieldname, entry) in self.frame.items() if entry.mandatory and entry.field == None]

      # Select one random question
      response = random.choice(self[to_fill[0]].questions)

      # Reply to the user
      Task.reply(response)

      # Get user input
      prompt = input(">> ")

      # Transform the prompt
      sentence = SplitTokenizer.tokenize(prompt)
      tagged_sentence = pos_tag(sentence, tagset = 'universal')

      # Extract values from the prompt based on the predicates
      inputs = {
        fieldname : list(map(mapper, filter(predicate, tagged_sentence))) 
        for (fieldname, predicate) in self.predicates.items()
      }

      # # Set the values for each fieldname
      for (fieldname, values) in inputs.items():
        if len(values) == 1 and self[fieldname].field == None:
          self.set_field(fieldname, values[0])

  def __init__(self, labels: list[str] = [], predicates: list = [], collectors: list = []):
    self.frame: dict[str, Task.EntryInfo] = dict.fromkeys(labels)
    self.predicates = { fieldname : predicate for (fieldname, predicate) in zip(labels, predicates) }
    self.collectors = { fieldname : collector for (fieldname, collector) in zip(labels, collectors) }

    for label in self.frame.keys():
      self.frame[label] = Task.EntryInfo()

  def __setitem__(self, label: str, task: EntryInfo) -> None:
    self.frame[label] = task

  def __getitem__(self, label: str) -> "Task.EntryInfo":
    return self.frame[label]
  
  def __str__(self) -> str:
    return f"""  """

  def __repr__(self):
    return self.__str__()
