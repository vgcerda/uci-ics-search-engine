from flask import Flask, url_for, render_template, request, redirect
from search import Search
from pathlib import Path
import json

app = Flask(__name__)

def load_url_lookup_table(url_lookup_table_path):
	print("LOADING URL TABLE")
	with open(url_lookup_table_path, 'r', encoding='utf-8') as f:
		table = json.load(f)
	return table

def load_byte_offset_table(byte_offset_table_path):
	print("LOADING BYTE OFFSET TABLE")
	with open(byte_offset_table_path, 'r', encoding='utf-8') as f:
		table = json.load(f)
	return table

current_working_directory = Path(Path.cwd())
url_table_path = current_working_directory.joinpath('URL_LOOKUP_TABLE.json')
byte_offset_table_path = current_working_directory.joinpath("BYTE_OFFSET_TABLE.json")
url_table = load_url_lookup_table(url_table_path)
byte_offset_table = load_byte_offset_table(byte_offset_table_path)

@app.route('/')
def base():
	return render_template('home.html')

@app.route('/search',  methods = ["POST", "GET"])
def s():
	if request.method == 'POST':
		query = request.form['query']
		results = Search(query).return_results()
	
	return render_template('search.html')

if __name__ == "__main__":
		
	app.run(debug=True)