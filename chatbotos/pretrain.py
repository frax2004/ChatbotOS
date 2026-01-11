from chatbotos.datasets import KEYWORDS
from nltk.metrics import edit_distance
from itertools import chain

def split_keywords(sentence: list[str]):
  keywords = set(chain(*KEYWORDS.values()))
  is_keyword = lambda w: w.lower() in keywords
  return list((word, 'keyword' if is_keyword(word) else 'non-keyword') for word in sentence)


def train_test_split(dataset, pivot: float = .5):
  pivot = round(min(1, max(pivot, 0))*len(dataset))
  return dataset[:pivot], dataset[pivot:]


def extract_features(sentence: list[str]) -> dict[str, bool]:
  extract_features_word = lambda w: {
    tag: bool(w.lower() in keywords) for (tag, keywords) in KEYWORDS.items()
  }
  sentence_features: dict[str, bool] = dict.fromkeys(KEYWORDS.keys(), False)

  for word in sentence:
    features = extract_features_word(word)
    for feature in sentence_features.keys():
      sentence_features[feature] = sentence_features[feature] | features[feature]

  return sentence_features


def syntax_check(sentence: list[str]):
  THRESHOLD = 3

  similarities = []
  for word in sentence:
    for _, keywords in KEYWORDS.items():
      sims: list[tuple] = [(w, edit_distance(word, w)) for w in keywords]
      similarities += list(filter(lambda pair: pair[1] < THRESHOLD and pair[1] > 0, sims))

  return similarities
  # print("I don't understand \033[1m{}\033[0m did you mean \033[1m{}\033[0m?".format(word, pair[0].lower()))
