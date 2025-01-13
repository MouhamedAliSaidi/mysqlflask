from flask import Flask, render_template, request, redirect, session, flash
import re
import mysql.connector

app = Flask(__name__)
app.secret_key = "supersecretkey"

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="users99"
)

cursor = db.cursor(dictionary=True)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

@app.route('/')
def index():
    return render_template('document.html')

@app.route('/register', methods=['POST'])
def register():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    print(f"Register Attempt: {first_name}, {last_name}, {email}, {password}, {confirm_password}")

    errors = []
    if not first_name or len(first_name) < 2 or not first_name.isalpha():
        errors.append("First name must be at least 2 characters and contain only letters.")
    if not last_name or len(last_name) < 2 or not last_name.isalpha():
        errors.append("Last name must be at least 2 characters and contain only letters.")
    if not EMAIL_REGEX.match(email):
        errors.append("Invalid email format.")
    if len(password) < 8 or not re.search(r"[A-Z]", password) or not re.search(r"\d", password):
        errors.append("Password must be at least 8 characters, include one uppercase letter, and one number.")
    if password != confirm_password:
        errors.append("Passwords do not match.")

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()
    if existing_user:
        errors.append("Email already exists.")

    if errors:
        for error in errors:
            flash(error, "error")
        return redirect('/')

    query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(query, (first_name, last_name, email, password))
        db.commit()
        print("User registered successfully!")
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        flash("An error occurred during registration. Please try again.", "error")
        return redirect('/')

    session['user_id'] = cursor.lastrowid
    flash("Registration successful!", "success")
    return redirect('/success')

@app.route('/success')
def success():
    if 'user_id' not in session:
        return redirect('/')
    
    cursor.execute("SELECT first_name FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()
    return render_template('success.html', first_name=user['first_name'])

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    print(f"Login Attempt: Email: {email}, Password: {password}")

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()

    if not user or user['password'] != password:
        flash("Invalid email or password.", "error")
        return redirect('/')

    session['user_id'] = user['id']
    flash("Login successful!", "success")
    return redirect('/success')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)


##tried correcting the code many times with  internet/ai, db seems bugged annd data nbot willing to get registered, wasted much time on this
