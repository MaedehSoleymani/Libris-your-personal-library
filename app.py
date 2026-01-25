from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response, session
import requests, random, sqlite3
from library import Library
from functools import wraps
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.secret_key = 'awesrdgtfhAWSEDTRYUIxCVGBHJ5247896532'

app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///sqlite.db"
db= SQLAlchemy(app)
class User(db.Model):
    id= db.Column (db.Integer, primary_key= True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__ (self):
        return self.username

with app.app_context():
    db.create_all()

USERNAME = "admin"
PASSWORD = "1234"

#-----------------------------------------------------
#non route functions

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "username" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

#-----------------------------------------------------

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/admin')
def admin():
    with sqlite3.connect ("db.sqlite") as con:
        c= con.cursor()
        c.execute("SELECT * FROM users")
        users= c.fetchall()
        return f"<h2>the users are:</h2><br>{users}"

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            with sqlite3.connect ("db.sqlite") as con:
                c= con.cursor()
                c.execute("SELECT * FROM users WHERE username=? AND password=?", (username,password))
                user= c.fetchone()
                if user:
                    flash (f"welcome {user[1]}","success")
                    session["username"]=username
                    return redirect(url_for("dashboard"))
                else:
                    return ("این نام کاربری وجود ندارد. آیا تمایل دارید اکانت بسازید؟")
    except:
        return "error"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("شما با موفقیت خارج شدید.", "success") 
    return redirect(url_for('login')) 

@app.route ("/register", methods=["POST","GET"])
def register():
    if request.method == "POST":
        username= request.form['username']
        password= request.form['password']
        user= User (username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect (url_for("login"))
    return render_template("register.html")

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        Library.load_books()
        books= Library.book_list
    except:
        return "<h1>ERORR</h1>"
    
    return render_template('dashboard.html', books=books)

@app.route ("/password_generator")
def password_generator():
    text= "123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM[]\';,./@#$%"
    password= ''.join(random.sample(text,12))
    return jsonify({"password": password})
    #return render_template ("password_generator.html", password=password)

@app.route ("/forgot_password")
def forgot_password():
    return render_template ("forgot_password.html")

@app.route ("/view_books")
@login_required
def view_books():
    Library.load_books()
    Library.show_books()

@app.route ("/add_book", methods=["GET", "POST"])
@login_required
def add_book():
    if request.method=="POST":
        title= request.form["title"]
        author= request.form["author"]
        pages= request.form["pages"]
        genre= request.form["genre"]
        status= request.form["status"]
        Library.load_books()
        Library.add_book (title, author, pages, genre, status)
        book = Library.book_list[-1]  # آخرین کتاب
        Library.save_books()
        flash("کتاب با موفقیت اضافه شد.", "success")
        return redirect(url_for("dashboard"))
    return render_template ("add_book.html")

@app.route("/delete_book")
@login_required
def delete_book():
    Library.load_books()
    Library.search_book()
    Library.delete_book()
    Library.save_books()

@app.route("/edit_book")
@login_required
def edit_book():
    Library.load_books()
    Library.search_book()

@app.route("/search_book")
@login_required
def search_book():
    Library.load_books()
    Library.search_book()

if __name__ == '__main__':
    create_db()
    app.run(debug=True)