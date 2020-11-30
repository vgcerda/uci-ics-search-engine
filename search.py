from collections import defaultdict
from pathlib import Path
import json
import time
from tokenizer import tokenize_query
import math

# TODO:
# Store positions of words in index file and use seek to get it from an open file using that position
# 	implemented using term to byte offset dictionary
# Rank words in bold, headers, and other important tags high
# Bigrams
# when intersecting postings, start with the smallest len postings first
# GUI
# 	Use TKinter
# Implement postings class shown in one of the lectures

def load_index(index_path):
	index = defaultdict(dict)
	print("LOADING INDEX")
	for char in 'abcdefghijklmnopqrstuvwxyz0':
		bucket = index_path.joinpath(char+'.json')
		with open(bucket, 'r', encoding='utf-8') as f:
			partial_index = json.load(f)
		index[char] = partial_index
	return index

def load_url_lookup_table(url_lookup_table_path):
	print("LOADING URL TABLE")
	with open(url_lookup_table_path, 'r', encoding='utf-8') as f:
		table = json.load(f)
	return table

class Query:
	def __init__(self, query_string, index, url_table):
		self._url_table = url_table
		self._query = tokenize_query(query_string, r"[a-zA-Z0-9]+[a-zA-Z0-9'-]*[a-zA-Z0-9]+") #all tokens are stemmed from the query
		self._index = index
		self.relevant_document_ids = set()
		self.result = {} #result is a dictionary {word:[IDF, {docid:tfidf], word:[IDF, {docid:tfidf], word:[IDF, {docid:tfidf]}
		self.query_tfidf = defaultdict(float)
		self.cosine_similarity = []  # [(docID1, cosine_similarity), (docid2, cosinesimilarity)]

	def get_relevant_documents(self):
		for word in self._query:
			if word[0].isdigit():
				bucket = '0'
			else:
				bucket = word[0] #bucket is either alpha letter or 0 
			self.result[word] = self._index[bucket][word] #retrieves data from the word and appends doc IDS and posting values(TFIDF scores )

	def print_results(self):
		for i in range(len(self.cosine_similarity)):
			docid = self.cosine_similarity[i][0]
			print(f'{i + 1}. {self._url_table[docid]}')

			# The code below is for testing
			print(self.cosine_similarity[i][1])



	def calculate_Cosine_Similarity(self):
		tf = 1 # float(1.0/len(self._query))	# 1 / number of words in the query (to get tf of each word in query)
		
		# To calculate tf-idf score for queries, we are using the scheme ltc (logarithm, idf, cosine normalization)

		query_cosine_normalization = 0
		i = 0
		for word, postings in self.result.items():
			token_tfidf = tf * postings[0]	# tfidf score for each term in the query (postings[0] is the IDF score for the term)
			self.query_tfidf[word] = token_tfidf
			query_cosine_normalization += token_tfidf ** 2
			if i == 0:
				self.relevant_document_ids = set(postings[1].keys())
			else:
				self.relevant_document_ids = self.relevant_document_ids.intersection(set(postings[1].keys()))
			i+=1
		query_cosine_normalization = math.sqrt(query_cosine_normalization)

		for word in self.query_tfidf.keys():
			self.query_tfidf[word] = self.query_tfidf[word] / query_cosine_normalization

		for docid in self.relevant_document_ids:
			dot_product = 0
			query_value_squared = 0
			doc_value_squared = 0
			for word, token_tfidf in self.query_tfidf.items():
				doc_tfidf = self.result[word][1][docid]
				dot_product += token_tfidf * doc_tfidf

			# The code below was what was causing the problem. I length normalized all the tf-idf's beforehand so there is no need
			#	do the normalization again here. The reason is in lecture 21 starting from slide 28.
			#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			# 	query_value_squared += token_tfidf ** 2
			# 	doc_value_squared += doc_tfidf ** 2
			# length_normalization = math.sqrt(query_value_squared * doc_value_squared)
			# cos_sim = dot_product / length_normalization
			# self.cosine_similarity.append((docid, cos_sim))

			self.cosine_similarity.append((docid, dot_product))
		self.cosine_similarity = sorted(self.cosine_similarity, key=lambda x: -x[1])


if __name__ == "__main__":
	current_working_directory = Path(Path.cwd())
	data_path  = current_working_directory.joinpath('INDEX')
	url_table_path = current_working_directory.joinpath('URL_LOOKUP_TABLE.json')
	index = load_index(data_path) #Index is a dictionary of all the json files
	table = load_url_lookup_table(url_table_path)

	query_string = input("Please Enter Your Query: ")
	start_time = time.time()
	query = Query(query_string, index, table) #index is passed into the query class
	query.get_relevant_documents()
	query.calculate_Cosine_Similarity()
	query.print_results()

	print("Search Time: {}".format(time.time() - start_time))
	