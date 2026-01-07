from chatbotos.tasks.task import Task
import os

class ShowDirTask(Task):
  def __init__(self):
    super().__init__(
      ['directory'],
      [
        lambda pair: os.path.isdir(pair[0])
      ],
      [
        lambda value: value
      ]
    )

        self['directory'] = Task.EntryInfo(
            acceptance_responses= (
                'Ok! I found the directory',
                'The specified directory exists'
            ),
            rejection_responses= (
                'I couldn\'t find the directory'
                'There\'s no such directory. Please rewrite it'
                'I can\'t seem find the specified directory'
            ),
            questions= (
                'Could you specify a directory?',
                'I\'d like to have a directory specified',
                'Could you write a directory?',
                "I need a directory"
            ),
            mandatory = True
        )

  def build(self) -> str:
    return "dir {}".format(
      self['directory'].field
    )