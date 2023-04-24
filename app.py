from flask import Flask,render_template,request,redirect,url_for,flash,session
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import werkzeug
from flask_bcrypt import Bcrypt, check_password_hash


app = Flask(__name__)
app.secret_key='admin123'
bcrypt = Bcrypt(app)


db = sqlite3.connect("posts-collection.db")
ub = sqlite3.connect("users-collection.db")
cursor = db.cursor()
cur = ub.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email varchar(150) NOT NULL, name varchar(250) NOT NULL, password varchar(250) NOT NULL)")

# cursor.execute("INSERT INTO posts VALUES(2, 'Second Post', 'My second post my friend!')")
db.commit()
ub.commit()




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
    
@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':                
            email = request.form['email']
            name = request.form['name']          
            password=request.form['password']
            pw = bcrypt.generate_password_hash(password)
            ub = sqlite3.connect("users-collection.db")
            cur = ub.cursor()
            cur.execute("insert into users(EMAIL,NAME,PASSWORD) values (?,?,?)",(email,name,pw))
            ub.commit()
            return redirect(url_for("index"))
    return render_template("register.html")

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        ub = sqlite3.connect("users-collection.db")
        cur = ub.cursor()
        pw = bcrypt.generate_password_hash(password)
        bcrypt.check_password_hash(pw, password)
        cur.execute("select email,password FROM users where email = '+email+' and password='+pw+'")
        ub.commit()
        return redirect(url_for("index"))
    return render_template("login.html")


# @app.route("/add", methods=['POST','GET'])
# def add():
#    if request.method=='POST':
#       title = request.form['title']
#       content = request.form['content']
#       db = sqlite3.connect("posts-collection.db")
#       cursor = db.cursor()
#       cursor.execute("insert into posts(TITLE,CONTENT) values (?,?)",(title,content))
#       db.commit()
#       return redirect(url_for("index"))
#    return render_template("add.html")




if __name__ == "__main__":
    app.run(debug=True)



