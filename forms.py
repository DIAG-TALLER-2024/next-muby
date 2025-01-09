from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError
from models import User


class ProfileForm(FlaskForm):
    favorite_genre = SelectField(
        '¿Qué género de película te gusta más?',
        choices=[
            ('Ninguno en particular', 'Ninguno en particular'),
            ('Acción', 'Acción'),
            ('Aventura', 'Aventura'),
            ('Comedia', 'Comedia'),
            ('Drama', 'Drama'),
            ('Fantasía', 'Fantasía'),
            ('Ciencia Ficción', 'Ciencia Ficción'),
            ('Musical', 'Musical'),
            ('Romance', 'Romance'),
            ('Suspenso', 'Suspenso'),
            ('Animación', 'Animación'),
        ]
    )
    disliked_genre = SelectField(
        '¿Qué género de película prefieres evitar?',
        choices=[
            ('Ninguno en particular', 'Ninguno en particular'),
            ('Acción', 'Acción'),
            ('Aventura', 'Aventura'),
            ('Comedia', 'Comedia'),
            ('Drama', 'Drama'),
            ('Fantasía', 'Fantasía'),
            ('Ciencia Ficción', 'Ciencia Ficción'),
            ('Musical', 'Musical'),
            ('Romance', 'Romance'),
            ('Suspenso', 'Suspenso'),
            ('Animación', 'Animación'),
        ]
    )
    submit = SubmitField('Guardar')


class SignUpForm(FlaskForm):
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email(message='Esto no parece ser un correo válido')])
    password = PasswordField('Contraseña', validators=[DataRequired(message='Este campo es obligatorio')])
    password_confirmation = PasswordField(
        'Confirmar Contraseña',
        validators=[
            DataRequired(message='Este campo es obligatorio'),
            EqualTo('password', message='Las contraseñas deben coincidir')
        ]
    )
    submit = SubmitField('Registrarse')
    def validate_email(self, email):
        existing_user = User.query.filter_by(email=email.data).first()  # Consulta en la base de datos
        if existing_user:
            raise ValidationError("El correo electrónico ya está registrado.")


class LoginForm(FlaskForm):
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email(message='Esto no parece ser un correo válido')])
    password = PasswordField('Contraseña', validators=[DataRequired(message='Este campo es obligatorio')])
    submit = SubmitField('Iniciar Sesión')
