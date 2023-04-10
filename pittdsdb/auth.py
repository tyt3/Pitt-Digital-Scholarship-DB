"""Module for Auth"""
from flask import Blueprint, render_template, request, redirect, session, url_for
from .database import db_session
from .models import User
import secrets
from werkzeug.security import generate_password_hash, check_password_hash
import re
from datetime import datetime
from passlib.hash import sha256_crypt


auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    msg = ""
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user :
            msg = "This email is already registered"
        else:
            regex = '^[a-z0-9]+@pitt.edu$'
            if re.search(regex,email):
                first_name = request.form.get('first_name')
                last_name = request.form.get('last_name')
                user_name = request.form.get('user_name')
                flag = 0
                if (len(password)<8):
                    msg = "Password should be min 8 characters"
                elif not re.search("[a-z]", password):
                    msg = "Password should contain atleast 1 lower case alphabet"
                elif not re.search("[A-Z]", password):
                    msg = "Password should contain atleast 1 upper case alphabet"
                elif not re.search("[0-9]", password):
                    msg = "Password should contain atleast 1 number"
                elif not re.search("[_@()*&^%#<>,$]" , password):
                    msg = "Password should contain atleast 1 special character"
                if len(msg) == 0:
                    p_level = request.form.get('permission_level')
                    if p_level > 4 or p_level < 1:
                        msg= "Invalid Permission"
                    else:
                        api_key = secrets.token_hex(16)
                        user = User(first_name=first_name, last_name=last_name, user_name=user_name, email=email, user_password=sha256_crypt.encrypt(password), api_key=api_key, permission_level=p_level, account_created = datetime.now().strftime("%Y/%m/%d %H:%M:%S"), last_login=datetime.now().strftime("%Y/%m/%d %H:%M:%S") )
                        db_session.add(user)
                        db_session.commit()
                        return redirect(url_for('auth_bp.login'))
            else:
                msg = "Please register using pitt.edu email address"
    return render_template("sign-up.html", title="Pitt Digital Scholarship Database", msg=msg)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    msg = ""
    if request.method == "POST":
        email = request.form.get('email')
        password = sha256_crypt.encrypt(request.form.get('password'))
        user = User.query.filter_by(email=email).first()
        
        remember = True if request.form.get('remember') else False

        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if user :
            if sha256_crypt.verify(user.password, password):
                session["email"] = email
                if user.permission_level == 4:
                    can_add = True
                    can_update = True
                    can_update_created = True
                    can_delete= True
                    can_search = True
                elif user.permission_level == 3:
                    can_add = True
                    can_update_all = True
                    can_update_created = True
                elif user.permission_level == 2:
                    can_add = True
                    can_update_created = True
                user.last_login=datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                db_session.commit()
                return render_template("index.html", title="Pitt Digital Scholarship Database", can_add=can_add, can_delete = can_delete, can_update_all = can_update_all, can_update_created = can_update_created)
            else:
                msg = "Wrong Password"
        else:
            msg = "Email not registered"
    return render_template("login.html", title="Login | Pitt Digital Scholarship Database", msg = msg)

@auth_bp.route('/logout')
def logout():
    session["email"] = None
    return render_template("logout.html", title="Logout | Pitt Digital Scholarship Database")

@auth_bp.route('/account')
def account():
    if 'email' in session:
        email = session['email']
        user = User.query.filter_by(email=email).first()
        return render_template("account.html", title="Account | Pitt Digital Scholarship Database", first_name = user.first_name, last_name=user.last_name, user_name=user.user_name, email=user.email, user_password=sha256_crypt.encrypt(user.user_password), api_key=user.api_key, permission_level=user.permission_level, account_created = user.account_created, last_login=user.lase_login)
    else:
        return render_template("login.html", title="Login | Pitt Digital Scholarship Database", msg = "Please login to see the account details")

@auth_bp.route('/update_account')
def update_account():
    if 'email' in session and request.method == "POST":
        email = session['email']
        user = User.query.filter_by(email=email).first()
        if user is not None:
            email = request.form.get('email')
            password = request.form.get('password')
            regex = '^[a-z0-9]+@pitt.edu$'
            if re.search(regex,email):
                first_name = request.form.get('first_name')
                last_name = request.form.get('last_name')
                user_name = request.form.get('user_name')
                flag = 0
                if (len(password)<8):
                    msg = "Password should be min 8 characters"
                elif not re.search("[a-z]", password):
                    msg = "Password should contain atleast 1 lower case alphabet"
                elif not re.search("[A-Z]", password):
                    msg = "Password should contain atleast 1 upper case alphabet"
                elif not re.search("[0-9]", password):
                    msg = "Password should contain atleast 1 number"
                elif not re.search("[_@()*&^%#<>,$]" , password):
                    msg = "Password should contain atleast 1 special character"
                if len(msg) == 0:
                    p_level = request.form.get('permission_level')
                    if p_level > 4 or p_level < 1:
                        msg= "Invalid Permission"
                    else:
                        user.first_name = first_name
                        user.last_name = last_name
                        user.user_name = user_name
                        user.password = sha256_crypt.encrypt(password)
                        user.permission_level = p_level
                        db_session.commit()
                        return redirect(url_for('auth_bp.account'))
            else:
                msg = "Please register using pitt.edu email address"
        return render_template("account.html", title="Account | Pitt Digital Scholarship Database", first_name = first_name, last_name=last_name, user_name=user_name, email=email, user_password="", api_key=api_key, permission_level=p_level, account_created = user.account_created, last_login=user.lase_login, msg = msg)
    else:
        return render_template("login.html", title="Login | Pitt Digital Scholarship Database", msg = "Please login to update the account details")
