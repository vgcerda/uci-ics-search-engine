import re
import sys
from collections import defaultdict
import json


def tokenize():
	json_dict = json.loads(json_file)
	self.url = json_dict['']
	for line in f:                                      # O(N) Dependent on the number of lines in a file
		for x in re.finditer(r'[0-9a-zA-Z]+', line):    # O(M) + O(P)
			yield x.group(0).lower()                    # O(1) always happens


# The computeWordFrequencies function has a runtime complexity of O(N)
#    derived from O(1) + O(N) * O(1) + O(1) = O(N)
#    Each component is enumerated in the comments below
def computeWordFrequencies(self, tokListGen):
	frequencies = defaultdict(lambda: 0)    # O(1)
	for t in tokListGen:                    # O(N) Iteration through all elements of the token list generator
		frequencies[t] += 1                 # O(1)
	return frequencies                      # O(1)
