from flask import Flask,render_template,request,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.secret_key='admin123'


db = sqlite3.connect("posts-collection.db")
cursor = db.cursor()
# # cursor.execute("CREATE TABLE posts (id INTEGER PRIMARY KEY, title varchar(150) NOT NULL, content varchar(250) NOT NULL)")

# cursor.execute("INSERT INTO posts VALUES(2, 'Second Post', 'My second post my friend!')")
# db.commit()





@app.route("/")
def index():
    db = sqlite3.connect("posts-collection.db")
    db.row_factory =sqlite3.Row
    cursor = db.cursor()
    cursor.execute("select * from posts")
    posts = cursor.fetchall()
    return render_template('index.html', post=posts)


@app.route("/add", methods=['POST','GET'])
def add():
   if request.method=='POST':
      title = request.form['title']
      content = request.form['content']
      db = sqlite3.connect("posts-collection.db")
      cursor = db.cursor()
      cursor.execute("insert into posts(TITLE,CONTENT) values (?,?)",(title,content))
      db.commit()
      return redirect(url_for("index"))
   return render_template("add.html")


      
@app.route("/edit/<int:id>", methods=['POST','GET'])
def edit(id):
   if request.method == 'POST':
       title = request.form['title']
       content = request.form['content']
       db = sqlite3.connect("posts-collection.db")
       cursor = db.cursor()
       cursor.execute("update posts set TITLE=?,CONTENT=? where ID=?",(title,content,id))
       db.commit()
       return redirect(url_for("index"))
   else:
        db = sqlite3.connect("posts-collection.db")
        db.row_factory =sqlite3.Row
        cursor = db.cursor()
        cursor.execute("select * from posts where ID=?", (id,))
        data = cursor.fetchone() 
        return render_template('edit.html', datas=data)

@app.route("/delete/<int:id>", methods=['GET'])
def delete(id):
     db = sqlite3.connect("posts-collection.db")
     cursor = db.cursor()
     cursor.execute("delete from posts where ID=?",(id,))
     db.commit()
     flash('Post Deleted Successfully')
     return redirect(url_for("index"))
    
   

if __name__ == "__main__":
    app.run(debug=True)



