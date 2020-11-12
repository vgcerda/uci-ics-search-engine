
import json
import re
from bs4 import BeautifulSoup
from collections import defaultdict
import os
from pathlib import Path, PurePath

# TODO:
#	Calculate td-idf score for each url with each word
#	Ignore stem words
#	Refine word processing: stemming, splitting apostrophes, splitting hyphens
#	Find out how to rank words
#	Assign ID's to each url
#	Check for similarity of each url (store url simhashes in a data structure and do some comparisons)

cwd = Path(Path.cwd())
INDEX_path = cwd.joinpath('INDEX')

def create_index_buckets():										# Creates initial word buckets for INDEX
	for letter in 'abcdefghijklmnopqrstuvwxyz':
		with open(cwd.joinpath('INDEX', letter + '.json'), 'w', encoding='utf-8') as f:
			json.dump({}, f)

def tokenize(text, regex):										# Tokenizer
	words = defaultdict(int)
	for word in re.findall(regex, text):
		words[word]+=1
	return words

def process_json(json_file):									# Processes json file
	with open(json_file, 'r') as json_file:						# Parses through each website's contents, tokenizes, 
		json_dict = json.load(json_file)						#	and performs relevant score calculations
	url = json_dict["url"]										# Writes to INDEX			
	encoding = json_dict["encoding"]
	soup = BeautifulSoup(json_dict["content"], 'html.parser')
	tokens = tokenize(soup.get_text(), r"[a-zA-Z']*[a-zA-Z']+")
	for word, frequency in tokens.items():
		bucket = INDEX_path.joinpath(word[0] + '.json')
		with open(bucket, 'r') as json_bucket:
			word_json = json.load(json_bucket)
		if word not in word_json:
			word_json[word] = {}
		word_json[word][url] = frequency
		with open(bucket, 'w') as json_bucket:
			json.dump(word_json, json_bucket)

def build_index():												# Process all json files in DEV database
	database_folder = cwd.joinpath('DEV')
	for file_name in database_folder.iterdir():
		for json_file in file_name.iterdir:
			if json_file.endswith(".json"):
				process_json(json_file)

def test():
	test_path = cwd.joinpath('test')
	for json_file in test_path.iterdir():
		if json_file.suffix == '.json':
			process_json(json_file)

if __name__ == "__main__":
	create_index_buckets()

	# Run test() to test functions on test json files

	# Run build_index() index to build INDEX based on DEV database
	

