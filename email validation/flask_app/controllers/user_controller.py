from flask import render_template, request, redirect, url_for
from flask_app import app  # Importing the app instance from __init__.py
from flask_app.models.users import User

@app.route('/')
def home():
    return redirect(url_for('read'))

@app.route('/read')
def read():
    users = User.get_all()
    return render_template('home.html', users=users)

@app.route('/create')
def create():
    return render_template('new.html')

@app.route('/process', methods=['POST'])
def process():
    first_name = request.form['name']
    last_name = request.form['lastname']
    email = request.form['email']
    User.create(first_name, last_name, email)
    return redirect(url_for('read'))

@app.route('/edit/<int:user_id>')
def edit(user_id):
    user = User.get_by_id(user_id)
    if not user:
        return "User not found", 404
    return render_template('edit.html', user=user)

@app.route('/update/<int:user_id>', methods=['POST'])
def update(user_id):
    user = User.get_by_id(user_id)
    if not user:
        return "User not found", 404
    User.update(
        user_id,
        request.form['name'],
        request.form['lastname'],
        request.form['email']
    )
    return redirect(url_for('read'))

@app.route('/delete/<int:user_id>')
def delete(user_id):
    User.delete(user_id)
    return redirect(url_for('read'))

@app.route('/user/<int:user_id>')
def user_details(user_id):
    user = User.get_by_id(user_id)
    if not user:
        return "User not found", 404
    return render_template('user.html', user=user)
