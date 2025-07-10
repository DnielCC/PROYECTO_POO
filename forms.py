from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms import ValidationError 
from config import ConexionDB
from wtforms import PasswordField
conexion = ConexionDB() 

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirmpassword = PasswordField('Confirmar Password', validators=[DataRequired(), EqualTo('password', message='Las contraseñas deben coincidir')])
    submit = SubmitField('Registrar')

    def validate_email(self, field):

        correo_a_validar = field.data
 
        consulta = conexion.get_datos(f"SELECT * FROM login WHERE correo = '{correo_a_validar}'")

        if len(consulta) > 0:
            raise ValidationError('Este correo electrónico ya está registrado. Por favor, usa otro o inicia sesión.')


class RegisterForm(FlaskForm):
    Email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class Registerinformacion(FlaskForm):
    codigo=StringField('codigo_postal',validators=[DataRequired()])
