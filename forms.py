from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length


# ---------------------- Request Form ----------------------
class RequestForm(FlaskForm):
    requester_name = StringField(
        'Your Name',
        validators=[DataRequired(), Length(min=2, max=100)]
    )
    
    department = SelectField(
        'Department',
        choices=[],  # This will be filled dynamically from the database or API
        validators=[DataRequired()]
    )
    
    category = StringField(
        'Category',
        validators=[DataRequired(), Length(min=2, max=100)]
    )
    
    description = TextAreaField(
        'Description',
        validators=[DataRequired(), Length(min=5)]
    )
    
    submit = SubmitField('Submit Request')


# ---------------------- Admin Login Form ----------------------
class LoginForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=3, max=50)]
    )
    
    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=3, max=50)]
    )
    
    submit = SubmitField('Login')
