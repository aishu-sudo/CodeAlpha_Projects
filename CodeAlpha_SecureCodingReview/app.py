import sqlite3
from flask import Flask, request, g, redirect, url_for

app = Flask(__name__)

# --- VULNERABILITY 1: Hardcoded secret key ---
app.secret_key = "supersecret123"      
# The secret key is stored directly in the source code. If someone gets access to our GitHub repository, anyone can steal it and potentially forge sessions.

# app.secret_key = os.getenv("SECRET_KEY")-----fix
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
    # --- VULNERABILITY 2: Plaintext password storage ---
    db.execute("INSERT OR IGNORE INTO users (id, username, password) VALUES (1, 'admin', 'admin123')")
    
    # Passwords should never be stored in plain text. If the database leaks, attackers immediately know users' passwords.
    # Use bcrypt:hashed = bcrypt.hashpw("admin123".encode(),bcrypt.gensalt())  db.commit()


@app.route("/")
def home():
    return "Welcome to the Notes App. Go to /login"


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # --- VULNERABILITY 7: Missing input validation ---
        username = request.form.get("username")
        password = request.form.get("password")
# A user can send:
# Empty values
# Very large inputs
# Special characters without any checks

        # if not username or not password:
        #     return "Invalid input"

        db = get_db()
        # --- VULNERABILITY 3: SQL Injection (string concatenation, not parameterized) ---
        query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
        # An attacker can bypass the login.Because '1'='1' is always true, the attacker may log in without the real password.
#         cursor = db.execute(
#     "SELECT * FROM users WHERE username = ? AND password = ?",
#     (username, password)
# )
        
        cursor = db.execute(query)
        user = cursor.fetchone()

        if user:
            return redirect(url_for("dashboard", user=username))
        else:
            # --- VULNERABILITY 4: Verbose error leaking internals ---
            return f"Login failed. Query used: {query}", 401
        # Attackers can see your SQL query and learn how the database works.
        # return "Invalid username or password.", 401

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
# Anyone can access the dashboard.
# @app.route("/dashboard")
# def dashboard():
#     if "user" not in session:
#         return redirect("/login")

#     return "Welcome to dashboard"

@app.route("/run", methods=["POST"])
def run_command():
    # --- VULNERABILITY 5: Command injection via unsafe eval/os.system-style pattern ---
    cmd = request.form.get("cmd")
    import os
    result = os.popen(cmd).read()
    return f"<pre>{result}</pre>"
# allowed_commands = ["date", "whoami"]


if __name__ == "__main__":
    with app.app_context():
        init_db()
    # --- VULNERABILITY 6: Debug mode enabled (exposes interactive debugger) ---
    app.run(debug=True, host="0.0.0.0")
    # Debug mode exposes stack traces and debugging tools.
    # app.run(host="127.0.0.1", debug=False)