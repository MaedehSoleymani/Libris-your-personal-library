from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import requests, random
from library import Library
from functools import wraps
from flask_sqlalchemy import SQLAlchemy 
from models import db,Book,User
from flask_mail import Mail, Message
import config
from emails.reset_password_email import reset_password_email

app = Flask(__name__)
app.secret_key = 'awesrdgtfhAWSEDTRYUIxCVGBHJ5247896532'
app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///sqlite.db"

app.config.from_object(config.Config)
mail=Mail(app)

db.init_app(app)

with app.app_context():
    db.create_all()

email = "admin"
PASSWORD = "1234"

#-----------------------------------------------------
#route functions

@app.route("/reset_db")
def reset_db():
    try:
        with app.app_context():
            db.drop_all()
            db.create_all()
            admin = User(email="admin")
            admin.password= "1234"
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
            email = request.form.get('email')
            password = request.form.get('password')
            user= User.query.filter_by(email=email).first()
            if user and user.verify_password(password):
                session['email'] = email
                print(f"user email: {email} - Password hash:{user.password_hash}")
                flash ("با موفقیت وارد شدید.","success")
                return redirect(url_for("dashboard"))
            elif user and not user.verify_password(password):
                flash ("رمز عبور اشتباه است.", "error")
                return redirect(url_for("dashboard"))
            elif not user:
                flash ("حساب کاربری‌ای با این ایمیل وجود ندارد.", "error")
                return redirect(url_for("dashboard"))
    except Exception as e:
        return f"Error: {e}"
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    flash("شما با موفقیت خارج شدید.", "success") 
    return redirect(url_for('login')) 

@app.route ("/register", methods=["POST","GET"])
def register():
    if request.method == "POST":
        email= request.form.get("email")
        password= request.form.get("password")
        if len(password)<5:
            flash("رمز عبور باید حداقل 5 کاراکتر باشد", "error")
            return render_template("register.html")
        existing_user= User.query.filter_by (email=email).first()
        if existing_user:
            flash ("حساب کاربری از قبل با این ایمیل وجود دارد.", "error")
            return render_template("register.html")
        new_user= User (email=email)
        new_user.password= password
        print(f"user email: {email} - Password hash:{new_user.password_hash}")
        db.session.add(new_user)
        db.session.commit()
        flash ("حساب کاربری با موفقیت ساخته شد.", "success")
        return redirect (url_for("login"))
    return render_template("register.html")

@app.route ("/password_generator")
def password_generator():
    text= "123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM[]\';,./@#$%"
    password= ''.join(random.sample(text,12))
    return jsonify({"password": password})

@app.route ('/reset_password<token>')
def reset_password(token):
    user= User.query.filter_by(reset_token=token).first()
    if not user:
        flash ("لینک منقضی شده.","error")
        return render_template('forgot password.html')
    else:
        return render_template('reset_password.html',token=token)

@app.route ("/forgot_password", methods= ["POST", "GET"])
def forgot_password():
    if request.method == "POST":
        email= request.form.get("email")
        user= User.query.filter_by(email=email).first()
        if user:
            print(f"ارسال ایمیل به: {email}")
            token= user.generate_reset_token()
            db.session.commit()
            reset_link= url_for ('reset_password', token=token, )
            msg= Message (
                subject= "لیبریس - تغییر رمز عبور",
                recipients=[email],
                html=reset_password_email(reset_link))
            mail.send(msg)
            flash ("ایمیل بازیابی رمز عبور با موفقیت ارسال شد. لطفا ایمیل خود را بررسی کرده و بر روی لینک کلیک کنید.","success")
            return render_template('forgot_password.html')
        else:
            flash ("حساب کاربری‌ای با این ایمیل وجود ندارد.","error")
            return render_template('forgot_password.html')
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
#profile routes

@app.route ('/profile')
@login_required
def profile():
    print ("current email:", session.get('email'))
    user= User.query.filter_by (email=session['email']).first()
    return render_template('profile.html',user=user)

@app.route ('/delete_account')
@login_required
def delete_account():
    pass

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
        title= request.form.get("title")
        author= request.form.get("author")
        pages= request.form.get("pages")
        genre= request.form.get("genre")
        status= request.form.get("status")
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
    title= request.form.get("title")
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