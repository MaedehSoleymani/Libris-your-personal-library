from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, make_response, session
import requests, random, sqlite3
from library import Library
from functools import wraps
from flask_sqlalchemy import SQLAlchemy 
from models import db,Book,User

app = Flask(__name__)
app.secret_key = 'awesrdgtfhAWSEDTRYUIxCVGBHJ5247896532'
app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///sqlite.db"

db.init_app(app)

with app.app_context():
    db.create_all()

email = "admin"
PASSWORD = "1234"

@app.route("/reset_db")
def reset_db():
    try:
        with app.app_context():
            db.drop_all()
            db.create_all()
            admin = User(email="admin", password="1234")
            db.session.add(admin)
            db.session.commit()
        return "Database has been reset successfully. Admin user created."
    except Exception as e:
        return f"Error resetting database: {e}"

#-----------------------------------------------------
#non route functions

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "email" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapper

#-----------------------------------------------------
#admin routes

@app.route('/admin')
def admin():
    users=User.query.all()
    return render_template("admin.html",users=users)
    
@app.route('/edit_users')
def edit_users():
    user= User.query.filter_by(email="").first()
    user.email=""
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/delete_user')
def delete_user():
    user=User.query.filter_by(email="").first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin'))

#-----------------------------------------------------
#home routes

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            print("Form keys:", list(request.form.keys()))
            print("Form data:", request.form)
            email = request.form.get('email')
            password = request.form.get('password')
            print (email,password)
            user= User.query.filter_by(email=email,password=password).first()
            print (user)
            if user:
                session['email'] = email
                flash (f"welcome {user}","success")
                return redirect(url_for("dashboard"))
            else:
                return ("این نام کاربری وجود ندارد. آیا تمایل دارید اکانت بسازید؟")
    except Exception as e:
        return f"Error: {e}"
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("شما با موفقیت خارج شدید.", "success") 
    return redirect(url_for('login')) 

@app.route ("/register", methods=["POST","GET"])
def register():
    if request.method == "POST":
        email= request.form['email']
        password= request.form['password']
        print (email,password)
        print("Form keys:", list(request.form.keys()))
        print("Form data:", request.form)
        new_user= User (email=email, password=password)
        print (new_user)
        db.session.add(new_user)
        db.session.commit()
        return redirect (url_for("login"))
    return render_template("register.html")

@app.route ("/password_generator")
def password_generator():
    text= "123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM[]\';,./@#$%"
    password= ''.join(random.sample(text,12))
    return jsonify({"password": password})

@app.route ("/forgot_password")
def forgot_password():
    return render_template ("forgot_password.html")

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@app.route ('/tos')
def tos():
    return render_template('tos.html')

@app.route ('/privacy_policy')
def privacy_policy():
    return render_template('privacy_policy.html')

@app.route ('/faq')
def faq():
    return render_template ('faq.html')

#-------------------------------------------
#dashboard routes

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        Library.load_books()
        books= Library.book_list
    except:
        return "<h1>ERORR</h1>"
    
    return render_template('dashboard.html', books=books)

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
    title= request.form["title"]
    Library.load_books()
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
    app.run(debug=True)