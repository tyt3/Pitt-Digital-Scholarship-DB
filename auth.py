"""Module for Auth"""
from flask import Blueprint

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return "<p>Login</<p>"

def logout():
    return "<p>Logout</p>"

def signup():
    return "<p>Sign Up</p>"