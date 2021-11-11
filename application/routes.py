from flask import render_template, redirect, url_for, flash, request
from application import app, db, bcrypt
from application.forms import SignUpForm, LoginForm, UpdateAccountForm
from application.models import User
from flask_login import login_user, logout_user, current_user, login_required


@app.route("/")  # default route
@app.route("/home")
# home page route
def home():
    # attaching the attributed html file
    return render_template("index.html", title="Home")


# about page route
@app.route("/about")
def about():
    # attaching the attributed html file
    return render_template("about.html", title="About")


# sign up page of website, accepts GET, POST requests
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        redirect(url_for('home'))
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
    if current_user.is_authenticated:
        redirect(url_for('home'))
    form = LoginForm()
    # if form validates, redirect to home
    if form.validate_on_submit():
        # select first user with input email
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            # if redirected to login, once logged in redirect back to requested page
            # use get method on dictionary args instead of [key] in case no "next" element
            requested_page = request.args.get("next")
            return redirect(requested_page) if requested_page else redirect(url_for('home'))
        else:
            flash("Incorrect username or password", 'danger')
    # attaching the attributed html file and passing in the login form
    return render_template("login.html", title="Login", form=form)


# logout route: redirects user to home page
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


# user account page route
@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    # upon validation, update user account information using PRG pattern
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.commit()
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    # getting path for user's profile image
    profile_image = url_for("static", filename="profile_pics/" + current_user.profile_img)
    # attaching the attributed html file and passing in user profile image
    return render_template("account.html", title="Account", form=form, profile_image=profile_image)
