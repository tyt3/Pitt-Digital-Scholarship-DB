"""Module for Auth"""
from flask import Blueprint, render_template, request
from .database import db_session
from .models import User

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # if request.method == 'GET':
    #     pass

    # if request.method == 'POST':
    #   pass
    return render_template("sign-up.html", title="Sign Up | Pitt Digital Scholarship Database")

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("login.html", title="Login | Pitt Digital Scholarship Database")

@auth_bp.route('/logout')
def logout():
    return render_template("logout.html", title="Logout | Pitt Digital Scholarship Database")

@auth_bp.route('/account')
def account():
    return render_template("account.html", title="Account | Pitt Digital Scholarship Database")
