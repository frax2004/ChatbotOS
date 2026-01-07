# NLTK
from nltk.classify import NaiveBayesClassifier

# Pretraining
from chatbotos.tokenizers import SplitTokenizer
from chatbotos.pretrain import train_test_split, extract_features
from chatbotos.datasets import COMMANDS, tagged_commands

# Tasks
from chatbotos.tasks.task import Task
from chatbotos.tasks.create_file_task import CreateFileTask
from chatbotos.tasks.show_file_task import ShowFileTask
from chatbotos.tasks.show_dir_task import ShowDirTask

# Other
import sys
import os


TASKS: dict[str, type[Task]] = {
  'CREATE_FILE': CreateFileTask, 
  # 'REMOVE_DIR': RemoveDirTask, # directory
  'SHOW_FILE': ShowFileTask,
  # 'CREATE_DIR': CreateDirTask, # directoryname, directory
  # 'REMOVE_FILE': RemoveFileTask, # file, directory
  # 'MOVE': MoveTask, # file, srcdir, dstdir
  # 'RENAME': RenameTask, # srcname, dstname
  'SHOW_DIR': ShowDirTask,
  # 'CHANGE_DIR': ChangeDirTask, # directory
  # 'COPY': CopyTask, # file, srcdir, dstdir
}

# Per ignorare le parole "prive di contenuto informativo" si può utilizzare il pos tagger di nltk
# (tipo articoli, preposizioni)
# (l'unico contenuto informativo potrebbero darlo le congiunzioni tipo "and" che possono servire ad identificare
# la presenza di più task)
# Per più task, per determinare l'ordine si fa pos tagging per estrarre le piu frasi in un solo prompt
class Eve:
  def __init__(self):
    self.__tagged__ = {command['input'] : command['output'] for command in tagged_commands()}
    sentences = [command['input'].split(' ') for command in COMMANDS]
    feature_set = [(extract_features(sentence), ' '.join(sentence)) for sentence in sentences]
    self.__train_set__, self.__test_set__ = train_test_split(feature_set, .75)
    self.__classifier__ = NaiveBayesClassifier.train(self.__train_set__)

  def classify_task(self, prompt) -> str:
    sentence = SplitTokenizer.tokenize(prompt)
    predicted_class = self.__classifier__.classify(extract_features(sentence))
    return self.__tagged__[predicted_class]

  def chat(self, input_stream = sys.stdin, output_stream = sys.stdout):
    stdin, stdout = sys.stdin, sys.stdout
    sys.stdin, sys.stdout = input_stream, output_stream

    while True:
      prompt: str = input(">> ")
      if prompt == 'exit': break
      taskname = self.classify_task(prompt)

      Task = TASKS[taskname]
      task = Task()
      task.fill(prompt)
      command = task.build()

      answer = input("Executing \"{}\" command. are you sure? yes/no: ".format(command))

      if answer == 'yes': os.system(command)

    sys.stdin, sys.stdout = stdin, stdout
