from index import Index
from pathlib import Path

# TODO:
#	Write a better tokenizer (stems words and accepts numbers, hyphenated words, and words with apostrophes)
#	Assign ID's to each url

if __name__ == "__main__":
	dataset_path = Path(Path.cwd()).joinpath('DEV')
	dump_path = Path(Path.cwd()).joinpath('INDEX')

	i = Index(dataset_path, dump_path, 1000)
	i.start()

	

