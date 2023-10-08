from flask import Blueprint, url_for, redirect, request, session, flash, render_template
from main.models.dbModel import User
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


@dbModel_route.route("/main", methods=["GET", "POST"])
def main():
     # Check if the user is logged in
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))

    return render_template("main.html")

@dbModel_route.route("/clear_session", methods=["POST"])
def clear_session():
    # Clear the user's session
    session.clear()

    # Respond with a JSON indicating success
    return {"success": True}

@dbModel_route.route("/result", methods=["GET", "POST"])
def programCSVresult():
    if 'user_id' not in session:
        flash('Please log in first.', 'error')
        return redirect(url_for('dbModel.login'))