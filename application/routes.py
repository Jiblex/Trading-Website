from flask import render_template, redirect, url_for , flash
from application import app, db, bcrypt
from application.forms import SignUpForm, LoginForm
from application.models import User
from flask_login import login_user, logout_user


@app.route("/")  # default route
@app.route("/home")
# home page of website
def home():
    # attaching the attributed html file
    return render_template("home.html", title="Home")


# about page of website
@app.route("/about")
def about():
    # attaching the attributed html file
    return render_template("about.html", title="About")


# sign up page of website, accepts GET, POST requests
@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    # if form validates, redirect to home
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    # attaching the attributed html file and passing in the sign up form
    return render_template("signup.html", title="Sign Up", form=form)


# login page of website, accepts GET, POST requests
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    # if form validates, redirect to home
    if form.validate_on_submit():
        # select first user with input email
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash("Incorrect username or password", 'danger')
    # attaching the attributed html file and passing in the login form
    return render_template("login.html", title="Login", form=form)


# page displayed when user logged in so that they don't see login/signup options
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))
