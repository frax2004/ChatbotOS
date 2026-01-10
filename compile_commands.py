import random
from nltk.classify import NaiveBayesClassifier as Classifier
from chatbotos.pretrain import extract_features, train_test_split
from nltk.corpus import brown

from chatbotos.datasets import CONTEXT_FREE_GRAMMARS, generate
import os

THRESHOLD = 1_000_000

for command, grammar in CONTEXT_FREE_GRAMMARS.items():
  path = f'data\\commands\\{command.lower()}'
  with open(path, 'w+') as file:
    print(f'[START] Compiling {path}')
    strings = [' '.join(string) + '\n' for string in generate(grammar)]
    if len(strings) >= THRESHOLD:
      file.writelines(random.choices(strings, k = THRESHOLD))
    else:
      file.writelines(strings)      
    print(f'[FINISH] Compiled {path}')

sentences: list[tuple] = [(sent, 'UNDEFINED') for sent in brown.sents()]

for path in os.listdir('data\\commands\\'):
  with open('data\\commands\\' + path, 'r') as file:
    print(f'[START] Reading data\\commands\\{path}')
    taskname = path.upper()

    print(taskname)
    while True:
      sents = file.readlines(1024)
      if sents == []: break
      sentences += [(line.split(' '), taskname) for line in sents]

    print(f'[FINISH] data\\commands\\{path} Read')

print("[TRAINING] start")
feature_set = [(extract_features(sentence), taskname) for (sentence, taskname) in sentences]
__train_set__, __test_set__ = train_test_split(feature_set, 1)
__classifier__ = Classifier.train(__train_set__)

print("[TRAINING] finish")

import pickle

with open('classifier.pickle', 'wb') as file:
  print("[SAVING] start")
  pickle.dump(__classifier__, file)
  print("[SAVING] end")
