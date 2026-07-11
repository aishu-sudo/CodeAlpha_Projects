# CodeAlpha Secure Coding Review

## Project Overview
This project was developed as part of the CodeAlpha Cyber Security Internship (Task 3: Secure Coding Review).
The project demonstrates common security vulnerabilities in a Flask application and shows how they can be fixed using secure coding practices.

📄 Full technical write-up with before/after code, findings table, and screenshot evidence: [REPORT.md](./CodeAlpha_SecureCodingReview/Report.pdf)

---

## Technologies Used
- Python
- Flask
- SQLite
- bcrypt
- Bandit

---

## Project Structure
```
CodeAlpha_SecureCodingReview/
├── app.py              # Vulnerable application
├── app_fixed.py         # Fixed application
├── requirements.txt
├── .gitignore
├── bandit_report.txt
├── REPORT.md
├── screenshots/
└── README.md
```

---

## Vulnerabilities Found

### 1. Hardcoded Secret Key
**Severity:** Medium
**Issue:** The secret key was stored directly in the source code.
**Fix:** Loaded from an environment variable instead.

---

### 2. Plaintext Password Storage
**Severity:** High
**Issue:** Passwords were stored directly in the database as plain text.
**Fix:** Passwords are hashed using bcrypt before being stored.

---

### 3. SQL Injection
**Severity:** Critical
**Issue:** SQL queries were built using string concatenation, allowing login bypass (e.g. `' OR '1'='1`).
**Fix:** Parameterized queries were implemented.

---

### 4. Information Leakage
**Severity:** Medium
**Issue:** The application displayed the internal SQL query in the login error message.
**Fix:** Generic error messages are shown instead ("Invalid username or password.").

---

### 5. Command Injection
**Severity:** Critical
**Issue:** The application executed arbitrary system commands using:
```python
os.popen(cmd)
```
**Fix:** Restricted execution to a whitelist of safe commands (`date`, `whoami`) instead of allowing arbitrary input.

---

### 6. Debug Mode Enabled
**Severity:** Medium
**Issue:** The application was running with Flask debug mode on, exposing the interactive debugger and PIN.
**Fix:** Debug mode disabled; app bound to `127.0.0.1` only.

---

## Security Tools Used

### Bandit
Run:
```bash
bandit -r .
```
Generate report:
```bash
bandit -r . > bandit_report.txt
```

---

## How to Run

Create a virtual environment:
```bash
python -m venv venv
```
Activate:
```bash
venv\Scripts\activate
```
Install dependencies:
```bash
pip install -r requirements.txt
```
Run vulnerable version:
```bash
python app.py
```
Run secure version:
```bash
python app_fixed.py
```

Then open `http://127.0.0.1:5000` in your browser.

**Default login for testing:** `admin` / `admin123`

---

## Author
Jannatul Ferdaus Oishi.


## CodeAlpha Cyber Security Internship
