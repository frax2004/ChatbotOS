# from chatbotos.datasets import COMMANDS, KEYWORDS
# from nltk.test.gensim_fixt import setup_module
# from itertools import chain
# from nltk.corpus import nps_chat, brown, genesis, gutenberg
import random
from nltk.classify import NaiveBayesClassifier as Classifier
from chatbotos.pretrain import extract_features, train_test_split

# import gensim

# setup_module()

# model = gensim.models.Word2Vec(nps_chat.posts() + brown.sents() + genesis.sents() + gutenberg.sents() + [[l.lower() for l in command['input'].split(' ')] for command in COMMANDS])

# keywords = {keyword.lower() for keyword in KEYWORDS.keys()}
# starts = set(chain.from_iterable([l.lower() for l in command['input'].split(' ')] for command in COMMANDS))

# for start in starts:
#   similarities = []
#   for keyword in keywords:
#     try:
#       similarities.append((keyword, start, float(model.wv.similarity(keyword, start))))
#     except:
#       similarities.append((keyword, start, 0))
  
#   print(*similarities, sep = '\n', end = '\n--------------')


from chatbotos.datasets import CONTEXT_FREE_GRAMMARS, generate
import os

# for command, grammar in CONTEXT_FREE_GRAMMARS.items():
#   with open(f'data\\commands\\{command.lower()}.command', 'w') as file:
#     print(f'[START] Compiling data\\commands\\{command.lower()}.commands')
#     strings = [' '.join(string) + '\n' for string in generate(grammar)]
#     file.writelines(random.choices(strings, k = int(round(len(strings)*.15))))
#     print(f'[FINISH] Compiled data\\commands\\{command.lower()}.commands')
    

sentences: list[tuple] = []

for path in os.listdir('data\\commands\\'):
  with open('data\\commands\\' + path, 'r') as file:
    print(f'[START] Reading data\\commands\\{path}')
    taskname = os.path.basename(path).split('.')[0].upper()
    
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

with open('classifier.json', 'w') as file:
  print("[SAVING] start")
  pickle.dump(__classifier__, file)
  print("[SAVING] end")
