from chatbotos.tokenizers import SplitTokenizer
from dataclasses import dataclass
from abc import abstractmethod
import os
from nltk import pos_tag
import re

class Task:
  @dataclass
  class EntryInfo:
    field: str = ""
    acceptance_responses: tuple = ()
    rejection_responses: tuple = ()
    questions: tuple = ()
    matches: str | None = None

  @abstractmethod
  def build(self) -> str: ...

  @abstractmethod
  def fill(self) -> None: ...

  def __init__(self, labels: list[str] = []):
    self.frame: dict[str, Task.EntryInfo] = dict.fromkeys(labels)

    for label in self.frame.keys():
      self.frame[label] = Task.EntryInfo()

  def __getitem__(self, label: str) -> "Task.EntryInfo":
    return self.frame[label]
  
  def __str__(self) -> str:
    return f"""  """

  def __repr__(self):
    return self.__str__()

class CreateFileTask(Task):
  def __init__(self):
    super().__init__(['filename', 'directory', 'extension'])
    self['filename'].matches = r"[a-zA-Z0-9]*\.([a-zA-Z0-9]+)"

  def fill(self, prompt: str):
    sentence = SplitTokenizer.tokenize(prompt)
    tagged_sentence = pos_tag(sentence, tagset = 'universal')
    nouns = [
      noun 
      for (noun, tag) in tagged_sentence 
      if tag == 'NOUN' and re.match(self['filename'].matches, noun)
    ]
    if len(nouns) == 0: 
      # re-ask the filename (possibly missing)
      pass
    elif len(nouns) == 1:
      print(nouns[0])
      s = nouns[0].split('.')
      self['filename'].field = s[0]
      self['extension'].field = s[1]
    else:
      # solve ambiguity
      pass
    

  def build(self) -> str:
    return "echo > {}/{}.{}".format(
      self['directory'].field, 
      self['filename'].field, 
      self['extension'].field
    )


TASKS: dict[str, type[Task]] = {
  'CREATE_FILE': CreateFileTask, 
  # 'REMOVE_DIR': RemoveDirTask, 
  # 'SHOW_FILE': ShowFileTask, 
  # 'CREATE_DIR': CreateDirTask, 
  # 'REMOVE_FILE': RemoveFileTask, 
  # 'MOVE': MoveTask, 
  # 'RENAME': RenameTask, 
  # 'SHOW_DIR': ShowDirTask, 
  # 'CHANGE_DIR': ChangeDirTask, 
  # 'COPY': CopyTask,
}