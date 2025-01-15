from flask import Flask, render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL
import re

# Initialize Flask App
app = Flask(__name__)
app.secret_key = 'super_secret_key'
bcrypt = Bcrypt(app)

# Configure MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'recipes'
mysql = MySQL(app)

# Regular Expression for Email Validation
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    confirm_pw = request.form['confirm_pw']

    # Validations
    if len(first_name) < 2 or len(last_name) < 2:
        flash('First and Last name must be at least 2 characters', 'register')
        return redirect('/')
    if not EMAIL_REGEX.match(email):
        flash('Invalid email format', 'register')
        return redirect('/')
    if password != confirm_pw:
        flash('Passwords do not match', 'register')
        return redirect('/')

    # Check if email already exists
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", [email])
    user = cur.fetchone()
    if user:
        flash('Email already registered', 'register')
        return redirect('/')

    # Hash password and save user
    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    cur.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
                (first_name, last_name, email, pw_hash))
    mysql.connection.commit()
    cur.close()
    flash('Registration successful! Please log in.', 'register')
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", [email])
    user = cur.fetchone()
    cur.close()

    if not user or not bcrypt.check_password_hash(user[4], password):
        flash('Invalid login credentials', 'login')
        return redirect('/')

    session['user_id'] = user[0]
    session['user_name'] = user[1]
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('You must be logged in to view this page', 'login')
        return redirect('/')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM recipes WHERE user_id = %s OR is_public = 1", [session['user_id']])
    recipes = cur.fetchall()
    cur.close()

    return render_template('dashboard.html', recipes=recipes)

@app.route('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        flash('You must be logged in to add a recipe', 'login')
        return redirect('/')
    return render_template('new_recipe.html')

@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        flash('You must be logged in to perform this action', 'login')
        return redirect('/')

    name = request.form['name']
    description = request.form['description']
    instructions = request.form['instructions']
    date_made = request.form['date_made']
    under_30 = request.form['under_30']

    if len(name) < 3 or len(description) < 3 or len(instructions) < 3:
        flash('All fields must be at least 3 characters long', 'recipe')
        return redirect('/recipes/new')

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO recipes (name, description, instructions, date_made, under_30, user_id) VALUES (%s, %s, %s, %s, %s, %s)",
                (name, description, instructions, date_made, under_30, session['user_id']))
    mysql.connection.commit()
    cur.close()
    return redirect('/dashboard')

@app.route('/recipes/<int:recipe_id>')
def view_recipe(recipe_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM recipes WHERE id = %s", [recipe_id])
    recipe = cur.fetchone()
    cur.close()
    return render_template('view_recipe.html', recipe=recipe)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
