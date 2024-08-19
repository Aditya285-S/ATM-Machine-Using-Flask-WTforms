from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SubmitField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError


def password_complexity_check(form, field):
    password = field.data
    if not any(char.isdigit() for char in password):
        raise ValidationError('Password must contain at least one digit.')
    if not any(char.isalpha() for char in password):
        raise ValidationError('Password must contain at least one letter.')
    if not any(char in '!@#$%^&*()-_+=' for char in password):
        raise ValidationError('Password must contain at least one special character.')



class LoginForms(FlaskForm):
    email = EmailField('Email', validators = [DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")



class SignupForms(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, message='Name must be of atleast 2 characters')
    ])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, max=20, message='Password must be between 8 and 20 characters'),
        password_complexity_check
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Sign Up')



class EmailCheck(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    submit = SubmitField('Validate')



class ResetPassForms(FlaskForm):
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, max=20, message='Password must be between 8 and 20 characters'),
        password_complexity_check
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match')
    ])
    submit = SubmitField('Reset')



class Create_account(FlaskForm):
    f_name = StringField('First Name', validators=[
        DataRequired(),
        Length(min=2, message='Name must be of atleast 2 characters')
    ])
    l_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(min=2, message='Name must be of atleast 2 characters')
    ])
    Account_number = StringField('Account Number', validators=[
        DataRequired(),
        Length(min=8, max=8, message='Account number must be 8 characters long')
    ])
    submit = SubmitField('Create')



class Check_account(FlaskForm):
    Account_number = StringField('Account Number', validators=[DataRequired()])
    submit = SubmitField('Validate')



class Create_pin(FlaskForm):
    pin = PasswordField('Pin', validators=[
        DataRequired(),
        Length(min=4, max=4, message='PIN must be 4 characters long')
    ])
    balance = StringField('Amount')
    submit = SubmitField('Create')



class Update_pin(FlaskForm):
    new_pin = PasswordField('New Pin', validators=[
        DataRequired(),
        Length(min=4, max=4, message='PIN must be 4 characters long')
    ])
    confirm_pin = PasswordField('Confirm Pin', validators=[
        DataRequired(),
        EqualTo('new_pin', message='Pin must match')
    ])
    submit = SubmitField('Update')



class Check_details(FlaskForm):
    Account_number = StringField('Account Number', validators=[DataRequired()])
    pin = PasswordField('Pin', validators=[DataRequired()])
    submit = SubmitField('Validate')
    


class Add_money(FlaskForm):
    amount = StringField('Amount', validators=[DataRequired()])
    submit = SubmitField('Add')



class Withdraw(FlaskForm):
    amount = StringField('Amount', validators=[DataRequired()])
    submit = SubmitField('Withdraw')
