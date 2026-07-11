import sqlite3
from flask import Flask, request, g, redirect, url_for

app = Flask(__name__)


app.secret_key = "supersecret123"      

DATABASE = "users.db"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def init_db():
    db = get_db()
    db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT
        )
    """)
   
    db.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'admin123')")
    
   


@app.route("/")
def home():
    return '''
    <h1>Welcome to the Notes App</h1>
    <a href="/login">Go to Login</a>
    '''


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        
        username = request.form.get("username")
        password = request.form.get("password")


        db = get_db()
        
        query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"

        
        cursor = db.execute(query)
        user = cursor.fetchone()

        if user:
            return redirect(url_for("dashboard", user=username))
        else:
            
            return f"Login failed. Query used: {query}", 401
        

    return """
        <form method="post">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit" value="Login">
        </form>
    """


@app.route("/dashboard")
def dashboard():
    user = request.args.get("user")
    return f"Welcome, {user}! This is your dashboard."


@app.route("/run", methods=["POST"])
def run_command():
  
    cmd = request.form.get("cmd")
    import os
    result = os.popen(cmd).read()
    return f"<pre>{result}</pre>"



if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(debug=True, host="0.0.0.0")
   