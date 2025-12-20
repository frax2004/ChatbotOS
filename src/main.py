import nltk



prompt = input(">> ")

grammar: nltk.CFG = nltk.data.load('grammars/large_grammars/atis.cfg')

parser = nltk.parse.ChartParser(grammar)

AST = parser.parse(prompt.split(' '))

for node in AST:
  print(node)
