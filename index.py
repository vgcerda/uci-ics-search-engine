import json
import re
from bs4 import BeautifulSoup
from collections import defaultdict
from pathlib import Path
from tokenizer import tokenize


class Index:
	def __init__(self, dataset_path, dump_path, dump_threshold):
		self.index = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))   # {'a':{'aword':{'url':freq}}, 'b':{'bword':{'url':freq}}}
		self.dataset_path = dataset_path
		self.dump_path = dump_path
		self.dump_threshold = dump_threshold
		self.partial_index_num = 0
		self.num_docs_processed = 0

	def start(self):
		database_folder = Path(self.dataset_path)
		for file_name in database_folder.iterdir():
			for json_file in file_name.iterdir():
				if json_file.suffix == ".json":
					self.process_json(json_file)

	def process_json(self, json_file):
		self.num_docs_processed += 1
		print("Processing: {}".format(json_file))									# Processes json file
		with open(json_file, 'r') as json_file:						# Parses through each website's contents, tokenizes, 
			json_dict = json.load(json_file)						#	and performs relevant score calculations
		url = json_dict["url"]										# Writes to INDEX			
		encoding = json_dict["encoding"]
		soup = BeautifulSoup(json_dict["content"], 'html.parser')
		tokens = tokenize(soup.get_text(), r"[a-zA-Z]+[a-zA-Z'-]*[a-zA-Z']+")
		for word, frequency in tokens.items():
			bucket = word[0]
			self.index[bucket][word][url] = frequency
		if self.num_docs_processed == self.dump_threshold:
			self.dump()

	def create_dump_buckets(self, partial_index_num):
		for letter in 'abcdefghijklmnopqrstuvwxyz':
			with open(Path(self.dump_path).joinpath(letter + str(partial_index_num) + '.json'), 'w', encoding='utf-8') as f:
				json.dump({}, f)

	def dump(self):
		print('DUMPING PARTIAL INDICES')
		self.create_dump_buckets(self.partial_index_num)
		for bucket, words in self.index.items():
			with open(Path(self.dump_path).joinpath(bucket + str(self.partial_index_num) + '.json'), 'w', encoding='utf-8') as f:
				json.dump(self.index[bucket], f)
		self.index = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
		self.num_docs_processed = 0
		self.partial_index_num += 1

