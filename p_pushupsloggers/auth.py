from flask import Blueprint, flash, render_template,url_for,request,redirect
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_required
from .models import User
from . import db


auth = Blueprint('auth',__name__)

@auth.route('/signup/')
def signup():
    return render_template('signup.html')

@auth.route('/signup/',methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    # print(email,name,password)
    user = User.query.filter_by(email=email).first()

    if user:
        flash('email-id already exists!!!',"danger")
        return redirect('/signup')
    
    new_user = User(email=email,name=name,password=generate_password_hash(password,method='sha256'))
    db.session.add(new_user)
    db.session.commit()
    flash('Account Created :) ',"success")
    return redirect('/login')


@auth.route('/login/')
def login():
    return render_template('login.html')

@auth.route('/login/',methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password,password):
        flash('Error!!',"danger")
        return redirect('/login/')

    login_user(user,remember=remember)

    return redirect('/profile')




@auth.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))