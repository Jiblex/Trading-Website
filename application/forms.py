from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo
from application.models import User


# Class represents a registration form when creating a new account, validates user registration fields
class SignUpForm(FlaskForm):
    # username: requires data, minimum length 3, max length 20
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)],
                           render_kw={'placeholder': "Username"})
    # email: requires data
    email = StringField('Email', validators=[DataRequired()], render_kw={'placeholder': "Email"})
    # password: requires data, min length 6
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)],
                             render_kw={'placeholder': "Password"})
    # confirm password: requires data, must equal password field
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')],
                                     render_kw={'placeholder': "Confirm Password"})
    # submit field: represents a sign up button
    submit_field = SubmitField('Sign Up', render_kw={'placeholder': "Sign Up"})

    # function used to validate username by seeing if username already exists in database
    def validate_username(self, username):
        # search for first instance of entered username, if none returns false
        taken = User.query.filter_by(username=username.data).first()
        if taken:
            raise ValidationError('Username taken.')

    # function used to validate email by seeing if email already exists in database
    def validate_email(self, email):
        # search for first instance of entered email, if none returns false
        taken = User.query.filter_by(email=email.data).first()
        if taken:
            raise ValidationError('Email taken.')


# Class represents a login form, validates user login fields
class LoginForm(FlaskForm):
    # email: requires data
    email = StringField('Email', validators=[DataRequired()], render_kw={'placeholder': "Email"})
    # password: requires data
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder': "Password"})
    # submit field: represents a login button
    submit_field = SubmitField('Login')


# Class represents user account update form
class UpdateAccountForm(FlaskForm):
    # username: requires data, minimum length 3, max length 20
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)],
                           render_kw={'placeholder': "Username"})
    # email: requires data
    email = StringField('Email', validators=[DataRequired()], render_kw={'placeholder': "Email"})
    # submit field: represents an update account information button
    submit_field = SubmitField('Update', render_kw={'placeholder': "Update"})

    # function used to validate username by seeing if username already exists in database
    def validate_username(self, username):
        # checks if user has updated username
        if username.data != current_user.username:
            # search for first instance of entered username, if none returns false
            taken = User.query.filter_by(username=username.data).first()
            if taken:
                raise ValidationError('Username taken.')

    # function used to validate email by seeing if email already exists in database
    def validate_email(self, email):
        # checks if user has updated email
        if email.data != current_user.email:
            # search for first instance of entered email, if none returns false
            taken = User.query.filter_by(email=email.data).first()
            if taken:
                raise ValidationError('Email taken.')
