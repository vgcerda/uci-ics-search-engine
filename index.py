import json
from bs4 import BeautifulSoup
from collections import defaultdict
from pathlib import Path
import glob
from tokenizer import tokenize, get_words
import os
import time
import math

# Index class takes in the path of the set of data being indexed,
#	the path where the index will be dumped, and the threshold
#	of number of documents to be parsed before dumping the stored
#	partial_index.

class Index:
	def __init__(self, current_working_directory, dataset_path, dump_path, dump_threshold):
		self.index = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))   # {'a':{'aword': {'url':freq}}, 'b':{'bword':{'url':freq}}}
		self.url_lookup = {}													  # {ID:'url'}
		self.token_byte_offset_dict = {}

		self.cwd = Path(current_working_directory)
		self.dataset_path = Path(dataset_path)
		self.dump_path = Path(dump_path)

		assert (self.cwd.is_dir() and self.cwd.exists()), "Index::<current_working_directory> not existing directory"
		assert (self.dataset_path.is_dir() and self.dataset_path.exists()), "Index::<dataset_path> not existing directory"
		assert (self.dump_path.is_dir() and self.dump_path.exists()), "Index::<dump_path> not existing directory"

		self.dump_threshold = dump_threshold

		assert (self.dump_threshold > 0), "Index::<dump_threshold> invalid: must be positive"

		self.num_tokens = 0
		self.doc_num = 0
		self.partial_index_num = 0
		self.num_docs_processed = 0
		

	def start(self):													# Starts the indexing process
		print("INDEXING...")
		start_time = time.time()
		files_to_be_indexed = glob.glob(str(self.dataset_path.joinpath("*").joinpath("*.json")))
		print(len(files_to_be_indexed))
		for file in files_to_be_indexed:
			self._process_json(file)
		# for folder in self.dataset_path.iterdir():
		# 	if folder.is_dir():
		# 		for file in folder.iterdir():
		# 			if file.suffix == ".json":
		# 				self._process_json(file)
		if self.num_docs_processed < self.dump_threshold:				# Final dumps
			self._dump()
		self._merge_partial_indices()
		self._dump_token_byte_offset_dict()
		self._dump_url_lookup()
		# self._calculate_IDF_score()
		print("FINISHED INDEXING")
		print("Execution Time: {}".format(time.time() - start_time))

	def index_size(self):
		return (self.num_tokens, self.doc_num)

	def _process_json(self, json_file):
		with open(json_file, 'r') as f:									# Parses through each website's contents, tokenizes, 
			json_dict = json.load(f)									#	and performs relevant score calculations
		url = json_dict["url"]											# Stores token and its postings in the relevant bucket
		encoding = json_dict["encoding"]								#	in self.index based on the first letter of the word
		soup = BeautifulSoup(json_dict["content"], 'html.parser')
		for script in soup(['style', 'script']):
			script.extract()

		# if bool(soup.find()):											# Checks if text has html, if not, document is ignored
		self.num_docs_processed += 1
		self.doc_num += 1
		# print("Processing: {}".format(json_file))					# Processes the json file at the given path
		self.url_lookup[self.doc_num] = url
		
		tokens = tokenize(soup.get_text(" "), r"[a-zA-Z0-9]+[a-zA-Z0-9'-]*[a-zA-Z0-9]+")

		# Add weight to important words

		weighted = set()

		title_tag = soup.find('title')
		if title_tag:
			title_text = get_words(title_tag.get_text(" "), r"[a-zA-Z0-9]+[a-zA-Z0-9'-]*[a-zA-Z0-9]+")
			for word in title_text:
				weighted.add(word)
				tokens[word] *= 3

		for tag in soup.find_all(["b", "strong", "h1", "h2", "h3", "h4", "h5", "h6"]):
			if tag:
				words = get_words(tag.get_text(" "), r"[a-zA-Z0-9]+[a-zA-Z0-9'-]*[a-zA-Z0-9]+")
				for word in words:
					if word not in weighted:
						weighted.add(word)
						tokens[word] *= 2

		# To calculate tf-idf score of docs, we are using the scheme lnc (logarithm, no idf, cosine normalization)

		# cosine_normalization = 0
		# for word, frequency in tokens.items():
		# 	if word[0].isdigit():
		# 		bucket = '0'
		# 	else:
		# 		bucket = word[0]
		# 	normalized_tf = round(1 + math.log(float(frequency)), 15)
		# 	self.index[bucket][word][self.doc_num] = normalized_tf # Calculate normalized TF
		# 	cosine_normalization += normalized_tf ** 2
		# cosine_normalization = math.sqrt(cosine_normalization)

		for word, frequency in tokens.items():
			if word[0].isdigit():
				bucket = '0'
			else:
				bucket = word[0]
			normalized_tf = round(1 + math.log(float(frequency)), 15)
			self.index[bucket][word][self.doc_num] = normalized_tf # Calculate normalized TF

		# Apply Cosine Normalization to the tf-idf score

		# for word in tokens.keys():
		# 	if word[0].isdigit():
		# 		bucket = '0'
		# 	else:
		# 		bucket = word[0]
		# 	self.index[bucket][word][self.doc_num] = self.index[bucket][word][self.doc_num] / cosine_normalization

		if self.num_docs_processed == self.dump_threshold:			# If the threshold for number fo documents parsed is met,
			self._dump()											#	the current partial index stored is dumped.
		# else:
		# 	print("No HTML: {}".format(json_file))

	def _create_dumps(self, partial_index_num):							# Creates the dump buckets of each numbered partial index.
		for char in 'abcdefghijklmnopqrstuvwxyz0':
			with open(self.dump_path.joinpath(char + str(partial_index_num) + '.json'), 'w', encoding='utf-8') as f:
				json.dump({}, f)

	def _dump(self):													# Dumps current partial index stored in self.index to the 
		print('DUMPING PARTIAL INDICES')								#	relevant numbered buckets created by create_dumps()
		self._create_dumps(self.partial_index_num)						#	After each dump, self.index is emptied,
		for bucket, words in self.index.items():						#	num_docs_processed is reset, and the partial_index_num is increased
			with open(self.dump_path.joinpath(bucket + str(self.partial_index_num) + '.json'), 'w', encoding='utf-8') as f:
				json.dump(self.index[bucket], f)
		self.index = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
		self.num_docs_processed = 0
		self.partial_index_num += 1

	def _merge_partial_indices(self):
		print("MERGING PARTIAL INDICES")

		final_index_path = self.dump_path.joinpath('index.txt')
		final_index = open(final_index_path, 'a', encoding='utf-8')

		for char in 'abcdefghijklmnopqrstuvwxyz0':
			print("    MERGING {}.json INTO INDEX".format(char))
			master_bucket = defaultdict(lambda: defaultdict(int))
			for partial_bucket_num in range(self.partial_index_num):
				partial_bucket_path = self.dump_path.joinpath(char + str(partial_bucket_num) + '.json')
				with open(partial_bucket_path, 'r', encoding='utf-8') as f:
					partial_bucket = json.load(f)
					for token, postings in partial_bucket.items():
						master_bucket[token].update(postings)
				os.remove(partial_bucket_path)

			self.num_tokens+=len(master_bucket)

			for token, postings in master_bucket.items():
				self.token_byte_offset_dict[token] = final_index.tell()
				IDF = math.log(float(self.doc_num) / float(len(postings)))

				for docid in postings.keys():
					master_bucket[token][docid] = round(master_bucket[token][docid] * IDF, 15) 

				top_k_docs = sorted([[docid, tfidf] for docid, tfidf in postings.items()], key=lambda x: -x[1])[:2500]
				top_k_dict = {}
				for docid, tfidf in top_k_docs:
					top_k_dict[docid] = tfidf

				json.dump([token, round(IDF, 15), top_k_dict], final_index)

				# json.dump([token, round(IDF, 15), postings], final_index)
				final_index.write('\n')

		final_index.close()


			# master_bucket_path = self.dump_path.joinpath(char + '.json')
			# with open(master_bucket_path, 'w', encoding='utf-8') as f:
			# 	json.dump(master_bucket, f)
			
	def _dump_token_byte_offset_dict(self):
		print("DUMPING TOKEN TO BYTE OFFSET TABLE")
		with open(self.cwd.joinpath('BYTE_OFFSET_TABLE.json'), 'w', encoding='utf-8') as f:
			json.dump(self.token_byte_offset_dict, f)

	def _dump_url_lookup(self):
		print('DUMPING URL LOOKUP TABLE')
		with open(self.cwd.joinpath('URL_LOOKUP_TABLE.json'), 'w', encoding='utf-8') as f:
			json.dump(self.url_lookup, f)

	# def _calculate_IDF_score(self):
	# 	print("CALCULATING IDF SCORES")
	# 	for char in 'abcdefghijklmnopqrstuvwxyz0':						# Line 123 overwrites what what stored before (normalized TF)
	# 		print("  for " + char + '.json')
	# 		partial_index_path = self.dump_path.joinpath(char + '.json')
	# 		with open(partial_index_path, 'r', encoding='utf-8') as f:
	# 			partial_index = json.load(f)
	# 			for token, postings in partial_index.items():
	# 				IDF = math.log(float(self.doc_num) / float(len(postings)))
	# 				partial_index[token] = [round(IDF, 15), postings]

	# 				# We will not use IDF for calculating the weight of each document since we're using the scheme lnc
	# 				#	(check line 70 for comment)
	# 				#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	# 				# for docID in postings.keys():
	# 				# 	TF_IDF = postings[docID] * IDF
	# 				# 	partial_index[token][1][docID] = round(TF_IDF, 15)

	# 		with open(partial_index_path, 'w', encoding='utf-8') as f:
	# 			json.dump(partial_index, f)

if __name__ == "__main__":
	current_working_directory = Path(Path.cwd())
	dataset_path = current_working_directory.joinpath('DEV')
	dump_path = current_working_directory.joinpath('INDEX')
	if not dump_path.exists():
		dump_path.mkdir()
	i = Index(current_working_directory, dataset_path, dump_path, 5000)
	i.start()
	i_size = i.index_size()

	print("Number of Tokens: {}\nNumber of Documents: {}".format(i_size[0], i_size[1]))
