from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo


class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirmpassword = PasswordField('Confirmar Password', validators=[DataRequired(), EqualTo('password', message='Las contraseñas deben coincidir')])
    submit = SubmitField('Registrar')


class RegisterForm(FlaskForm):
<<<<<<< HEAD
    Email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class Registerinformacion(FlaskForm):
    codigo=StringField('codigo_postal',validators=[DataRequired()])
=======
    Email=StringField('email_r',validators=[DataRequired(),Email()])
    password=PasswordField('password_r',validators=[DataRequired()])
>>>>>>> 889ab90fed7598423d334fd22af0003e90fcea8b
