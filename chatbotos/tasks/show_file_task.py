from chatbotos.tasks.task import Task
import re
import os

#TODO: sistemare il riconoscimento di questa task
class ShowFileTask(Task):
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
      acceptance_responses = (
        'I found the file!',
        'The file is in the directory.',
        'The file exists.'
      ),
      rejection_responses = (
        'I can\'t seem to find the file. Could you please rewrite its name?',
        'Write the file name you want to see, please.',
        'There\'s no file with such name. Rewrite the name please.'
      ),
      questions = (
        'Could you please write the name of the file you want to be shown?',
        'Write the file name so that I can show it.'
        'Can you give me a file name?'
        'I\'d like to know which is the name of the file you want to be showed.',
        'Can you specify a file name?' 
      ),
      matches = r"[a-zA-Z0-9_]*((\.[a-zA-Z0-9_])+)",
      mandatory = True
    )

    self['extension'] = Task.EntryInfo(
      acceptance_responses = (
        "There is a file with the specified extension!",
        "I found a file with the specified extension.",
        "There is at least one file with the specified extension."
      ),
      rejection_responses = (
        'There isn\'t such an extension.',
        'I can\'t seem to find the extension. Please rewrite it.',
        'Rewrite the extension please.',
        'Could you please rewrite the extension?',
        'Are you sure you wrote the extension correctly? Could you please rewrite it?'
      ),
      questions = (
        'Can you give me an extension?',
        'Could you specify an extension?',
        'I\'d like to have an extension specified.',
        'Can you give me an extension?'
      ),
      matches = r"[a-zA-Z0-9_]*((\.[a-zA-Z0-9_])+)",
      mandatory = True
    )

    self['directory'] = Task.EntryInfo(
      acceptance_responses = (
          'Ok! I found the directory.',
          'The specified directory exists.'
      ),
      rejection_responses = (
        'I couldn\'t find the directory.'
        'There\'s no such directory. Please rewrite it.'
        'I can\'t seem find the specified directory.'
      ),
      questions = (
        'Could you specify a directory?',
        'I\'d like to have a directory specified',
        'Could you write a directory?',
        "I need a directory"
      ),
      mandatory = True
    )

  def build(self) -> str:
    return "type {}\\{}.{}".format(
      self['directory'].field, 
      self['filename'].field, 
      self['extension'].field
    )