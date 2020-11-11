
import json
import re
from bs4 import BeautifulSoup
from collections import defaultdict

for i in 'abcdefghijklmnopqrstuvwxyz':
	with open(i + '.json', 'w', encoding='utf-8') as f:
		json.dump(dict(), f)

def tokenize(text, regex):
	words = defaultdict(int)
	for word in re.findall(regex, text):
		words[word]+=1
	return words

def process_json(json_file):
	json_dict = json.loads(json_file)
	url = json_dict["url"]
	encoding = json_dict["encoding"]
	soup = BeautifulSoup(json_dict["content"], 'html.parser')
	tokens = tokenize(soup.get_text(), r"[a-zA-Z'-]*[a-zA-Z']+")

	# here we iterate through the words and put them in the corresponding files, along with urls