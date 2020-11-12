from nltk.stem import PorterStemmer

words = ['said', 'typed', "step-mother", 'pythoned', "pemdas"]

ps = PorterStemmer()

for word in words:
	print(ps.stem(word))