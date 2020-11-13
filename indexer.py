from index import Index
from pathlib import Path

# TODO:
#	Write a better tokenizer (stems words and accepts numbers, hyphenated words, and words with apostrophes)
#	Assign ID's to each url

if __name__ == "__main__":
	current_working_directory = Path(Path.cwd())
	dataset_path = current_working_directory.joinpath('DEV')
	dump_path = current_working_directory.joinpath('INDEX')

	i = Index(current_working_directory, dataset_path, dump_path, 5000)
	i.start()
	i_size = i.index_size()

	print("Number of Tokens: {}\nNumber of Documents: {}".format(i_size[0], i_size[1]))

	

