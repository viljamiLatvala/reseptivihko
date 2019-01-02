from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user

from application import app, db
from application.auth.models import User
from application.auth.forms import LoginForm, SignupForm

from sqlalchemy import func

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
        return render_template("auth/loginform.html", form = form,
                               error = "No such username or password")
    login_user(user)
    return redirect(url_for("index"))

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/auth/signup", methods = ["GET", "POST"])
def auth_signup():
    if request.method == "GET":
        return render_template("auth/signupform.html", form = SignupForm())

    form = SignupForm(request.form)

    if not form.validate():
        return render_template("auth/signupform.html", form = form)
    
    nameTaken = User.query.filter(func.lower(User.username) == func.lower(form.username.data)).first()
    if nameTaken:
        form.username.errors.append('usename taken!')
        return render_template("auth/signupform.html", form = form)

    newUser = User(form.name.data,form.username.data,form.password.data)
    db.session().add(newUser)
    db.session().commit()

    createdUser = User.query.filter(username=form.username.data, password=form.password.data).first()
    login_user(createdUser)
    return redirect(url_for("index"))