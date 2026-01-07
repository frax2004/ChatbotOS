from nltk.classify import NaiveBayesClassifier
from chatbotos.pretrain import train_test_split, extract_features
from chatbotos.datasets import COMMANDS, tagged_commands
from chatbotos.tokenizers import SplitTokenizer
from chatbotos.tasks import TASKS
import sys
import os

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

  @staticmethod  
  def reply(rep):
    print("[\033[38;2;255;215;0mEve\033[0m] : " + rep)

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
