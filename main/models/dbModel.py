from main import db, app

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Coordinator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    
    # Coordinator can manage multiple programs
    programs = db.relationship('Program', backref='coordinator', lazy=True)

class Program(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    
    # Program is managed by a coordinator
    coordinator_id = db.Column(db.Integer, db.ForeignKey('coordinator.id'), nullable=False)
    
    # Program can have multiple subprograms
    subprograms = db.relationship('Subprogram', backref='program', lazy=True)
    
    # Community can implement multiple programs (up to 3)
    communities = db.relationship('CommunityProgram', backref='program', lazy=True)

class Subprogram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    
    # Subprogram is associated with a program
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'), nullable=False)

class Community(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    
    # Community can implement multiple programs (up to 3)
    programs = db.relationship('CommunityProgram', backref='community', lazy=True)

class CommunityProgram(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    community_id = db.Column(db.Integer, db.ForeignKey('community.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('program.id'), nullable=False)


# Create the database tables
with app.app_context():
    db.create_all()


def create_tables_and_insert_user():
    new_user = User(username='admin', password='123')
    db.session.add(new_user)
    db.session.commit()

@app.route('/dbApp')
def initialize_database():
    create_tables_and_insert_user()
    return 'Database tables created, and a new user inserted.'


