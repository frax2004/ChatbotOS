from chatbotos.tasks.task import Task
import os

class CreateDirTask(Task):
  def __init__(self):
    super().__init__(
      ['directory', 'destination directory'], 
      [
        lambda pair: pair[1] == 'NOUN',
        lambda pair: os.path.isdir(pair[0])
      ],
      [
        lambda value: value,
        lambda value: value,
      ]
    )

    self['destination directory'] = Task.EntryInfo(
      questions = (
        'Can you give the destination directory?',
        'In which directory do you want to create the folder?',
        'Could you give me the name of the folder in which you want to create the directory, please?'
      ),
      rejection_responses = (
        "Sorry, i didn't understand the destination directory name",
        "I don't understand, can you say that again?",
        "I don't know this folder"
      ),
      acceptance_responses = (
        "Perfect, I will create the new folder into this directory",
        "Got it",
        "Yeah, let's do it!",
        "All right, so I will use this as the destination directory"
      )
    )
    
    self['directory'] = Task.EntryInfo(
      questions = (
        'Can you give me the new directory\'s name?',
        'Could you specify the name of the new folder, please?',
      ),
      rejection_responses = (
        "Sorry, I didn't understand the new dir's name",
        "I don't understand the new folder name",
        "I don't know man, repeat please"
      ),
      acceptance_responses = (
        "Ok then, I will create the new directory",
        "Got it",
        "Oook, I will add the new folder to the destination directory",
        "All right, so I will create this directory"
      )
    )
  
  def build(self):
    return "mkdir {}\\{}".format(
      self['destination directory'].field,
      self['directory'].field
    )

  def execute(self):
    path = self['destination directory'].field + '\\' + self['directory'].field
    if os.path.exists(path) and os.path.isdir(path):
      Task.error("Directory already exists")
    else:
      os.mkdir(path)
