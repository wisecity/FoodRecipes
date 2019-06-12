from flask_wtf import FlaskForm
# from flask_login import current_user -- to validate
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class UserRegistrationForm(FlaskForm):
	username = StringField('Username',
		validators=[DataRequired(), Length(min=2, max=20)])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',
		validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')
	'''
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('Kullanici adi daha once alinmis.')
	'''


class UserLoginForm(FlaskForm):
	username = StringField('Username',
		validators=[DataRequired(), Length(min=2, max=20)])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember me')
	submit = SubmitField('Sign in')


class UpdateAccountForm(FlaskForm):
	username = StringField('Username',
		validators=[DataRequired(), Length(min=2, max=20)])
	password = StringField('Password', validators=[DataRequired()])
	submit = SubmitField('Update')

	'''
	def validate_username(self, username):
		print("{} - {}".format(username.data, current_user.username))
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('Kullanici adi daha once alinmis.')
	'''


class AddRecipeForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	contents = StringField('Contents', validators=[DataRequired()])
	details = StringField('Details', validators=[DataRequired()])
	submit = SubmitField('Submit Recipe')