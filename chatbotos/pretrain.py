from chatbotos.datasets import KEYWORDS
from nltk.metrics import edit_distance
from chatbotos.tokenizers import DefaultTokenizer
from nltk.tokenize import sent_tokenize
from nltk import pos_tag
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

def most_similar_by_syntax(prompt: str, threshold: int) -> str:
  sentence = DefaultTokenizer.tokenize(prompt)
  keywords = set(chain(*KEYWORDS.values()))

  def most_similar(word):
    similars = tuple((w, edit_distance(word, w)) for w in keywords)
    similars = tuple(filter(lambda pair: pair[1] <= threshold, similars))
    return min(similars, key = lambda pair: pair[1])[0] if len(similars) > 0 else word

  return ' '.join(word if word in keywords else most_similar(word) for word in sentence)

def segments(prompt: str) -> list[str]:
  sentencies = []
  for sentence in sent_tokenize(prompt):

    tagged = pos_tag(DefaultTokenizer.tokenize(sentence))
    regex = '|'.join([word for word, tag in tagged if tag == 'CC'])
    if regex != '':
      sentencies += sentence.split(regex)
    else:
      sentencies.append(sentence)
  return sentencies
