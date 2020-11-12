import json
from bs4 import BeautifulSoup
from collections import defaultdict
from pathlib import Path
from tokenizer import tokenize


# Index class takes in the path of the set of data being indexed,
#	the path where the index will be dumped, and the threshold
#	of number of documents to be parsed before dumping the stored
#	partial_index.

class Index:
	def __init__(self, dataset_path, dump_path, dump_threshold):
		self.index = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))   # {'a':{'aword':{'url':freq}}, 'b':{'bword':{'url':freq}}}
		self.dataset_path = dataset_path
		self.dump_path = dump_path
		self.dump_threshold = dump_threshold
		self.partial_index_num = 0
		self.num_docs_processed = 0

	def start(self):												# Starts the indexing process
		database_folder = Path(self.dataset_path)
		for file_name in database_folder.iterdir():
			for json_file in file_name.iterdir():
				if json_file.suffix == ".json":
					self.process_json(json_file)
		if self.num_docs_processed < self.dump_threshold:			# Final dumps
			self.dump()
		print("FINISHED INDEXING")

	def process_json(self, json_file):
		self.num_docs_processed += 1
		print("Processing: {}".format(json_file))					# Processes the json file at the given path
		with open(json_file, 'r') as json_file:						# Parses through each website's contents, tokenizes, 
			json_dict = json.load(json_file)						#	and performs relevant score calculations
		url = json_dict["url"]										# Stores token and its postings in the relevant bucket
		encoding = json_dict["encoding"]							#	in self.index based on the first letter of the word
		soup = BeautifulSoup(json_dict["content"], 'html.parser')
		tokens = tokenize(soup.get_text(), r"[a-zA-Z]+[a-zA-Z'-]*[a-zA-Z']+")
		for word, frequency in tokens.items():
			bucket = word[0]
			self.index[bucket][word][url] = frequency
		if self.num_docs_processed == self.dump_threshold:			# If the threshold for number fo documents parsed is met,
			self.dump()												#	the current partial index stored is dumped.

	def create_dumps(self, partial_index_num):						# Creates the dump buckets of each numbered partial index.
		for letter in 'abcdefghijklmnopqrstuvwxyz':
			with open(Path(self.dump_path).joinpath(letter + str(partial_index_num) + '.json'), 'w', encoding='utf-8') as f:
				json.dump({}, f)

	def dump(self):													# Dumps current partial index stored in self.index to the 
		print('DUMPING PARTIAL INDICES')							#	relevant numbered buckets created by create_dumps()
		self.create_dumps(self.partial_index_num)					#	After each dump, self.index is emptied,
		for bucket, words in self.index.items():					#	num_docs_processed is reset, and the partial_index_num is increased
			with open(Path(self.dump_path).joinpath(bucket + str(self.partial_index_num) + '.json'), 'w', encoding='utf-8') as f:
				json.dump(self.index[bucket], f)
		self.index = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
		self.num_docs_processed = 0
		self.partial_index_num += 1

