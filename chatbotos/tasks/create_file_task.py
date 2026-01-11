from chatbotos.tasks.task import Task
import re
import os

class CreateFileTask(Task):
  def __init__(self):
    super().__init__(
      ['file name', 'extension', 'directory'], 
      [
        lambda pair: pair[1] == 'NOUN' and re.match(self['file name'].matches, pair[0]),
        lambda pair: pair[1] == 'NOUN' and re.match(self['extension'].matches, pair[0]),
        lambda pair: os.path.isdir(pair[0])
      ],
      [
        lambda value: value[ : value.rfind('.') ],
        lambda value: value[value.rfind('.') + 1 : ],
        lambda value: value
      ]
    )

    self['file name'] = Task.EntryInfo(
      acceptance_responses = (
        "letzgoski",
      ),
      rejection_responses = (
        "i didn't understand the file name, rewrite it.",
        "write the file name please"
      ),
      questions = (
        "which file do you want to create?",
        "can you give a file name?",
        "can you specify what file name?",
        "can you give one file name?"
      ),
      matches = r"[a-zA-Z0-9_]*((\.[a-zA-Z0-9_])+)",
      mandatory = True
    )
    self['extension'] = Task.EntryInfo(
      acceptance_responses = (
        "letzgoski",
      ),
      questions = (
        "i didn't understand the extension, can you specify one?",
        "can you specify an extension?"
      ),
      rejection_responses = (
        "i didn't understand the file extension, rewrite it.",
        "write the file extension please"
      ),
      matches = r"[a-zA-Z0-9_]*((\.[a-zA-Z0-9_])+)",
      mandatory = True
    )
    self['directory'] = Task.EntryInfo(
      acceptance_responses = (
        "letzgoski",
      ),
      rejection_responses = (
        "i didn't understand the directory, rewrite it.",
        "write the directory please"
      ),
      questions = (
        "i didn't understand the directory, do you want to specify one?",
        "can you give a directory name?"
      ),
      mandatory = True
    )

  def build(self) -> str:
    return "echo > {}\\{}.{}".format(
      self['directory'].field, 
      self['file name'].field, 
      self['extension'].field
    )

  def execute(self):
    path = self['directory'].field + '\\' + self['file name'].field + '.' + self['extension'].field
    if os.path.exists(path) and os.path.isfile(path):
      Task.error("File already exists")
    else:
      with open(path, 'w') as file: pass
