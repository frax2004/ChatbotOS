from tokenizers import SplitTokenizer
import pretrain as pt

# def syntax_check(sentence: list[str]) -> None:
#   for word in sentence:
#     similarities = []
#     for _, keywords in Datasets.KEYWORDS.items():
#       if word not in Datasets.KEYWORDS.values():
#         sims: list[tuple] = [(w, edit_distance(word, w)) for w in keywords]
#         similarities += list(map(lambda pair: pair[0], filter(lambda pair: pair[1] < threshold, sims)))
#     print("I don't understand {} did you mean one of these? {}".format(word, ', '.join(similarities)))


# Per ignorare le parole "prive di contenuto informativo" si può utilizzare il pos tagger di nltk
# (tipo articoli, preposizioni)
# (l'unico contenuto informativo potrebbero darlo le congiunzioni tipo "and" che possono servire ad identificare
# la presenza di più task)
# Per più task, per determinare l'ordine si fa pos tagging per estrarre le piu frasi in un solo prompt
while True:
  prompt: str = input(">> ")

  # def print_features(prompt: str):
  #   sentence_tokens = SplitTokenizer.tokenize(prompt)
  #   syntax_check(sentence_tokens)

  #   features = extract_features(sentence_tokens)
  #   print(sentence_tokens)
  #   for (feature, is_present) in features.items():
  #     print(feature, is_present)

  #print_features(prompt)

  #prova di check_keyword_for_sentence
  sentence_tokens = SplitTokenizer.tokenize(prompt)
  check_list = pt.check_keywords_for_sentence(sentence_tokens)
  print(check_list)



# while 1:
#   prompt: str = input(">> ")

#   dataset = {
#     "": 
#   }
#   train_set = []

#   classifier = Classifier.train(train_set)
#   task = classifier.classify(prompt)
#   task --> command
#   os.system(command)
  
