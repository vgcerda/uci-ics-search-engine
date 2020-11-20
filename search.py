from collections import defaultdict
from pathlib import Path
import json
import time
from tokenizer import tokenize_query


def load_index(index_path):
	index = defaultdict(dict)
	print("LOADING INDEX")
	for char in 'abcdefghijklmnopqrstuvwxyz0':
		bucket = index_path.joinpath(char+'.json')
		with open(bucket, 'r', encoding='utf-8') as f:
			partial_index = json.load(f)
		index[char] = partial_index
	return index


class Query:
	def __init__(self, query_string, index):
		self._query = tokenize_query(query_string, r"[a-zA-Z0-9]+[a-zA-Z0-9'-]*[a-zA-Z0-9]+") #all tokens are stemmed from the query
		self._index = index
		self.result = [] #result is a nested list [[[IDF_Score, {DOCID: TFIDF_SCORE}]]
		self._get_relevant_documents()


	def _get_relevant_documents(self):
		for word in self._query:
			if word[0].isdigit():
				bucket = '0'
			else:
				bucket = word[0] #bucket is either alpha letter or 0 
			self.result.append(self._index[bucket][word]) #retrieves data from the word and appends doc IDS and posting values(TFIDF scores )


	# def get_relevant_documents(self):
	# 	i = 0
	# 	current_working_directory = Path(Path.cwd())
	# 	data_path  = current_working_directory.joinpath('INDEX')
	# 	current_file = data_path.joinpath(self._query[i][0] + ".json")
	# 	current_letter = self._query[i][0]
	# 	with open(current_file, 'r', encoding='utf-8') as f:
	# 				json_dict = json.load(f)
	# 	while i < len(self._query):
	# 		word = self._query[i]
	# 		if current_letter != word[0]:
	# 			if word[0].isdigit():
	# 				current_letter = "0"
	# 			else:
	# 				current_letter = word[0]	
	# 			current_file = data_path.joinpath(word[0] + ".json")
	# 			with open(current_file, 'r', encoding='utf-8') as f:
	# 				json_dict = json.load(f)
	# 		self.data[word] = json_dict[word][1].items()
	# 		i += 1

	def _calculate_Cosine_Similarity(self):
		return 0

if __name__ == "__main__":
	current_working_directory = Path(Path.cwd())
	data_path  = current_working_directory.joinpath('INDEX')
	index = load_index(data_path) #Index is a dictionary of all the json files

	query_string = input("Please Enter Your Query: ")
	start_time = time.time()
	query = Query(query_string, index) #index is passed into the query class
	print(time.time() - start_time)
	for item in query.result:
		print(item)