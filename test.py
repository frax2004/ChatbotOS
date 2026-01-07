from nltk.test.gensim_fixt import setup_module
from nltk.corpus import brown
import gensim

setup_module()

inputs = brown.sents()


a = .75
train_set = inputs[:int(round(len(inputs)*a))]
model = gensim.models.Word2Vec(train_set)


while True:
  s = input(">> ")
  words = s.split(' ')
  sims = []
  for w in words:
    try:
      sims.append((w, model.wv.similarity('yes', w)))
    except: pass

  print(*sims, sep = '\n')
    
