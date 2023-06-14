"""Module for Auth"""
import re
from datetime import datetime
from flask import Blueprint, render_template, request, redirect,  url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import select
from passlib.hash import sha256_crypt
import secrets
from .database import db_session
from .models import User, Permission
from .add import add_user


auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        flash("You are already signed up.", category="error")
        return redirect(url_for('views_bp.index'))
    
    if request.method == "POST":
        # Get form input
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        user_name = request.form.get('user_name')
        email = request.form.get('email')
        password = request.form.get('password')
        password_conf = request.form.get('password_conf')
        admin_code = request.form.get('admin_code')

        # Check if user email is already in the database
        user = User.query.filter_by(email=email).first()
        if user :
            flash("This email is already registered.", category='error')
        else:
            # Check that username is unique
            # Check that email is from the Pitt domain
            regex = '^[a-z0-9]+@pitt.edu$'
            if not re.search(regex, email):
                flash("Please register using your Pitt (@pitt.edu) email address.", category='error')
            else:
                # Check for valid password
                if (len(password) < 8):
                    flash("Password must be at least 8 characters.", category='error')
                elif (len(password) > 16):
                    flash("Password must be less than 16 characters.", category='error')
                elif not re.search("[a-z]", password):
                    flash("Password must contain at least 1 lowercase alphabet.", category='error')
                elif not re.search("[A-Z]", password):
                    flash("Password must contain at least 1 uppercase alphabet.", category='error')
                elif not re.search("[0-9]", password):
                    flash("Password must contain at least 1 number.", category='error')
                elif not re.search("[_@()*&^%#<>,$!]", password):
                    flash("Password must contain at least 1 special character.", category='error')
                elif password != password_conf:
                    flash("Passwords do not match.", category='error')
                else:
                    # Check for valid admin code
                    p_level = permission_id = 1
                    if admin_code:
                        # Get all permission codes
                        permission_codes = db_session.execute(
                            select(Permission.permission_code)).all()
                        # Check for a matching permission code
                        for code in permission_codes:
                            if sha256_crypt.verify(admin_code, code[0]):
                                permission_id_result = db_session.execute(
                                    select(Permission.permission_id).where(
                                    Permission.permission_code == code[0])).first()
                                permission_id = permission_id_result[0]
                                break
                        # Check if given permission code, if any, was matched
                        # and update permission level accordingly
                    if permission_id or not admin_code:
                        p_level = permission_id
                        # Generate API key
                        api_key = secrets.token_hex(16)
                        # Create new user object
                        new_user = add_user(first_name=first_name,
                                            last_name=last_name,
                                            user_name=user_name,
                                            email=email,
                                            password=sha256_crypt.hash(password),
                                            api_key=api_key,
                                            permission_level=p_level)
                        
                        if new_user:
                            # Log new user in
                            login_user(new_user)

                        # Redirect to login page
                        return redirect(url_for('views_bp.index'))
                    else:
                        flash("Please enter a valid Administrator code.", category='error')
    
    if current_user.is_authenticated:
        current_user.set_permissions()
        
    return render_template("sign-up.html", 
                           title="Sign Up",
                           user = current_user)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", category="error")
        return redirect(url_for('views_bp.index'))
    
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        remember = True if request.form.get('remember') else False

        # Check if the user actually exists
        if user:
            # Confirm that password matches
            if sha256_crypt.verify(password, user.user_password):
                user.last_login = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                db_session.commit()
                login_user(user, remember=remember)
                user.set_permissions()
                #flash("Login successful!", category="success")
                return render_template("index.html",
                                       title="Pitt Digital Scholarship Database",
                                       user = current_user)
            else:
                flash("Password is incorrect.", category="error")
        else:
            flash("Email not registered.", category="error")

    return render_template("login.html",
                           title="Log In",
                           user = current_user)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    if current_user.is_authenticated:
        current_user.set_permissions()
    return redirect(url_for('views_bp.index',
                    user=None))


@auth_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    current_user.set_permissions()
            
    if request.method == "POST":
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        user_name = request.form.get('user_name')
        email = request.form.get('email')
        cur_password = request.form.get('cur_password')
        password = request.form.get('password')
        password_conf = request.form.get('password_conf')
        admin_code = request.form.get('admin_code')
        # Check that email is from the Pitt domain
        regex = '^[a-z0-9]+@pitt.edu$'
        if not re.search(regex, email):
            flash("Please register using your Pitt (@pitt.edu) email address.", category='error')
        else:
            if password:
                if not sha256_crypt.verify(cur_password, current_user.user_password):
                    flash("Password is incorrect.", category="error")
                elif (len(password) < 8):
                    flash("Password must be at least 8 characters.", category='error')
                elif (len(password) > 16):
                    flash("Password must be less than 16 characters.", category='error')
                elif not re.search("[a-z]", password):
                    flash("Password must contain at least 1 lowercase alphabet.", category='error')
                elif not re.search("[A-Z]", password):
                    flash("Password must contain at least 1 uppercase alphabet.", category='error')
                elif not re.search("[0-9]", password):
                    flash("Password must contain at least 1 number.", category='error')
                elif not re.search("[_@()*&^%#<>,!$]", password):
                    flash("Password must contain at least 1 special character.", category='error')
                elif password != password_conf:
                    flash("Passwords do not match.", category='error')
            else:
                password = current_user.user_password
            # Check for valid admin code
            permission_id = current_user.fk_permission_id
            if admin_code:
                # Get all permission codes
                permission_codes = db_session.execute(
                    select(Permission.permission_code)).all()
                # Check for a matching permission code
                for code in permission_codes:
                    if sha256_crypt.verify(admin_code, code[0]):
                        permission_id_result = db_session.execute(
                            select(Permission.permission_id).where(
                            Permission.permission_code == code[0])).first()
                        permission_id = permission_id_result[0]
                        break
            # Save any updated user account variables
            p_level = permission_id
            current_user.first_name=first_name
            current_user.last_name=last_name,
            current_user.user_name=user_name,
            current_user.email=email,
            current_user.user_password=sha256_crypt.hash(password),
            current_user.permission_level=p_level
            db_session.commit()
            # Alert user that account was created succesfully
            flash("Account Details Updated!", category="success")
    
    return render_template("account.html",
                           title="Account",
                           user=current_user)
