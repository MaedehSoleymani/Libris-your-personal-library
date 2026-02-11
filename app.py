from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import requests, random
from functools import wraps
from flask_sqlalchemy import SQLAlchemy 
from models import db,Book,User,ContactMessage
from flask_mail import Mail, Message
import config
from emails.reset_password_email import reset_password_email
from datetime import datetime, timezone

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

@app.route("/user_reset_db")
def user_reset_db():
    try:
        with app.app_context():
            User.__table__.drop(db.engine)
            User.__table__.create(db.engine)
            admin = User(email="admin")
            admin.password= "1234"
            db.session.add(admin)
            db.session.commit()
        return "Database has been reset successfully. Admin user created."
    except Exception as e:
        return f"Error resetting database: {e}"

@app.route("/book_reset_db")
def book_reset_db():
    try:
        with app.app_context():
            Book.__table__.drop(db.engine)
            Book.__table__.create(db.engine)
        return "Database has been reset successfully."
    except Exception as e:
        return f"Error resetting database: {e}"
    
@app.route("/ContactMessage_reset_db")
def ContactMessage_reset_db():
    try:
        with app.app_context():
            ContactMessage.__table__.drop(db.engine)
            ContactMessage.__table__.create(db.engine)
        return "Database has been reset successfully."
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
    
@app.route('/show_message')
def show_message():
    messages= ContactMessage.query.all()
    return render_template ('show_message.html', messages=messages)

@app.route('/delete_message')
def delete_message():
    return redirect (url_for('show_message'))

@app.route('/edit_users/int:<user_id>')
def edit_users(user_id):
    user= User.query.get_or_404(user_id).first()
    user.email=request.form.get('new_email')
    db.session.commit()
    return redirect(url_for('admin'))

@app.route('/delete_user/<int:user_id>')
def delete_user(user_id):
    user=User.query.get_or_404(user_id).first()
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
                flash ("با موفقیت وارد شدید.","success")
                return redirect(url_for("dashboard"))
            elif user and not user.verify_password(password):
                flash ("رمز عبور اشتباه است.", "error")
                return redirect(url_for("login"))
            elif not user:
                flash ("حساب کاربری‌ای با این ایمیل وجود ندارد.", "error")
                return redirect(url_for("login"))
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
            return redirect (url_for('register'))
        existing_user= User.query.filter_by (email=email).first()
        if existing_user:
            flash ("حساب کاربری از قبل با این ایمیل وجود دارد.", "error")
            return redirect (url_for('register'))
        new_user= User (email=email)
        new_user.password= password
        db.session.add(new_user)
        db.session.commit()
        flash ("حساب کاربری با موفقیت ساخته شد.", "success")
        return redirect (url_for('login'))
    return render_template('register.html')

@app.route ("/password_generator")
def password_generator():
    text= "123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM[]\';,./@#$%"
    password= ''.join(random.sample(text,12))
    return jsonify({"password": password})

@app.route ('/reset_password/<token>', methods= ['GET', 'POST'])
def reset_password(token):
    try:
        user= User.query.filter_by(reset_token=token).first()
        if not user:
            flash ("لینک بازیابی نامعتبر است.","error")
            return redirect (url_for('change_password'))
        elif user.reset_token_expire < datetime.now():
            flash ("لینک منقضی شده.","error")
            return redirect (url_for('change_password'))
        if request.method=='POST':
            new_password= request.form.get('new_password')
            confirm_password= request.form.get('confirm_password')
            if len(new_password)<5:
                flash ("رمز عبور باید حداقل 5 کاراکتر باشد.","error")
            if new_password!=confirm_password:
                flash ("رمز عبور و تکرار آن یکسان نیستند.","error")
            else:
                user.password= new_password
                user.reset_token= None
                user.reset_token_expire= None
                db.session.commit()
                flash("رمز عبور با موفقیت تغییر یافت.","success")
                return redirect (url_for('login'))
            
        return render_template ('reset_password.html')
    except Exception as e:
        return f"error {e}"

@app.route ("/change_password", methods= ["POST", "GET"])
def change_password():
    if request.method == "POST":
        email= request.form.get("email")
        user= User.query.filter_by(email=email).first()
        if user:
            token= user.generate_reset_token()
            db.session.commit()
            reset_link= url_for ('reset_password', token=token, )
            reset_link = url_for('reset_password', token=token, _external=True)
            msg= Message (
                subject= "لیبریس - تغییر رمز عبور",
                recipients=[email],
                html=reset_password_email(reset_link))
            mail.send(msg)
            flash ("ایمیل بازیابی رمز عبور با موفقیت ارسال شد. لطفا ایمیل خود را بررسی کرده و بر روی لینک کلیک کنید.","success")
            return redirect (url_for('change_password'))
        else:
            flash ("حساب کاربری‌ای با این ایمیل وجود ندارد.","error")
            return redirect (url_for('change_password'))
    return render_template ("change_password.html")        

@app.route('/contact_us', methods=['POST','GET'])
def contact_us():
    try:
        if request.method=='POST':
            if 'email' not in session:
                flash ("برای ثبت پیام باید ابتدا وارد حساب کاربری خود شوید.","error")
                return redirect (url_for('login'))
            else:
                message= request.form.get('message')
                email=session.get('email')
                created_time=datetime.now()
                new_message= ContactMessage (message=message,email=email,created_time=created_time)
                print (message)
                db.session.add(new_message)
                print("addede")
                db.session.commit()
                print("commited")
                flash ("پیام شما با موفقیت ثبت شد.","success")
        return render_template('contact_us.html')
    except Exception as e:
        return f"error {e}"

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
    books=Book.query.all()
    return render_template('dashboard.html', books=books)

@app.route ("/add_book", methods=["GET", "POST"])
@login_required
def add_book():
    if request.method=="POST":
        title= request.form.get("title")
        author= request.form.get("author")
        pages= request.form.get("pages")
        genre= request.form.get("genre")
        status= request.form.get("status")
        book = Book (title=title,author=author,pages=pages,genre=genre,status=status)
        db.session.add(book)
        db.session.commit()
        flash("کتاب با موفقیت اضافه شد.", "success")
        return redirect(url_for("dashboard"))
    return render_template ("add_book.html")

@app.route("/delete_book/<int:book_id>")
@login_required
def delete_book(book_id):
    book= Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    flash("کتاب با موفقیت حذف شد.","success")
    return redirect(url_for('dashboard'))

@app.route("/edit_book/<int:book_id>", methods=['POST','GET'])
@login_required
def edit_book(book_id):
    book= Book.query.get_or_404(book_id)
    if request.method=='POST':
        book.title= request.form.get("title")
        book.author= request.form.get("author")
        book.pages= request.form.get("pages")
        book.genre= request.form.get("genre")
        book.status= request.form.get("status")
        db.session.commit()
        flash("کتاب با موفقیت ویرایش شد.", "success")
        return redirect(url_for("dashboard"))
    return render_template ('edit_book.html', book=book)

@app.route("/search_book")
@login_required
def search_book():
    query= request.args.get('q','').strip()
    if query:
        book=Book.query.filter(Book.title.ilike(f'%{query}%')).all()
    else:
        books=[]
    return render_template('dashboard.html', book=book, search_query=query)

if __name__ == '__main__':
    app.run(debug=True)