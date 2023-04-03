"""Module for Auth"""
from flask import Blueprint, render_template, request
from models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return "<h1>Login</h1>"

@auth.route('/logout')
def logout():
    return "<h1>Logout</h1>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # if request.method == 'GET':
    #     pass
  
    # if request.method == 'POST':
    #   pass
    return "<h1>Sign Up</h1>"