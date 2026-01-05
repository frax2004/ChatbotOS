from chatbotos.datasets import Datasets
from nltk.metrics import edit_distance

def check_keywords(word: str):
  for (tag, items) in Datasets.KEYWORDS.items():
    if word in items:
      return (word, True)
  return (word, False)

def check_sentence_for_non_keywords(sentence: list[str]):
  check_list: list[tuple[str, bool]] = []
  for word in sentence:
    check_list.append(check_keywords(word))
  
  return check_list

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


def syntax_check(sentence: list[str]):
  THRESHOLD = 3

  similarities = []
  for word in sentence:
    for _, keywords in Datasets.KEYWORDS.items():
      sims: list[tuple] = [(w, edit_distance(word, w)) for w in keywords]
      similarities += list(filter(lambda pair: pair[1] < THRESHOLD and pair[1] > 0, sims))

  return similarities
  # print("I don't understand \033[1m{}\033[0m did you mean \033[1m{}\033[0m?".format(word, pair[0].lower()))
