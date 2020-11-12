from index import Index
from pathlib import Path

# TODO:
#	Import PorterStemmer from nltk.stem to stem words
#	Calculate td-idf score for each url with each word
#	Ignore stem words
#	Refine word processing: stemming, splitting apostrophes, splitting hyphens
#	Find out how to rank words
#	Assign ID's to each url
#	Check for similarity of each url (store url simhashes in a data structure and do some comparisons)


if __name__ == "__main__":
	dataset_path = Path(Path.cwd()).joinpath('DEV')
	dump_path = Path(Path.cwd()).joinpath('INDEX')

	i = Index(dataset_path, dump_path, 20)
	i.start()

	

