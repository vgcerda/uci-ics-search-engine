import re
from nltk.stem import PorterStemmer
from collections import defaultdict

ps = PorterStemmer()

def tokenize(text, regex):										# Tokenizer
	words = defaultdict(int)
	for word in re.finditer(regex, text):
		if '-' in word.group(0):
			words[word.group(0).lower()]+=1
		else:
			words[ps.stem(word.group(0).lower())]+=1
	return words