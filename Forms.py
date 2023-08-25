from wtforms import StringField, SelectField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms.widgets import PasswordInput
from wtforms.fields import DateField, EmailField



class RegistrationForm(FlaskForm):
	name = StringField('Name',[DataRequired(), Length(min=2, max=50,
                                                                     message='Name should be 2 to 50 characters long')])
	email = EmailField('Email', [DataRequired()])
	phone = StringField('Phone Number',[DataRequired(), Length(min=10, max=10,
                                                                       message='Phone Number should be 10 characters long')])
	password = StringField('Password', [DataRequired(),Length(min=8,
                                                                   message='Password should be minimum 8 characters long')], widget=PasswordInput(hide_value=False))
	submit = SubmitField('Register')

class LoginForm(FlaskForm):
	email = EmailField('Email', [DataRequired()])
	password = StringField('Password', [DataRequired()], widget=PasswordInput(hide_value=False))
	submit = SubmitField('Login')

class IncomeForm(FlaskForm):
	income_src = StringField('Income Source',[DataRequired()])
	income_amt = StringField('Income Amount',[DataRequired()])
	submit = SubmitField('Submit')

class ExpenseForm(FlaskForm):
	expense_src = StringField('Expense Source',[DataRequired()])
	expense_amt = StringField('Expense Amount',[DataRequired()])
	submit = SubmitField('Submit')