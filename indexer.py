import json
from collections import defaultdict
from Tokenizer import Json_Tokenizer
from bs4 import BeautifulSoup

indices = defaultdict(set)

def process_json(json_file):
	json_dict = json.loads(json_file)
	indices

	



def build_index(documents):
	indexes = defaultdict(set) #key = token and value = set of URLS
	doc_id = 0
	tokenizer = Tokenize_object()
	for doc in documents:
		tokenized_doc = tokenizer.tokenize(doc)
		tokens_dict = tokenizer.computeWordFrequencies(tokenized_doc)
		for (token,frequency) in tokens_dict.items():
			indexes[token].add(tuple("URL from JSON doc", frequency)) #edit the string to get URL from the json doc 
	return indexes
    




