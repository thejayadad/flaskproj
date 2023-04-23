from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////posts-collection.db"
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.String(250), nullable=False)

    #Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Post {self.title}>'
    

new_post = Post(id=2, title="Second Post", content="Just sample text for my second post")
db.session.add(new_post)
db.session.commit()


# db = sqlite3.connect("posts-collection.db")
# cursor = db.cursor()
# # cursor.execute("CREATE TABLE posts (id INTEGER PRIMARY KEY, title varchar(150) NOT NULL, content varchar(250) NOT NULL)")

# cursor.execute("INSERT INTO posts VALUES(1, 'First Post', 'J. K. Rowling')")
# db.commit()

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post-collection.db'

# db = SQLAlchemy(app)
# app.app_context().push()

# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     content = db.Column(db.String(250), nullable=False)

    
#     def __str__(self):
#        return f'<Post {self.title}>'
    



# new_post = Post(id=1, title="First Post", content="Just my first post thats all")
# db.session.add(new_post)
# db.session.commit()

# db.create_all()



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



