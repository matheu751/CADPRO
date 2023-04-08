from flask import render_template, request, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, exc
from app import app
from models import db, User

login = LoginManager(app)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/register_user", methods=['POST', 'GET'])
def register_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        try:
            new_user = User(username = username, email = email)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
        except exc.IntegrityError:
            flash("Username or Email already exists")
        else:
            return redirect(url_for('login'))   
    return render_template("register_user.html")

@app.route("/login", methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('/home'))
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username = username).first()
        if user is None or not user.check_password(password):
            flash("Incorrect Username or Password")
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for("home"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))