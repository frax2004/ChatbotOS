from chatbotos.tokenizers import SplitTokenizer
from dataclasses import dataclass
from abc import abstractmethod
from nltk import pos_tag
import re
import random
import os


class Task:
  @dataclass
  class EntryInfo:
    field: str | None = None
    mandatory: bool = True
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

  def __setitem__(self, label: str, task: EntryInfo) -> None:
    self.frame[label] = task

  def __getitem__(self, label: str) -> "Task.EntryInfo":
    return self.frame[label]
  
  def __str__(self) -> str:
    return f"""  """

  def __repr__(self):
    return self.__str__()

class CreateFileTask(Task):
  def __init__(self):
    super().__init__(['filename', 'directory', 'extension'])
    self['filename'] = Task.EntryInfo(
      rejection_responses = (
        "[\033[38;2;255;215;0mEve\033[0m] : i didn't understand the file name, rewrite it.",
        "[\033[38;2;255;215;0mEve\033[0m] : write the file name please",
      ),
      questions = (
        "[\033[38;2;255;215;0mEve\033[0m] : which file do you want to create?",
        "[\033[38;2;255;215;0mEve\033[0m] : can you give a file name?",
        "[\033[38;2;255;215;0mEve\033[0m] : can you specify what file name?",
        "[\033[38;2;255;215;0mEve\033[0m] : can you give one file name?"
      ),
      matches = r"[a-zA-Z0-9_]*((\.[a-zA-Z0-9_])+)",
      mandatory = True
    )
    self['extension'] = Task.EntryInfo(
      questions = (
        "[\033[38;2;255;215;0mEve\033[0m] : i didn't understand the extension, can you specify one?",
        "[\033[38;2;255;215;0mEve\033[0m] : can you specify an extension?"
      ),
      matches = r"[a-zA-Z0-9_]*((\.[a-zA-Z0-9_])+)",
      mandatory = True
    )
    self['directory'] = Task.EntryInfo(
      questions = (
        "[\033[38;2;255;215;0mEve\033[0m] : i didn't understand the directory, do you want to specify one?",
        "[\033[38;2;255;215;0mEve\033[0m] : can you give a directory name?"
      ),
      mandatory = True
    )

  def fill(self, prompt: str):
    def mapper(pair): 
      return pair[0]
    
    def is_file(pair): 
      return pair[1] == 'NOUN' and re.match(self['filename'].matches, pair[0])

    def is_extension(pair): 
      return pair[1] == 'NOUN' and re.match(self['extension'].matches, pair[0])

    def is_directory(pair):
      return pair[1] == 'NOUN' and os.path.isdir(pair[0])

    sentence = SplitTokenizer.tokenize(prompt)
    tagged_sentence = pos_tag(sentence, tagset = 'universal')
    inputs = {
      'filename': list(map(mapper, filter(is_file, tagged_sentence))),
      'extension': list(map(mapper, filter(is_extension, tagged_sentence))),
      'directory': list(map(mapper, filter(is_directory, tagged_sentence)))
    }

    for fieldname, values in inputs.items():
      if len(values) == 1:
        self[fieldname].field = values[0]

    while len([1 for (_, v) in self.frame.items() if v.mandatory and v.field == None]) > 0:
      response = random.choice(self[[k for k, v in self.frame.items() if v.mandatory and v.field == None][0]].questions)
      prompt = input(response + "\n>> ")
      sentence = SplitTokenizer.tokenize(prompt)
      tagged_sentence = pos_tag(sentence, tagset = 'universal')
      inputs = {
        'filename': list(map(mapper, filter(is_file, tagged_sentence))),
        'extension': list(map(mapper, filter(is_extension, tagged_sentence))),
        'directory': list(map(mapper, filter(is_directory, tagged_sentence)))
      }

      values = inputs['filename']
      if len(values) == 1 and self['filename'].field == None:
        self['filename'].field = values[0][ : values[0].rfind('.')]

      values = inputs['extension']
      if len(values) == 1 and self['extension'].field == None:
        self['extension'].field = values[0][values[0].rfind('.')+1 : ]

      values = inputs['directory']
      if len(values) == 1 and self['directory'].field == None:
        self['directory'].field = values[0]

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