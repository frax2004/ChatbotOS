import abc


class Tokenizer:
  @staticmethod
  @abc.abstractmethod
  def tokenize(input: str): ...

class SplitTokenizer(Tokenizer):
  @staticmethod
  def tokenize(input: str):
    return input.split(' ')