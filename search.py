
from collections import defaultdict
from pathlib import Path
import json


class Query:
    def __init__(self, query_string):
        self._query = query_string.lower().split().sort()
        self.data = defaultdict(list)

    def get_relevant_documents(self):
		i = 0
		current_working_directory = Path(Path.cwd())
        data_path  = current_working_directory.joinpath('INDEX')
		current_file = data_path.joinpath(self._query[i][0] + ".json")
		current_letter = self._query[i][0]
		while i + 1 != len(self._query):
			with open(current_file, 'r', encoding='utf-8') as f:
				json_dict = json.load(f)	
			for word in self._query[i:]:
				if current_file[0] != word[0]:
					if word[0].isnum():
						current_letter = "0"
					else:
						current_letter = word[0]
					current_file = data_path.joinpath(word[0] + ".json")
					break
				else:
					self.data[word] = json_dict[word].items()
					i += 1

				
		
		
			if json_file[0] == word[0]:
				with open
				self_data[word] += json_file[word]
        
        # for json_file in self.data_path.iterdir():
        #     if json_file.is_dir() file.suffix == ".json":
        #         for word in self._query:
        #             if json_file[0] == word[0]:
        #                 self.data[word].append(json_file)
                



    def _calculate_Cosine_Similarity(self):
        return 0

if __name__ == "__main__":
	query = Query("cristina lopes")
	query.get_relevant_documents()
	print(query.data.items())
