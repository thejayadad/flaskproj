from flask import Flask, render_template
import sqlite3


app = Flask(__name__)

db = sqlite3.connect("post-collection.db")
cursor = db.cursor()

cursor.execute("CREATE TABLE posts (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL, content varchar(250) NOT NULL)")


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/add")
def add():
    return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True)



