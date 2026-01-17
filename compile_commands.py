from matplotlib.colors import LogNorm
from nltk.classify import NaiveBayesClassifier as Classifier
from nltk.corpus import brown
from nltk import ConfusionMatrix
from chatbotos.pretrain import extract_features, train_test_split
from chatbotos.datasets import CONTEXT_FREE_GRAMMARS, generate
import pickle
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import random
import os


THRESHOLD = 1_000_000

def compile_commands():
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

def load_commands():
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
  return sentences

def train(sentencies):
  print("[TRAINING] start")
  print("[TRAINING] extracting features")
  feature_set = [(extract_features(sentence), taskname) for (sentence, taskname) in sentencies]
  print("[TRAINING] features extracted")
  print("[TRAINING] shuffling")
  random.shuffle(feature_set)
  print("[TRAINING] shuffling complete")
  train_set, test_set = train_test_split(feature_set, .5)

  print("[TRAINING] training")
  classifier = Classifier.train(train_set)
  print("[TRAINING] training complete")
  print("[TRAINING] finish")
  return classifier, test_set

def evaluate(classifier: Classifier, test_set):
  print("[EVALUATION] start")
  gold = [label for (_, label) in test_set]
  predicted = [classifier.classify(features) for (features, _) in test_set]
  labels = set(gold)
  confusion_matrix = ConfusionMatrix(gold, predicted)
  results = {label: {func.__name__: func(label) for func in [confusion_matrix.precision, confusion_matrix.recall, confusion_matrix.f_measure]} for label in labels}

  sorted_labels = sorted(list(labels))
  cm_list = []

  for gold_label in sorted_labels:
    row = []
    for predicted_label in sorted_labels:
      row.append(confusion_matrix[gold_label, predicted_label])
    cm_list.append(row)

  cm_array = np.array(cm_list)

  plt.figure(figsize = (12, 8))
  sb.heatmap(cm_array, annot=True, fmt = 'd', cmap = 'Blues', xticklabels=sorted_labels, yticklabels=sorted_labels, norm = LogNorm())
  plt.title('Confusion Matrix')
  plt.xlabel('Actual')
  plt.ylabel('Predicted')
  plt.xticks(rotation = 45)
  plt.tight_layout()
  plt.savefig('confusion_matrix.png')
  plt.show()


  metrics = ['precision', 'recall', 'f_measure']
  x = np.arange(len(sorted_labels))
  width = 0.25

  fig, ax = plt.subplots(figsize = (14, 7))

  for i, metric in enumerate(metrics):
    values = [results[label][metric] if results[label][metric] is not None else 0 for label in sorted_labels]
    ax.bar(x + (i*width), values, width, label = metric.capitalize())

  ax.set_title('Performance Metrics per Class')
  ax.set_xticks(x + width)
  ax.set_xticklabels(sorted_labels, rotation = 45)
  ax.set_ylim(0, 1.1)
  ax.legend()
  ax.grid(axis = 'y', linestyle = '--', alpha = 0.7)

  plt.tight_layout()
  plt.savefig('classification_results.png')
  plt.show()

  print("[EVALUATION] finish")

def save(classifier: Classifier):
  with open('classifier.pickle', 'wb') as file:
    print("[SAVING] start")
    pickle.dump(classifier, file)
    print("[SAVING] end")


if __name__ == '__main__':

  # compile_commands()
  commands = load_commands()
  classifier, test_set = train(commands)
  evaluate(classifier, test_set)
  save(classifier)