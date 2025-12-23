import nltk.corpus
import math
from datasets import Datasets
from itertools import chain
from nltk.metrics import edit_distance

def softmax(v):
  E = map(math.exp, v)
  S = sum(E)
  return list(map(lambda e: e/S, E))

class Classifier:
  @staticmethod
  def train(train_set):
    pass


def extract_features(sentence: list[str]) -> dict[str: bool]:
  def extract_feature(word: str) -> dict[str: bool]:
    return { 
      tag: bool(word in keywords) 
      for (tag, keywords) in Datasets.KEYWORDS.items() 
    }

  sentence_features: dict[str: bool] = { key: False for key in Datasets.KEYWORDS.keys() }
  for word in sentence:
    features = extract_feature(word)
    for feature in sentence_features.keys():
      sentence_features[feature] = sentence_features[feature] | features[feature]

  return sentence_features

class Tokenizer:
  def tokenize(input: str):
    raise NotImplementedError()

class SplitTokenizer(Tokenizer):
  def tokenize(input: str):
    return input.split(' ')

threshold = 3


# def syntax_check(sentence: list[str]) -> None:
#   for word in sentence:
#     similarities = []
#     for _, keywords in Datasets.KEYWORDS.items():
#       if word not in Datasets.KEYWORDS.values():
#         sims: list[tuple] = [(w, edit_distance(word, w)) for w in keywords]
#         similarities += list(map(lambda pair: pair[0], filter(lambda pair: pair[1] < threshold, sims)))
#     print("I don't understand {} did you mean one of these? {}".format(word, ', '.join(similarities)))

def syntax_check(sentence: list[str]) -> None:
  for word in sentence:

    frequencies = {}
    for tag, keywords in Datasets.KEYWORDS.items():
      sims: list[tuple] = [(w, edit_distance(word, w)) for w in keywords]
      similarities = list(filter(lambda pair: pair[1] < threshold and pair[1] > 0, sims))
      frequencies[tag] = len(similarities)

    pair = max(frequencies, key = lambda pair: pair[1])
    print("I don't understand {} did you mean {}".format(word, pair))


# Per più task, per determinare l'ordine si fa pos tagging per estrarre le piu frasi in un solo prompt
while True:
  prompt: str = input(">> ")

  def print_features(prompt: str):
    sentence_tokens = SplitTokenizer.tokenize(prompt)
    syntax_check(sentence_tokens)

    features = extract_features(sentence_tokens)
    print(sentence_tokens)
    for (feature, is_present) in features.items():
      print(feature, is_present)

  print_features(prompt)



# while 1:
#   prompt: str = input(">> ")

#   dataset = {
#     "": 
#   }
#   train_set = []

#   classifier = Classifier.train(train_set)
#   task = classifier.classify(prompt)
#   task --> command
#   os.system(command)
  
