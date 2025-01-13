from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/dojos_ninjas_111'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Dojo(db.Model):
    __tablename__ = 'dojos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    ninjas = db.relationship('Ninja', backref='dojo')

class Ninja(db.Model):
    __tablename__ = 'ninjas'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    dojos_id = db.Column(db.Integer, db.ForeignKey('dojos.id'), nullable=False)

@app.route('/')
def home():
    dojos = Dojo.query.all()
    return render_template('dojos.html', dojos=dojos)

@app.route('/process', methods=['POST'])
def process_dojo():
    dojo_name = request.form['name']
    if dojo_name:
        new_dojo = Dojo(name=dojo_name)
        db.session.add(new_dojo)
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/ninjas', methods=['GET', 'POST'])
def ninjas_page():
    if request.method == 'POST':
        dojos_id = request.form['dojo']
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        age = request.form['age']

        if dojos_id and first_name and last_name and age:
            new_ninja = Ninja(
                first_name=first_name,
                last_name=last_name,
                age=int(age),
                dojos_id=int(dojos_id)
            )
            db.session.add(new_ninja)
            db.session.commit()
        return redirect(url_for('home'))

    dojos = Dojo.query.all()
    return render_template('ninjas.html', dojos=dojos)

@app.route('/dojo/<int:dojo_id>')
def dojo_ninjas(dojo_id):
    dojo = Dojo.query.get_or_404(dojo_id)
    ninjas = dojo.ninjas
    return render_template('dojo_ninjas.html', dojo_name=dojo.name, ninjas=ninjas)

if __name__ == '__main__':
    app.run(debug=True)
