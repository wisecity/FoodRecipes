from flask_wtf import FlaskForm
# from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class AddRecipeForm(FlaskForm):
	name = StringField('Name', validators=[DataRequired()])
	contents = StringField('Contents', validators=[DataRequired()])
	details = StringField('Details', validators=[DataRequired()])
	submit = SubmitField('Submit Recipe')