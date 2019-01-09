from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, PasswordField, SubmitField, Form, IntegerField
from wtforms.validators import DataRequired, Length,Email , EqualTo, ValidationError
from Election.models import User, Option, db

class RegistrationForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired(), Length(10)])
	secretid = IntegerField('SecretId', validators = [DataRequired()])
	password = PasswordField('Password' , validators = [DataRequired()])
	confirmpassword = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password')])
	submit = SubmitField('Register')

	def validate_username(self,username):
		user = User.query.filter_by(username = username.data).first()
		if user:
			raise ValidationError('This user already exists.')
	def validate_secretid(self,secretid):
		if secretid.data != 1011:
			raise ValidationError('The secret id is incorrect')
class LoginForm(FlaskForm):
	username = StringField('Username',validators=[DataRequired(), Length(10)])
	password = PasswordField('Password',validators=[DataRequired()])
	submit = SubmitField('Login')

class CandidateLoginForm(FlaskForm):
	username = StringField('Username', validators = [DataRequired(), Length(max=30)])
	password = PasswordField('Password', validators=[DataRequired()])
	key = IntegerField('Key', validators=[DataRequired()])
	submit = SubmitField('Login')

class CandidateInfo(FlaskForm):
	info = TextAreaField('Content', validators = [DataRequired()])
	facebook = StringField('Facebook', validators = [DataRequired()])
	github = StringField('Github', validators = [DataRequired()])
	submit = SubmitField('Submit')