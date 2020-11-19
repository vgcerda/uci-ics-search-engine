
from collections import defaultdict
from pathlib import Path
import json
from nltk.stem.snowball import SnowballStemmer
import time

ss = SnowballStemmer('english')

class Query:
	def __init__(self, query_string):
		self._query = sorted([ss.stem(word) for word in query_string.lower().split()])
		self.data = defaultdict(list)

	def get_relevant_documents(self):
		i = 0
		current_working_directory = Path(Path.cwd())
		data_path  = current_working_directory.joinpath('INDEX')
		current_file = data_path.joinpath(self._query[i][0] + ".json")
		current_letter = self._query[i][0]
		with open(current_file, 'r', encoding='utf-8') as f:
					json_dict = json.load(f)
		while i < len(self._query):
			word = self._query[i]
			if current_letter != word[0]:
				if word[0].isdigit():
					current_letter = "0"
				else:
					current_letter = word[0]	
				current_file = data_path.joinpath(word[0] + ".json")
				with open(current_file, 'r', encoding='utf-8') as f:
					json_dict = json.load(f)
			self.data[word] = json_dict[word].items()
			i += 1

	def _calculate_Cosine_Similarity(self):
		return 0

if __name__ == "__main__":
	query = Query("cristina lopes")
	start_time = time.time()
	query.get_relevant_documents()
	print(time.time() - start_time)
	for key, postings in query.data.items():
		print(key)
		print(postings)
