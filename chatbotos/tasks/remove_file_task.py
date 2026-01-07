from chatbotos.tasks.task import Task
import os
import re

class RemoveFileTask(Task):
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

    self['directory'] = Task.EntryInfo(
      rejection_responses = (
        "I didn't understand the directory, would you specify one?",
        "I didn't find the directory in the file system, could you insert it again?",
        "The system doesn't contain any folder with the name you said; would you insert another one, please?"
      ),
      acceptance_responses = (
        "Perfect directory name",
        "The directory exists and we can continue",
        "I understood the directory name"
      ),
      questions = (
        "Can you give a directory name?",
        "Could you specify the directory name please?",
        "I need the folder name in order to execute your command"
      ),
      mandatory = True
    )
    
    self['filename'] = Task.EntryInfo(
      rejection_responses = (
        "I didn't understand the file name, rewrite it please.",
        "Can you write the file name please?"
      ),
      questions = (
        "Which file do you want to remove?",
        "Can you give a file name?",
        "Can you specify what is the file name?",
        "Can you give one file name?"
      ),
      acceptance_responses = (
        "Perfect",
        "Nice",
        "Good"
      ),
      matches = r"[a-zA-Z0-9_]*((\.[a-zA-Z0-9_])+)",
      mandatory = True
    )
    
    self['extension'] = Task.EntryInfo(
      rejection_responses = (
        "I didn't understand the extension, rewrite it please.",
        "Can you write the extension name please?"
      ),
      questions = (
        "I didn't understand the extension, can you specify one?",
        "Can you specify an extension?"
      ),
      acceptance_responses = (
        "Perfect",
        "Nice",
        "Good"
      ),
      matches = r"[a-zA-Z0-9_]*((\.[a-zA-Z0-9_])+)",
      mandatory = True
    )

  def build(self) -> str:
    return "rm {}\\{}.{}".format(
      self['directory'].field, 
      self['filename'].field, 
      self['extension'].field
    )
