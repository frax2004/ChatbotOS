import abc
from nltk.tokenize import word_tokenize, sent_tokenize

class Tokenizer:
  @staticmethod
  @abc.abstractmethod
  def tokenize(input: str): ...

class SplitTokenizer(Tokenizer):
  @staticmethod
  def tokenize(input: str):
    return input.split(' ')
  
class WordTokenizer(Tokenizer):
  @staticmethod
  def tokenize(input: str):
    return word_tokenize(input)

class SentenceTokenizer(Tokenizer):
  @staticmethod
  def tokenize(input: str):
    return sent_tokenize(input)
  
DefaultTokenizer = WordTokenizer

