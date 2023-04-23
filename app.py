from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post-collection.db'

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(250), nullable=False)

    
    def __str__(self):
       return f'<Post {self.title}>'
    



new_post = Post(id=1, title="First Post", content="Just my first post thats all")
db.session.add(new_post)
db.session.commit()

db.create_all()



@app.route("/")
def index():
    return render_template('index.html')


@app.route("/add")
def add():
    return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True)



