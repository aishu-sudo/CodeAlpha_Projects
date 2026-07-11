import os
import sqlite3
import bcrypt
from flask import Flask, request, g, redirect, url_for, session

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY", os.urandom(24).hex())
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
            username TEXT UNIQUE,
            password TEXT
        )
    """)
    hashed = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt())
    db.execute(
        "INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', ?)",
        (hashed,)
    )
    db.commit()


@app.route("/")
def home():
    return "Welcome to the Notes App. Go to /login"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "Invalid input"

        db = get_db()
        cursor = db.execute(
            "SELECT password FROM users WHERE username = ?",
            (username,)
        )
        row = cursor.fetchone()

        
        if row and bcrypt.checkpw(password.encode(), row[0]):
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return "Invalid username or password.", 401

    return """
        <form method="post">
            Username: <input name="username"><br>
            Password: <input name="password" type="password"><br>
            <input type="submit" value="Login">
        </form>
    """


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return f"Welcome to your dashboard, {session['user']}!"


@app.route("/run", methods=["POST"])
def run_command():
    if "user" not in session:
        return redirect("/login")

    allowed_commands = {"date": ["date"], "whoami": ["whoami"]}
    choice = request.form.get("cmd")

    if choice not in allowed_commands:
        return "Command not allowed.", 400

    import subprocess
    result = subprocess.run(allowed_commands[choice], capture_output=True, text=True)
    return f"<pre>{result.stdout}</pre>"


if __name__ == "__main__":
    with app.app_context():
        init_db()
    app.run(host="127.0.0.1", debug=False)