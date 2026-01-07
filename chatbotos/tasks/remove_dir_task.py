from chatbotos.tasks.task import Task
import os

class RemoveDirTask(Task):
  def __init__(self):
    super().__init__(
      ['directory', 'recursive'], 
      [
        lambda pair: os.path.isdir(pair[0]),
        lambda pair: pair[1] == "ADJ" or pair[0].lower() in ["yes", "no"]
      ],
      [
        lambda value: value,
        lambda value: "/r" if value.lower() in ["recursive" or "yes"] else "" 
      ]
    )

    self['directory'] = Task.EntryInfo(
      rejection_responses = (
        "I didn't understand the directory, do you want to specify one?",
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
    
    self['recursive'] = Task.EntryInfo(
      rejection_responses = (
        "Sorry, I don't understand what you mean",
        "Can you say it in another way please?"
      ),
      acceptance_responses = (
        "Perfect",
        "Ok, let's go to the next step"
      ),
      questions = (
        "Do you want to delete all the contents of the folder?",
        "Would you delete the folder recursively?"
      ),
      mandatory = True
    )

  def build(self) -> str:
    return "rd {} {}".format(
      self['recursive'].field,
      self['directory'].field 
    )
