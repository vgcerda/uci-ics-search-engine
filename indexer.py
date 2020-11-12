from index import Index
from pathlib import Path

# TODO:
#	Write a better tokenizer (stems words and accepts numbers, hyphenated words, and words with apostrophes)
#	Assign ID's to each url

if __name__ == "__main__":
	dataset_path = Path(Path.cwd()).joinpath('ANALYST')
	dump_path = Path(Path.cwd()).joinpath('INDEX')

	i = Index(dataset_path, dump_path, 5000)
	i.start()

	

