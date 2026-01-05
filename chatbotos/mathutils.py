import math

def softmax(v):
  E = map(math.exp, v)
  S = sum(E)
  return list(map(lambda e: e/S, E))