from nltk.test.gensim_fixt import setup_module
from chatbotos.datasets import Datasets
import gensim

setup_module()

inputs: list[list[str]] = []

for dictionary in Datasets.COMMANDS:
  inputs.append(list(w.lower() for w in dictionary['input'].split(' ')))

a = 1
train_set = inputs[:int(round(len(inputs)*a))]
model = gensim.models.Word2Vec(train_set)

sim = model.wv.similarity('delete', 'create')
print(sim)

l = model.wv.most_similar(positive=['delete', 'file'], negative = ['create', 'directory'], topn = 8)

for j in l:
  print(j)