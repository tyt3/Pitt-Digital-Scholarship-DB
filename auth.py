"""Module for Auth"""
from flask import Blueprint, render_template, request

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    return "<p>Login</<p>"

@auth.route('/logout')
def logout():
    return "<p>Logout</p>"

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    # if request.method == 'GET':
    #     pass
  
    # if request.method == 'POST':
    #   pass
    return "<p>Sign Up</p>"