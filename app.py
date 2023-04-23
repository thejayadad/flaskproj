from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)


db = sqlite3.connect("posts-collection.db")
cursor = db.cursor()
# # cursor.execute("CREATE TABLE posts (id INTEGER PRIMARY KEY, title varchar(150) NOT NULL, content varchar(250) NOT NULL)")

cursor.execute("INSERT INTO posts VALUES(2, 'Second Post', 'My second post my friend!')")
db.commit()





@app.route("/")
def index():
    return render_template('index.html')


@app.route("/add")
def add():
    return render_template('add.html')


if __name__ == "__main__":
    with app.app_context():
     db.create_all()
    app.run(debug=True)



