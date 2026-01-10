from chatbotos.tasks.task import Task
import os
import re

class RemoveFileTask(Task):
  def __init__(self):
    super().__init__(
      ['file name'],
      [lambda pair: os.path.isfile(pair[0])],
      [lambda value: value]
    )
        
    self['file name'] = Task.EntryInfo(
      rejection_responses = (
        "I didn't understand the file name, rewrite it please.",
        "Can you write the file name please, I didn't understand?"
      ),
      questions = (
        "Which file do you want to remove? Please write file as \"PATH\\file.extension\"",
        "Can you give a file name? Please write file as \"PATH\\file.extension\"",
        "Can you specify what is the file name? Please write file as \"PATH\\file.extension\"",
        "Can you give one file name? Please write file as \"PATH\\file.extension\""
      ),
      acceptance_responses = (
        "Perfect",
        "Nice",
        "Good"
      ),
      mandatory = True
    )

  def build(self) -> str:
    return "del /f {}".format(self['file name'].field)

  def execute(self) -> None:
    path = self['file name'].field
    if os.path.exists(path):
      os.remove(self['file name'].field)
    else:
      Task.error('File to remove {} does not exist'.format(path))