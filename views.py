"""Module for Views"""
from flask import Blueprint, render_template, request

views = Blueprint('views', __name__)

"""Function to Show Homepage"""
@views.route('/')
def home():
    return render_template("index.html", title="Pitt Digital Scholarship Database")
