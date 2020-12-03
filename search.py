from collections import defaultdict
from pathlib import Path
import json
import time
from tokenizer import tokenize_query
import math
import heapq

# TODO:
# Implement MaxScore
# 	Compute the scores for the first N documents and find the min. After Those documents, any documents that have a lower score
#	will be skipped.
#	N is determined by the number of results that the user wants to be shown.
# Try Not normalizing tf-idfs and just store the normalization value in another table
# 	and use that later to do the cosine similarity with length normalization
# 	* Figure out what's wrong with cosine similarity/tf-idf calculations
# Bigrams
# GUI
# 	Use TKinter
# Implement postings class shown in one of the lectures (lecture 16 slide 31)
#	doesn't have to be a class but we have to store the fields of the token in the postings list

def load_url_lookup_table(url_lookup_table_path):
	print("LOADING URL TABLE")
	with open(url_lookup_table_path, 'r', encoding='utf-8') as f:
		table = json.load(f)
	return table

def load_byte_offset_table(byte_offset_table_path):
	print("LOADING BYTE OFFSET TABLE")
	with open(byte_offset_table_path, 'r', encoding='utf-8') as f:
		table = json.load(f)
	return table

class Search:
	def __init__(self, query_string, url_table, byte_offset_table):
		self._query = tokenize_query(query_string, r"[a-zA-Z0-9]+[a-zA-Z0-9'-]*[a-zA-Z0-9]+") #all tokens are stemmed from the query
		self._url_table = url_table
		self._byte_offset_table = byte_offset_table

		self.relevant_document_ids = set()
		self.relevant_postings = {} #result is a dictionary {word:[IDF, {docid:tfidf], word:[IDF, {docid:tfidf], word:[IDF, {docid:tfidf]}

		self.query_tfidf = defaultdict(float)
		self.scores = []
		self.cosine_similarity = []  # [(docID1, cosine_similarity), (docid2, cosinesimilarity)]

		current_working_directory = Path(Path.cwd())
		data_path  = current_working_directory.joinpath('INDEX')
		index_path = data_path.joinpath("index.txt")

		self._index = open(index_path, 'r', encoding='utf-8')  # Index is an open file on which we can perform seek and readline operations
		
		self._get_relevant_postings()
		self._calculate_Scores()
		# self._calculate_Cosine_Scores()

		self._index.close()

	def return_results(self):
		for docid, _ in self.scores:
			yield self._url_table[docid]

	def _get_relevant_postings(self):
		delete = set()
		for token in self._query:
			if token in self._byte_offset_table:
				self._index.seek(self._byte_offset_table[token])
				postings_as_string = self._index.readline()
				postings = json.loads(postings_as_string)
				if postings[1] > 1:
					self.relevant_postings[postings[0]] = postings[1:]
				else:
					delete.add(token)
			else:
				delete.add(token)
		for token in delete:
			self._query.remove(token)

	def print_results(self, k):

		for i in range(len(self.scores[:k])):
			docid = self.scores[i][0]
			print(f'{i + 1}. {self._url_table[docid]}')

			# The code below is for testing
			# print(self.cosine_similarity[i][1])

	def _calculate_Scores(self):
		i = 0
		for word, postings in self.relevant_postings.items():
			if i == 0:
				self.relevant_document_ids = set(postings[1].keys())
			else:
				self.relevant_document_ids = self.relevant_document_ids.union(set(postings[1].keys()))

		for docid in self.relevant_document_ids:
			score = 0
			for word in self._query:
				if docid in self.relevant_postings[word][1]:
					doc_tfidf = self.relevant_postings[word][1][docid]
				else:
					doc_tfidf = 0
				score += doc_tfidf
			self.scores.append((docid, score))

		self.scores.sort(key=lambda x: -x[1])

	def _calculate_Cosine_Scores(self):
		tf = 1 # float(1.0/len(self._query))	# 1 / number of words in the query (to get tf of each word in query)
		
		# To calculate tf-idf score for queries, we are using the scheme ltc (logarithm, idf, cosine normalization)

		query_cosine_normalization = 0
		i = 0
		for word, postings in self.relevant_postings.items():
			token_tfidf = tf * postings[0]	# tfidf score for each term in the query (postings[0] is the IDF score for the term)
			self.query_tfidf[word] = token_tfidf
			query_cosine_normalization += token_tfidf ** 2
			if i == 0:
				self.relevant_document_ids = set(postings[1].keys())
			else:
				self.relevant_document_ids = self.relevant_document_ids.union(set(postings[1].keys()))
			i+=1
		query_cosine_normalization = math.sqrt(query_cosine_normalization)

		for word in self.query_tfidf.keys():
			self.query_tfidf[word] = self.query_tfidf[word] / query_cosine_normalization

		for docid in self.relevant_document_ids:
			dot_product = 0
			query_value_squared = 0
			doc_value_squared = 0
			for word, token_tfidf in self.query_tfidf.items():
				if docid in self.relevant_postings[word][1]:
					doc_tfidf = self.relevant_postings[word][1][docid]
				else:
					doc_tfidf = 0
				dot_product += token_tfidf * doc_tfidf
				query_value_squared += token_tfidf ** 2
				doc_value_squared += doc_tfidf ** 2

			# The code below was what was causing the problem. I length normalized all the tf-idf's beforehand so there is no need
			#	do the normalization again here. The reason is in lecture 21 starting from slide 28.
			#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
			# 	query_value_squared += token_tfidf ** 2
			# 	doc_value_squared += doc_tfidf ** 2
			length_normalization = math.sqrt(query_value_squared * doc_value_squared)
			cos_sim = dot_product / length_normalization
			# self.cosine_similarity.append((docid, cos_sim))

			self.cosine_similarity.append((docid, cos_sim))
		self.cosine_similarity = sorted(self.cosine_similarity, key=lambda x: -x[1])


if __name__ == "__main__":
	current_working_directory = Path(Path.cwd())
	url_table_path = current_working_directory.joinpath('URL_LOOKUP_TABLE.json')
	byte_offset_table_path = current_working_directory.joinpath("BYTE_OFFSET_TABLE.json")
	url_table = load_url_lookup_table(url_table_path)
	byte_offset_table = load_byte_offset_table(byte_offset_table_path)

	query_string = input("Please Enter Your Query: ")
	start_time = time.time()
	query = Search(query_string, url_table, byte_offset_table) #index is passed into the query class
	query.print_results(30)
	print("Search Time: {}".format(time.time() - start_time))
	
	