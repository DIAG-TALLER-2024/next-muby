from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField


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
