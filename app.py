from flask import Flask, render_template, request, redirect, url_for, flash
import requests, random, sqlite3

app = Flask(__name__)
app.secret_key = 'mysecretkey'

USERNAME = "admin"
PASSWORD = "1234"

def create_db():
    con= sqlite3.connect ("db.sqlite")
    c= con.cursor()
    c.execute("")
    con.commit()
    con.close()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            flash('ورود موفقیت‌آمیز بود!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('نام کاربری یا رمز عبور اشتباه است.', 'danger')
    return render_template('login.html')

@app.route ("/register", methods=["POST","GET"])
def register():
    if request.method == "POST":
        username= request.form['username']
        password= request.form['password']
        con= sqlite3.connect ("db.sqlite")
        c= con.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?,?)", (username,password))
        con.commit()
        con.close()
    return render_template("register.html")

@app.route('/dashboard')
def dashboard():
    try:
        response = requests.get('https://jsonplaceholder.typicode.com/posts?userId=1')
        posts = response.json()  
    except:
        posts = []
        flash('خطا در دریافت داده از سرور!', 'danger')
    
    return render_template('dashboard.html', posts=posts)

@app.route ("/password_generator")
def password_generator():
    text= "123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM[]\';,./@#$%"
    password= ''.join(random.sample(text,12))
    return render_template ("password_generator.html", password=password)

@app.route ("/forgot_password")
def forgot_password():
    return render_template ("forgot_password.html")

if __name__ == '__main__':
    app.run(debug=True)