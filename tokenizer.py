import re
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict

ss = SnowballStemmer('english')

def tokenize(text, regex):										# Tokenizer
	numWords = 0
	words = defaultdict(int)
	for word in re.findall(regex, text):
		if '-' in word or "'" in word:
			numWords += 1
			words[word.lower()]+=1
		else:
			numWords += 1
			words[ss.stem(word.lower())]+=1
	return words, numWords
