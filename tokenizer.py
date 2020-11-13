import re
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict

ss = SnowballStemmer('english')

def tokenize(text, regex):										# Tokenizer
	words = defaultdict(int)
	for word in re.findall(regex, text):
		if '-' in word or "'" in word:
			words[word.lower()]+=1
		else:
			words[ss.stem(word.lower())]+=1
	return words