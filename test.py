from nltk.test.gensim_fixt import setup_module
from nltk.corpus import *
import gensim
import os
import matplotlib.pyplot as plt

setup_module()

filenames = os.listdir('embeddings')

X = ['yes', 'yeah', 'ok', 'absolutely', 'surely', 'sure']

model = gensim.models.Word2Vec.load("embeddings/brown.embedding")
Y = [model.wv.similarity('yes', w) for w in X]
plt.scatter(X, Y)
plt.show()

