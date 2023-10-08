from flask import Blueprint, redirect, url_for

index_route = Blueprint('index', __name__)

@index_route.route("/", methods=["GET", "POST"])
def index():
    # Assuming you want to redirect to the login route in dbModelRoute.py
    return redirect(url_for('dbModel.login'))
