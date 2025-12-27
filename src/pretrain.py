from datasets import Datasets
from nltk.metrics import edit_distance

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


def syntax_check(sentence: list[str]) -> None:
  THRESHOLD = 3

  for word in sentence:

    frequencies: list[tuple[str: int]] = []
    for tag, keywords in Datasets.KEYWORDS.items():
      sims: list[tuple] = [(w, edit_distance(word, w)) for w in keywords]
      #per ogni parola, prendiamo il tag corrispondente alle keywords con maggiore frequenza
      #dove la misura di frequenza è data da edit_distance < THRESHOLD e > 0
      similarities = list(filter(lambda pair: pair[1] < THRESHOLD and pair[1] > 0, sims))
      frequencies.append((tag, len(similarities)))

    pair: tuple[str, int] = max(frequencies, key = lambda pair: pair[1])
    print("I don't understand \033[1m{}\033[0m did you mean \033[1m{}\033[0m?".format(word, pair[0].lower()))