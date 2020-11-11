
import json
import re
from bs4 import BeautifulSoup
from collections import defaultdict
import os
from pathlib import Path


def json_buckets():
	for letter in 'abcdefghijklmnopqrstuvwxyz':
		with open(letter + '.json', 'w', encoding='utf-8') as f:
			json.dump(defaultdict(lambda: defaultdict(int)), f)

def tokenize(text, regex):
	words = defaultdict(int)
	for word in re.findall(regex, text):
		words[word]+=1
	return words

def process_json(json_file):
	json_dict = json.load(json_file)
	url = json_dict["url"]
	encoding = json_dict["encoding"]
	soup = BeautifulSoup(json_dict["content"], 'html.parser')
	tokens = tokenize(soup.get_text(), r"[a-zA-Z'-]*[a-zA-Z']+")
	for word, frequency in tokens:
		word_json = json.load(word[0] + '.json')
		word_json[word][url] = frequency
		json.dump(word[0] + '.json', word_json)

def build_indexer():
	current_directory = os.getcwd()
	folder = os.path.join(current_directory, 'ANALYST')
	for file_name in os.listdir(folder):
		for json_file in os.listdir(file_name):
			if json_file.endswith(".json"):
				process_json(json_file)


	# here we iterate through the words and put them in the corresponding files, along with urls