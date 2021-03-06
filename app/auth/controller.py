from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from .forms import LoginForms, RegistrationForm
from ..models import User
from .. import db


@auth.route("/login", methods=["GET", "POST"])
def login():
    """ Route that displays the form to allow users to login."""

    form = LoginForms()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next = request.args.get("next")  
            
            if next is None or not next.startswith("/"): # Next is used to check if the user was redirected.
                next = url_for("main.index")
            return redirect(next)
        flash("Invalid username or password!")
    return render_template("auth/login.html", form=form)


@auth.route("/logout")
@login_required
def logout():
    """ Route to logout a logged in user"""
    
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("main.index"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    """ Route that registers a user using the registration form."""

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        flash("You are now registered")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)
