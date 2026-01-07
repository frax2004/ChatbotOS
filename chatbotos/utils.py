from nltk.test.gensim_fixt import setup_module
import gensim
import math

setup_module()
__model__ = gensim.models.Word2Vec.load("embeddings/brown.embedding")

def softmax(v):
  E = map(math.exp, v)
  S = sum(E)
  return list(map(lambda e: e/S, E))

def similarity(w1: str, s: list[str]) -> float:
  similarities = []
  for w in s:
    try:
      similarities.append(__model__.wv.similarity(w1, w))
    except: pass

  return max([0, *similarities])
