from chatbotos.tasks.task import Task
import re
import os
import shutil as shell

class MoveTask(Task):
  def __init__(self):
    super().__init__(
      ['file name', 'source directory', 'destination directory'], 
      [
        lambda pair: pair[1] == 'NOUN' and re.match(self['file name'].matches, pair[0]),
        lambda pair: os.path.isdir(pair[0]),
        lambda pair: os.path.isdir(pair[0])
      ],
      [
        lambda value: value,
        lambda value: value,
        lambda value: value
      ]
    )

    self['file name'] = Task.EntryInfo(
      questions = (
        'can you specify the file to move?',
        'can you give me the file to move?',
        'would you tell the file to move?'
      ),
      rejection_responses = (
        "sorry, i didn't understand the file name",
        "you haven't provided any file name",
        "the file name was not specified"
      ),
      acceptance_responses = (
        "ok then, i will move this file",
        "got it",
        "ok, i will move this file",
        "all right, so i will move that file"
      ),
      matches = r"[a-zA-Z0-9_]*((\.[a-zA-Z0-9_])+)"
    )

    self['source directory'] = Task.EntryInfo(
      questions = (
        'can you give the source directory?',
        'from which directory do you want to move the file?',
        'which directory do you want to move the file from?',
        'can you specify the directory to move the file from?'
      ),
      rejection_responses = (
        "sorry, i didn't understand in which directory is the file",
        "i don't understand where is the file to move",
        "i don't know from where to move the file"
      ),
      acceptance_responses = (
        "ok then, i will move the file from this directory",
        "got it",
        "ok, i will move the file from there",
        "all right, so i will move the file from this directory"
      )
    )
    
    self['destination directory'] = Task.EntryInfo(
      questions = (
        'can you give the destination directory?',
        'which directory do you want to move the file into?',
        'where do you want to move the file?',
        'can you specify the directory to move the file into?'
      ),
      rejection_responses = (
        "sorry, i didn't understand which directory to move the file into",
        "i don't understand where to move the file",
        "i don't know where to move the file"
      ),
      acceptance_responses = (
        "ok then, i will move the file into this directory",
        "got it",
        "ok, i will move the file in this directory",
        "all right, so i will move the file in this directory"
      )
    )

  def build(self):
    return 'move {}\\{} {}'.format(
      self['source directory'].field,
      self['file name'].field,
      self['destination directory'].field
    )

  def execute(self) -> None:
    source_path = self['source directory'].field + '\\' + self['file name'].field
    target_path = self['destination directory'].field

    if not (os.path.exists(source_path) and os.path.isfile(source_path)):
      Task.error('File to move "{}" does not exist'.format(source_path))
    elif not (os.path.exists(target_path) and os.path.isdir(target_path)):
      Task.error('Directory to move the file into "{}" does not exist'.format(target_path))
    else:
      shell.move(source_path, target_path)
