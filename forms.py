from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField
from wtforms.validators import DataRequired,Email,length


class SignupForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(),length(max=20)])
    email= StringField('Email', validators=[DataRequired(),Email()])
    password= PasswordField('Password',validators=[DataRequired()])
    confirmpassword= PasswordField('confirmar_Password',validators=[DataRequired()])
    submit=SubmitField('Registrar')


class RegisterForm(FlaskForm):
    Email=StringField('email_r',validators=[DataRequired(),Email()])
    password=PasswordField('password_r',validators=[DataRequired()])
