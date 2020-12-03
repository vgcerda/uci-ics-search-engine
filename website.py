from flask import Flask, url_for, render_template, request, redirect
from search import Query

app = Flask(__name__)


@app.route('/')
def base():
    return render_template('home.html')





@app.route('/search',  methods = ["POST", "GET"])
def s():
    if request.method == 'POST':
        search = request.form['query']
        print(search) #put search buttons here
    return render_template('search.html')



if __name__ == "__main__":
    app.run(debug=True)