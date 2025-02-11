from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class LinkForm(FlaskForm):
    yt_link = StringField('Youtube Link',validators=[
            DataRequired(message="O link do YouTube é obrigatório."),
            Regexp(
                regex=r'^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+',
                message="The url entered is not from YouTube."
            )
        ]
    )
    submit = SubmitField('Download')