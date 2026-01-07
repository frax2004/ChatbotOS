from chatbotos.tasks.task import Task
import re
import os

class CreateFileTask(Task):
  def __init__(self):
    super().__init__(
      ['filename', 'extension', 'directory'], 
      [
        lambda pair: pair[1] == 'NOUN' and re.match(self['filename'].matches, pair[0]),
        lambda pair: pair[1] == 'NOUN' and re.match(self['extension'].matches, pair[0]),
        lambda pair: os.path.isdir(pair[0])
      ],
      [
        lambda value: value[ : value.rfind('.') ],
        lambda value: value[value.rfind('.') + 1 : ],
        lambda value: value
      ]
    )

    self['filename'] = Task.EntryInfo(
      rejection_responses = (
        "i didn't understand the file name, rewrite it.",
        "write the file name please",
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
      questions = (
        "i didn't understand the extension, can you specify one?",
        "can you specify an extension?"
      ),
      matches = r"[a-zA-Z0-9_]*((\.[a-zA-Z0-9_])+)",
      mandatory = True
    )
    self['directory'] = Task.EntryInfo(
      questions = (
        "i didn't understand the directory, do you want to specify one?",
        "can you give a directory name?"
      ),
      mandatory = True
    )

  def build(self) -> str:
    return "echo > {}/{}.{}".format(
      self['directory'].field, 
      self['filename'].field, 
      self['extension'].field
    )
