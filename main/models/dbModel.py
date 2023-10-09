from main import db, app
from flask import render_template

class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community = db.Column(db.String(255))
    program = db.Column(db.String(255), nullable=False)
    subprogram = db.Column(db.String(255), nullable=False)
    week = db.Column(db.Integer, nullable=True)
    totalWeek = db.Column(db.Integer, nullable=False)
    user =db.Column(db.String(255), unique=True, nullable=False)
    

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    firstname = db.Column(db.String(255), nullable=False)
    lastname = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)

class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(255), unique=True, nullable=False)

class Subprogram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program = db.Column(db.String(255), nullable=False)
    subprogram = db.Column(db.String(255), nullable=False)


# Create the database tables
with app.app_context():
    db.create_all()

def create_tables_and_insert_subprogram():
    new_subprogram = Subprogram(program='Literacy', subprogram='Literacy2')
    db.session.add(new_subprogram)
    db.session.commit()

@app.route('/db')
def initialize_database():
    create_tables_and_insert_subprogram()
    return 'Database tables created, and a new user inserted.'

@app.route('/test')

def display_subprograms():
    # Query all subprogram records from the database
    subprograms = Subprogram.query.all()
    
    # Render a template and pass the subprograms data to it
    return render_template('test.html', subprograms=subprograms)



