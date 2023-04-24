from collections import UserString
from flask import Flask,render_template,request,redirect,url_for,flash,session,Blueprint
from flask_sqlalchemy import SQLAlchemy
import sqlite3
import werkzeug
from flask_bcrypt import Bcrypt, check_password_hash
import functools
from werkzeug.security import check_password_hash, generate_password_hash




app = Flask(__name__)
app.secret_key='admin123'
bcrypt = Bcrypt(app)
SESSION_TYPE = 'redis'
bp = Blueprint('auth', __name__, url_prefix='/auth')



db = sqlite3.connect("posts-collection.db")
ub = sqlite3.connect("users-collection.db")
cb = sqlite3.connect("comment-collection.db")

cursor = db.cursor()
cur = ub.cursor()
curs = cb.cursor()

# cur.execute("DROP TABLE users")
# cursor.execute("DROP TABLE posts")
# curs.execute("DROP TABLE comments")


cur.execute(""" CREATE TABLE IF NOT EXISTS users(
    id INT PRIMARY KEY,
    email VARCHAR(50),
    username VARCHAR(50) UNIQUE,
    password VARCHAR(50)   
)
""")

cursor.execute(""" CREATE TABLE IF NOT EXISTS posts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,   
    title VARCHAR(100),
    body VARCHAR(300),
    author_id INT,
    FOREIGN KEY (author_id) REFERENCES users(username) ON DELETE CASCADE
)
""")

curs.execute(""" CREATE TABLE IF NOT EXISTS comments(
    body VARCHAR(100),
    author_id INT,
    FOREIGN KEY (author_id) REFERENCES users(username) ON DELETE SET NULL
)
""")



# cur.execute("CREATE TABLE IF NOT EXISTS comment (id INTEGER PRIMARY KEY AUTOINCREMENT, author_id INTEGER NOT NULL,   created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,  body TEXT NOT NULL,   FOREIGN KEY (author_id) REFERENCES users (id)")



# cursor.execute("INSERT INTO posts VALUES(2, 'Second Post', 'My second post my friend!')")
db.commit()
ub.commit()
cb.commit()



@app.route("/")
def index():
    if "use" in session:
        user = session["use"]
        db = sqlite3.connect("posts-collection.db")
        db.row_factory =sqlite3.Row
        cursor = db.cursor()
        cursor.execute("select * from posts")
        posts = cursor.fetchall()
        return render_template('index.html', post=posts, name=user)
    else:
        return redirect(url_for('login')) 
    





@app.route("/add", methods=['POST','GET'])
def add():
    if "use" in session:
        user = session["use"]
    if request.method=='POST':
      title = request.form['title']
      body = request.form['body']
      db = sqlite3.connect("posts-collection.db")
      cursor = db.cursor()
      cursor.execute("insert into posts(TITLE,BODY,AUTHOR_ID) values (?,?,?)",(title,body,user))
      db.commit()
      return redirect(url_for("index"))
    return render_template("add.html")


      
@app.route("/edit/<int:id>", methods=['POST','GET'])
def edit(id):
   if "use" in session:
      user = session["use"]
   if request.method == 'POST':
       title = request.form['title']
       body = request.form['body']
       db = sqlite3.connect("posts-collection.db")
       cursor = db.cursor()
     
       cursor.execute("update posts set TITLE=?,BODY=? where ID=?",(title,body,id))
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
            id = request.form['id']
            username = request.form['username']          
            password=request.form['password']
            pw = bcrypt.generate_password_hash(password)
            ub = sqlite3.connect("users-collection.db")
            cur = ub.cursor()
            cur.execute("insert into users(EMAIL,USERNAME,PASSWORD,ID) values (?,?,?,?)",(email,username,pw,id))
            ub.commit()
            return redirect(url_for("index"))
     return render_template("register.html")   

            




           







@app.route('/login',methods=['POST','GET'])
def login():
     if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        ub = sqlite3.connect("users-collection.db")
        cur = ub.cursor()
        pw = bcrypt.generate_password_hash(password)
        bcrypt.check_password_hash(pw, password)
        cur.execute("select username,password FROM users where username = '+username+' and password='+pw+'")
        session['use'] = username
        ub.commit()
        return redirect(url_for("index"))
     return render_template("login.html")
    



@app.route("/logout")
def logout():
    session.pop("use", None)
    return render_template("login.html")




if __name__ == "__main__":
    app.run(debug=True)



