import json
from bs4 import BeautifulSoup
from collections import defaultdict
from pathlib import Path
from tokenizer import tokenize
import os

# Index class takes in the path of the set of data being indexed,
#	the path where the index will be dumped, and the threshold
#	of number of documents to be parsed before dumping the stored
#	partial_index.

class Index:
	def __init__(self, dataset_path, dump_path, dump_threshold):
		self.index = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))   # {'a':{'aword':{'url':freq}}, 'b':{'bword':{'url':freq}}}
		self.dataset_path = Path(dataset_path)
		self.dump_path = Path(dump_path)
		self.dump_threshold = dump_threshold
		self.num_tokens = 0
		self.num_documents = 0
		self.partial_index_num = 0
		self.num_docs_processed = 0

	def start(self):												# Starts the indexing process
		for file_name in self.dataset_path.iterdir():
			for json_file in file_name.iterdir():
				if json_file.suffix == ".json":
					self._process_json(json_file)
		if self.num_docs_processed < self.dump_threshold:			# Final dumps
			self._dump()
		self._merge()
		print("FINISHED INDEXING")

	def index_size(self):
		return (self.num_tokens, self.num_documents)

	def _process_json(self, json_file):
		with open(json_file, 'r') as f:								# Parses through each website's contents, tokenizes, 
			json_dict = json.load(f)						#	and performs relevant score calculations
		url = json_dict["url"]										# Stores token and its postings in the relevant bucket
		encoding = json_dict["encoding"]							#	in self.index based on the first letter of the word
		soup = BeautifulSoup(json_dict["content"], 'html.parser')
		if bool(soup.find()):										# Checks if text has html, if not, document is ignored
			self.num_docs_processed += 1
			self.num_documents += 1
			print("Processing: {}".format(json_file))					# Processes the json file at the given path
			tokens = tokenize(soup.get_text(), r"[a-zA-Z]+[a-zA-Z'-]*[a-zA-Z']+")
			for word, frequency in tokens.items():
				bucket = word[0]
				self.index[bucket][word][url] = frequency
			if self.num_docs_processed == self.dump_threshold:			# If the threshold for number fo documents parsed is met,
				self._dump()												#	the current partial index stored is dumped.
		else:
			print("No HTML: {}".format(json_file))

	def _create_dumps(self, partial_index_num):						# Creates the dump buckets of each numbered partial index.
		for letter in 'abcdefghijklmnopqrstuvwxyz':
			with open(self.dump_path.joinpath(letter + str(partial_index_num) + '.json'), 'w', encoding='utf-8') as f:
				json.dump({}, f)

	def _dump(self):													# Dumps current partial index stored in self.index to the 
		print('DUMPING PARTIAL INDICES')							#	relevant numbered buckets created by create_dumps()
		self._create_dumps(self.partial_index_num)					#	After each dump, self.index is emptied,
		for bucket, words in self.index.items():					#	num_docs_processed is reset, and the partial_index_num is increased
			with open(self.dump_path.joinpath(bucket + str(self.partial_index_num) + '.json'), 'w', encoding='utf-8') as f:
				json.dump(self.index[bucket], f)
		self.index = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
		self.num_docs_processed = 0
		self.partial_index_num += 1

	def _merge(self):
		print("MERGING PARTIAL INDICES")
		for letter in 'abcdefghijklmnopqrstuvwxyz':
			master_bucket = defaultdict(lambda: defaultdict(int))
			for partial_bucket_num in range(self.partial_index_num):
				partial_bucket_path = self.dump_path.joinpath(letter + str(partial_bucket_num) + '.json')
				with open(partial_bucket_path, 'r', encoding='utf-8') as f:
					partial_bucket = json.load(f)
					for token, postings in partial_bucket.items():
						master_bucket[token].update(postings)
				os.remove(partial_bucket_path)
			master_bucket_path = self.dump_path.joinpath(letter + '.json')
			with open(master_bucket_path, 'w', encoding='utf-8') as f:
				json.dump(master_bucket, f)
			self.num_tokens+=len(master_bucket)

