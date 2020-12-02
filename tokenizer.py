import re
from nltk.stem.snowball import SnowballStemmer
from collections import defaultdict

ss = SnowballStemmer('english')

def tokenize(text, regex):										# Tokenizer
	# numWords = 0
	words = defaultdict(int)
	for word in re.findall(regex, text):
		if '-' in word or "'" in word:
			# numWords += 1
			words[word.lower()]+=1
		else:
			# numWords += 1
			words[ss.stem(word.lower())]+=1
	return words 	# , numWords

def tokenize_query(text, regex):
	words = set()
	for word in re.findall(regex, text):
		if '-' in word or "'" in word:
			words.add(word.lower())
		else:
			words.add(ss.stem(word.lower()))
	return words

def get_words(text, regex):
	words = set()
	for word in re.findall(regex, text):
		if '-' in word or "'" in word:
			words.add(word.lower())
		else:
			words.add(ss.stem(word.lower()))
	return words