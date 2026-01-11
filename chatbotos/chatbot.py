# NLTK
from nltk.classify import NaiveBayesClassifier as Classifier

# Pretraining
from chatbotos.tokenizers import DefaultTokenizer
from chatbotos.pretrain import train_test_split, extract_features, most_similar_by_syntax, segments

# Tasks
from chatbotos.tasks.task import Task
from chatbotos.tasks.create_file_task import CreateFileTask
from chatbotos.tasks.copy_task import CopyTask
from chatbotos.tasks.move_task import MoveTask
from chatbotos.tasks.remove_dir_task import RemoveDirTask
from chatbotos.tasks.show_file_task import ShowFileTask
from chatbotos.tasks.show_dir_task import ShowDirTask
from chatbotos.tasks.create_dir_task import CreateDirTask
from chatbotos.tasks.remove_file_task import RemoveFileTask
from chatbotos.tasks.change_dir_task import ChangeDirTask
from chatbotos.tasks.rename_task import RenameTask

# Other
import sys
import os
import random
import pickle

from chatbotos.utils import similarity

TASKS: dict[str, type[Task]] = {
  'CREATE_FILE': CreateFileTask, 
  'REMOVE_DIR': RemoveDirTask,
  'SHOW_FILE': ShowFileTask,
  'SHOW_DIR': ShowDirTask,
  'COPY': CopyTask,
  'MOVE': MoveTask,
  'CREATE_DIR': CreateDirTask,
  'REMOVE_FILE': RemoveFileTask,
  'RENAME': RenameTask,
  'SHOW_DIR': ShowDirTask,
  'CHANGE_DIR': ChangeDirTask,
}

# Per ignorare le parole "prive di contenuto informativo" si può utilizzare il pos tagger di nltk
# (tipo articoli, preposizioni)
# (l'unico contenuto informativo potrebbero darlo le congiunzioni tipo "and" che possono servire ad identificare
# la presenza di più task)
# Per più task, per determinare l'ordine si fa pos tagging per estrarre le piu frasi in un solo prompt
class Eve:
  def __init__(self):

    if os.path.exists('classifier.pickle'):
      Task.debug("Creating Classifier...")
      with open('classifier.pickle', 'rb') as file:
        self.__classifier__ = pickle.load(file)
      Task.debug("Classifier ready")

    else: 
      sentences: list[tuple] = []
      for path in os.listdir('data\\commands\\'):
        with open('data\\commands\\' + path, 'r') as file:
          print(f'[START] Reading data\\commands\\{path}')
          taskname = os.path.basename(path).upper()
          
          while True:
            sents = file.readlines(1024)
            if sents == []: break
            sentences += [(line.split(' '), taskname) for line in sents]

          print(f'[FINISH] data\\commands\\{path} Read')

      feature_set = [(extract_features(sentence), taskname) for (sentence, taskname) in sentences]
      self.__train_set__, self.__test_set__ = train_test_split(feature_set, 1)
      self.__classifier__ = Classifier.train(self.__train_set__)
      

  def classify_task(self, prompt) -> str:
    sentence = DefaultTokenizer.tokenize(prompt)
    predicted_class = self.__classifier__.classify(extract_features(sentence))
    return predicted_class

  def try_predict(self, prompt: str) -> str:
    predicted_prompt = most_similar_by_syntax(prompt, 2)

    taskname = self.classify_task(predicted_prompt)
    TaskType = TASKS.get(taskname)

    if TaskType != None:
      Task.reply('Did you mean ' + taskname + '?')
      answer = Task.user()

      if similarity('yes', answer.split(' ')) > .8: 
        return TaskType
    
    return None


  def chat(self, input_stream = sys.stdin, output_stream = sys.stdout):
    stdin, stdout = sys.stdin, sys.stdout
    sys.stdin, sys.stdout = input_stream, output_stream

    initial_responses = (
      'Hello user, how may i help you?',
      'Hi there, how can i help you today?',
      'What can i do today for you?',
      'Welcome back user, what do we do?'
    )

    rejection_responses = (
      "Sorry i didn't understand what to do",
      "I don't understand the task",
      "Be more precise",
      "I can't do this",
      "Sorry, i am not supposed to do this"
    )

    mid_responses = (
      "Great! what's next?",
      "Anything else?",
      "What do we do now?"
    )

    final_responses = (
      'All right! See you soon...',
      'As you wish user, see you later!',
      "Bye bye!",
      "See you next time user!"
    )

    response = random.choice(initial_responses)
    Task.reply(response)

    while True:
      user_input: str = Task.user()
      if user_input == 'exit': break

      prompts = segments(user_input)

      for prompt in prompts:
        taskname = self.classify_task(prompt)
        TaskType = TASKS.get(taskname)

        if TaskType == None:
          TaskType = self.try_predict(prompt)

        if TaskType != None:
          task = TaskType()
          task.fill(prompt)
          command = task.build()

          Task.reply("Should i execute the \"{}\" command?".format(command))
          answer = Task.user()

          if similarity('yes', answer.split(' ')) > .8: 
            task.execute()
        else:
          # Task.error('Unkown task "{}"'.format(taskname))
          response = random.choice(rejection_responses)
          Task.reply(response)

      response = random.choice(mid_responses)
      Task.reply(response)

    response = random.choice(final_responses)
    Task.reply(response)

    sys.stdin, sys.stdout = stdin, stdout
