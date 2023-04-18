"""Module for Auth"""
from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from .database import db_session
from .models import User, Permission
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime
from passlib.hash import sha256_crypt
from sqlalchemy import select
from flask_login import login_user, login_required, logout_user, current_user


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
                elif not re.search("[_@()*&^%#<>,$]", password):
                    flash("Password must contain at least 1 special character.", category='error')
                elif password != password_conf:
                    flash("Passwords do not match.", category='error')
                else:
                    # Check for valid admin code
                    p_level = 1
                    permission_id = None
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
                        new_user = User(first_name=first_name,
                                        last_name=last_name,
                                        user_name=user_name,
                                        email=email,
                                        user_password=sha256_crypt.hash(password),
                                        api_key=api_key,
                                        permission_level=p_level,
                                        account_created=datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
                                        last_login=datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
                        # Add new user to database
                        db_session.add(new_user)
                        db_session.commit()
                        # Alert user that account was created succesfully
                        login_user(new_user)
                        flash("Account created!", category="success")

                        # Redirect to login page
                        return redirect(url_for('views_bp.index'))
                    else:
                        flash("Please enter a valid Administrator code.", category='error')
    
    if current_user.is_authenticated:
        current_user.set_permissions()
        
    return render_template("sign-up.html", 
                           title="Sign Up | Pitt Digital Scholarship Database",
                           user = current_user)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", category="error")
        return redirect(url_for('views_bp.index'))
    
    if request.method == "POST":
        email = request.form.get('email')
        print(email)
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
                           title="Login | Pitt Digital Scholarship Database",
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
    if current_user:
        print(request.method)
        current_user.set_permissions()
        email = current_user.email
        print(email)
        user = User.query.filter_by(email=email).first()
        print(user)
        if user:
            if request.method == "GET":
                result={"first_name":user.first_name, "last_name":user.last_name, "user_name":user.user_name, "email":user.email}
                print(result)
                return render_template("account.html",
                           title="Account | Pitt Digital Scholarship Database",
                           user=current_user,
                           result=result)
            if request.method == "POST":
                first_name = request.form.get('first_name')
                last_name = request.form.get('last_name')
                user_name = request.form.get('user_name')
                print(user_name)
                email = request.form.get('email')
                password = request.form.get('password')
                password_conf = request.form.get('password_conf')
                # Check that email is from the Pitt domain
                regex = '^[a-z0-9]+@pitt.edu$'
                if not re.search(regex, email):
                    flash("Please register using your Pitt (@pitt.edu) email address.", category='error')
                else:
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
                    elif not re.search("[_@()*&^%#<>,$]", password):
                        flash("Password must contain at least 1 special character.", category='error')
                    elif password != password_conf:
                        flash("Passwords do not match.", category='error')
                    else:
                        user.first_name=first_name
                        user.last_name=last_name,
                        user.user_name=user_name,
                        user.email=email,
                        user.user_password=sha256_crypt.hash(password),
                        db_session.commit()
                        # Alert user that account was created succesfully
                        flash("Account Details Updated!", category="success")
    else:
        flash("Login to view or update login details", category="error")
        return redirect(url_for('auth_bp.login'))
    return redirect(url_for('views_bp.index'))
