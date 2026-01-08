# from chatbotos.datasets import COMMANDS, KEYWORDS
# from nltk.test.gensim_fixt import setup_module
# from itertools import chain
# from nltk.corpus import nps_chat, brown, genesis, gutenberg

# import gensim

# setup_module()

# model = gensim.models.Word2Vec(nps_chat.posts() + brown.sents() + genesis.sents() + gutenberg.sents() + [[l.lower() for l in command['input'].split(' ')] for command in COMMANDS])

# keywords = {keyword.lower() for keyword in KEYWORDS.keys()}
# starts = set(chain.from_iterable([l.lower() for l in command['input'].split(' ')] for command in COMMANDS))

# for start in starts:
#   similarities = []
#   for keyword in keywords:
#     try:
#       similarities.append((keyword, start, float(model.wv.similarity(keyword, start))))
#     except:
#       similarities.append((keyword, start, 0))
  
#   print(*similarities, sep = '\n', end = '\n--------------')