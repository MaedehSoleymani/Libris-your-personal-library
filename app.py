from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests, random, sqlite3

app = Flask(__name__)
app.secret_key = 'mysecretkey'

USERNAME = "admin"
PASSWORD = "1234"

def create_db():
    with sqlite3.connect ("db.sqlite") as con:
        c= con.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR (32) NOT NULL UNIQUE,
        password VARCHAR (62) NOT NULL)
        """)
        con.commit()

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
                    return redirect(url_for('dashboard'))
    except:
        return "error"
    return render_template('login.html')

@app.route ("/register", methods=["POST","GET"])
def register():
    if request.method == "POST":
        username= request.form['username']
        password= request.form['password']
        with sqlite3.connect ("db.sqlite") as con:
            c= con.cursor()
            c.execute("INSERT INTO users (username, password) VALUES (?,?)", (username,password))
            con.commit()
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
    return jsonify({"password": password})
    #return render_template ("password_generator.html", password=password)

@app.route ("/forgot_password")
def forgot_password():
    return render_template ("forgot_password.html")

if __name__ == '__main__':
    create_db()
    app.run(debug=True)