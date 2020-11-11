import json
from collections import defaultdict
from Tokenizer import Tokenize_object

def build_index(documents):
    indexes = defaultdict(lambda: defaultdict(int)) #key = token and value = set of URLS
    doc_id = 0
    tokenizer = Tokenize_object()
    for json_doc in documents:
        tokenized_doc = tokenizer.tokenize(json_doc)
        tokens_dict = tokenizer.computeWordFrequencies(tokenized_doc)
        for (token,frequency) in tokens_dict.items():
            indexes[token]["URL from json doc"] = frequency #edit the string to get URL from the json doc 
    return indexes




