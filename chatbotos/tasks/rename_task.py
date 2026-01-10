from chatbotos.tasks.task import Task
import os
import re

class RenameTask(Task):
  def __init__(self):
    super().__init__(
      [
        'source file', 
        'target name',
      ],
      [
        lambda pair: os.path.isfile(pair[0]),
        lambda pair: pair[1] == 'NOUN' and re.match(self['target name'].matches, pair[0]),
      ],
      [
        lambda value: value,
        lambda value: value
      ],
    )

    self['source file'] = Task.EntryInfo(
      acceptance_responses = (
        "ok, so i got the file to rename",
        "good to know it",
        "perfect, so i'll rename that file"
      ),
      rejection_responses = (
        "sorry, i didn't get what is the file to rename",
        "i didn't understand the file to rename",
        "i don't know the file to rename"
      ),
      questions = (
        "can you specify the name of the file to rename?",
        "please specify the name of the file to rename",
        "can you tell which file to rename?",
      )
    )
    
    self['target name'] = Task.EntryInfo(
      acceptance_responses = (
        "great. i will rename it to that",
        "awesome! let's call it like that",
        "ok, we will call it like that"
      ),
      rejection_responses = (
        "sorry, i didn't understand the name",
        "i didn't understand what to call it",
        "i don't get how should i rename it"
      ),
      questions = (
        "how do you want to call it?"
        "can you give the new name?",
        "can you specify a new name?",
        "please choose a name",
        "can you write the new name?"
      ),
      matches = r"[a-zA-Z0-9_]*((\.[a-zA-Z0-9_])+)"
    )
    
  def build(self):
    return "rename {} {}".format(
      self['source file'].field,
      self['target name'].field
    )
    
  def execute(self) -> None:
    source_path = self['source file'].field
    target_path = self['target name'].field
    if not (os.path.exists(source_path) and os.path.isfile(source_path)):
      Task.error('File {} to rename does not exist'.format())
    elif os.path.exists(target_path):
      Task.error('File {} already exists'.format(target_path))
    else:
      os.rename(self['source file'].field, self['target name'].field)
