from flask import Blueprint, url_for, redirect, request, session, flash, render_template, jsonify
from main.models.dbModel import User, Community, Program, Subprogram
from main import db
from main import Form


dbModel_route = Blueprint('dbModel', __name__)

@dbModel_route.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check the username and password against the database (replace with actual database query)
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            # Store the user's ID in the session to keep them logged in
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dbModel.main'))
        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template("login.html")
@dbModel_route.route("/main")
def main():
     # Check if the user is logged in
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))

    return render_template("main.html")

@dbModel_route.route("/clear_session")
def clear_session():
    # Clear the user's session
    session.clear()
    
    # Redirect the user to the login page
    return redirect(url_for('dbModel.login'))

@dbModel_route.route("/result")
def programCSVresult():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))


#FOR USER CRUD

@dbModel_route.route("/manage_account")
def manage_account():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
     # Fetch all user records from the database
     
    all_data = User.query.all()
    return render_template("manage_account.html", users = all_data)

@dbModel_route.route("/add_account", methods=["POST"])
def add_account():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    if request.method == "POST":
        username = request.form.get("username")
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        password = request.form.get("password")
        role = request.form.get("role")
        # Check if the username already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
        else:
            # Create a new user without hashing the password
            new_user = User(username=username, firstname=firstname, lastname=lastname, password=password, role = role)

            try: 
                db.session.add(new_user)
                db.session.commit()
                flash('Account created successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while creating the account. Please try again.', 'error')
                # You may also want to log the exception for debugging purposes
    return redirect(url_for('dbModel.manage_account'))

@dbModel_route.route('/edit_account', methods=['POST'])
def edit_account():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    if request.method == 'POST':
        user_id = request.form.get('id')  # Get the user ID from the form
        new_username = request.form['new_username']
        new_firstname = request.form['new_firstname']
        new_lastname = request.form['new_lastname']
        new_password = request.form['new_password']
        new_role = request.form['new_role']
        
        
        # Query the user by ID
        user = User.query.get(user_id)
        
        if user:
            # Update the user's information
            user.username = new_username
            user.firstname = new_firstname
            user.lastname = new_lastname
            user.password = new_password
            user.role = new_role

            # Commit the changes to the database
            db.session.commit()
            flash('Account updated successfully!', 'success')
        else:
            flash('User not found. Please try again.', 'error')

        return redirect(url_for('dbModel.manage_account'))

@dbModel_route.route('/delete_account/<int:id>', methods=['GET'])
def delete_account(id):
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    user = User.query.get(id)

    if user:
        try:
            # Delete the user from the database
            db.session.delete(user)
            db.session.commit()
            flash('Account deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while deleting the account. Please try again.', 'error')
            # You may want to log the exception for debugging purposes
    else:
        flash('User not found. Please try again.', 'error')

    return redirect(url_for('dbModel.manage_account'))


##################  FOR COMMUNITY CRUD  #######################
programs = [
    {"id": 1, "program": "Literacy"},
    {"id": 2, "program": "Socio-economic"},
     {"id": 3, "program": "Environmental Stewardship"},
    {"id": 4, "program": "Socio-economic"},
     {"id": 5, "program": "Literacy"},
    {"id": 6, "program": "Socio-economic"},
     {"id":7, "program": "Literacy"},
    {"id": 8, "program": "Socio-economic"}
    # Add more programs
]

subprograms = [
    {"id": 1, "subprogram": "Sub-Literacy", "program_id": 1},
    {"id": 2, "subprogram": "Sub-Socio-economic", "program_id": 2},
    {"id": 3, "subprogram": "Sub-Environmental Stewardship", "program_id": 3},
     {"id": 4, "subprogram": "Sub-Health and Wellness", "program_id": 4},
    {"id": 5, "subprogram": "Sub-Cultural Enhancement", "program_id": 5},
    {"id": 6, "subprogram": "Sub-Values Formation", "program_id": 6},
     {"id": 7, "subprogram": "Sub-Disaster Management", "program_id": 7},
    {"id": 8, "subprogram": "Sub-Gender and Development", "program_id": 8}
    # Add more sub-programs
]





@dbModel_route.route("/manage_community")
def manage_community():
    form = Form()
    form.program.choices = [program.program for program in Program.query.all()]
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
     # Fetch all user records from the database
    all_data = Community.query.all()
    return render_template("community.html", community = all_data, form=form)

@dbModel_route.route("/subprogram/<get_subprogram>")
def subprogram(get_subprogram):
    sub = Subprogram.query.filter_by(program=get_subprogram).all()
    subArray = [program.subprogram for program in sub]  # Extract the subprograms from the query result
    return jsonify({'subprogram': subArray})



@dbModel_route.route("/add_community", methods=["POST"])
def add_community():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    if request.method == "POST":
        community = request.form.get("community")
        program = request.form.get("program")
        subprogram = request.form.get("subprogram")
        week = request.form.get("week")
        totalWeek = request.form.get("totalWeek")
        user = request.form.get("user")

        # Check if a community with the same values for 'community' and 'subprogram' already exists
        existing_community = Community.query.filter_by(community=community, subprogram=subprogram).first()

        if existing_community:
            flash('This combination of community and subprogram already exists. Please choose a different combination.', 'error')
        else:
            new_community = Community(community=community, program=program, subprogram=subprogram, week=week, totalWeek=totalWeek, user=user)

            try:
                db.session.add(new_community)
                db.session.commit()
                flash('Community created successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('An error occurred while creating the community. Please try again.', 'error')
                # You may also want to log the exception for debugging purposes

    return redirect(url_for('dbModel.manage_community'))



@dbModel_route.route('/edit_community', methods=['POST'])
def edit_community():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    if request.method == 'POST':
        user_id = request.form.get('id')  # Get the user ID from the form
        new_community = request.form['new_community']
        new_program = request.form['new_program']
        new_subprogram = request.form['new_subprogram']
        new_week= request.form['new_week']
        new_totalWeek = request.form['new_totalWeek']
        new_user = request.form['new_user']
        
        # Query the user by ID
        user = Community.query.get(user_id)
        
        if user:
            # Update the user's information
            user.community = new_community
            user.program = new_program
            user.subprogram = new_subprogram
            user.week = new_week
            user.totalWeek = new_totalWeek
            user.user = new_user

            # Commit the changes to the database
            db.session.commit()
            flash('Account updated successfully!', 'success')
        else:
            flash('User not found. Please try again.', 'error')

        return redirect(url_for('dbModel.manage_community'))

@dbModel_route.route('/delete_community/<int:id>', methods=['GET'])
def delete_community(id):
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))
    
    community = Community.query.get(id)
    if community:
        try:
            # Delete the user from the database
            db.session.delete(community)
            db.session.commit()
            flash('Account deleted successfully!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while deleting the account. Please try again.', 'error')
            # You may want to log the exception for debugging purposes
    else:
        flash('User not found. Please try again.', 'error')
    return redirect(url_for('dbModel.manage_community'))


