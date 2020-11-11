import json
from collections import defaultdict
from Tokenizer import Tokenize_object, computeWordFrequencies

def build_index(documents):
    indexes = defaultdict(set)
    doc_id = 0
    for doc in documents:



