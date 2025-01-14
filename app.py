from flask import Flask, render_template, request, flash, jsonify
from flask_bootstrap import Bootstrap5
from openai import OpenAI
from dotenv import load_dotenv
from db import db, db_config
from models import User, Message
from forms import ProfileForm, SignUpForm, LoginForm
from flask_wtf.csrf import CSRFProtect
from os import getenv
import json
from bot import search_movie_or_tv_show, where_to_watch
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from flask_bcrypt import Bcrypt
from flask import redirect, url_for
from langsmith.wrappers import wrap_openai

load_dotenv()

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message = 'Inicia sesión para continuar'
client = wrap_openai(OpenAI())
app = Flask(__name__)
app.secret_key = getenv('SECRET_KEY')
bootstrap = Bootstrap5(app)
csrf = CSRFProtect(app)
login_manager.init_app(app)
bcrypt = Bcrypt(app)
db_config(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



tools = [
    {
        'type': 'function',
        'function': {
            "name": "where_to_watch",
            "description": "Returns a list of platforms where a specified movie can be watched.",
            "parameters": {
                "type": "object",
                "required": [
                    "name"
                ],
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the movie to search for"
                    }
                },
                "additionalProperties": False
            }
        },
    },
    {
        'type': 'function',
        'function': {
            "name": "search_movie_or_tv_show",
            "description": "Returns information about a specified movie or TV show.",
            "parameters": {
                "type": "object",
                "required": [
                    "name"
                ],
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The name of the movie/tv show to search for"
                    }
                },
                "additionalProperties": False
            }
        },
    }
]


@app.route('/')
def index():
    return render_template('landing.html')


@app.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    user = db.session.query(User).get(current_user.id)

    if request.method == 'GET':
        return render_template('chat.html', messages=user.messages)

    user_message = request.form.get('message')

    # Guardar nuevo mensaje en la BD
    db.session.add(Message(content=user_message, author="user", user=user))
    db.session.commit()

    # Crear prompt para el modelo
    system_prompt = '''Eres un chatbot que recomienda películas, te llamas 'Next Moby'.
    - Tu rol es responder recomendaciones de manera breve y concisa.
    - No repitas recomendaciones.
    '''

    # Incluir preferencias del usuario
    if user.favorite_genre:
        system_prompt += f'- El género favorito del usuario es: {user.favorite_genre}.\n'
    if user.disliked_genre:
        system_prompt += f'- El género a evitar del usuario es: {user.disliked_genre}.\n'

    messages_for_llm = [{"role": "system", "content": system_prompt}]

    for message in user.messages:
        messages_for_llm.append({
            "role": message.author,
            "content": message.content,
        })

    chat_completion = client.chat.completions.create(
        messages=messages_for_llm,
        model="gpt-4o",
        temperature=1,
        tools=tools,
    )

    if chat_completion.choices[0].message.tool_calls:
        tool_call = chat_completion.choices[0].message.tool_calls[0]

        if tool_call.function.name == 'where_to_watch':
            arguments = json.loads(tool_call.function.arguments)
            name = arguments['name']
            model_recommendation = where_to_watch(client, name, user)
        elif tool_call.function.name == 'search_movie_or_tv_show':
            arguments = json.loads(tool_call.function.arguments)
            name = arguments['name']
            model_recommendation = search_movie_or_tv_show(client, name, user)
    else:
        model_recommendation = chat_completion.choices[0].message.content

    db.session.add(Message(content=model_recommendation, author="assistant", user=user))
    db.session.commit()

    accept_header = request.headers.get('Accept')
    if accept_header and 'application/json' in accept_header:
        last_message = user.messages[-1]
        return jsonify({
            'author': last_message.author,
            'content': last_message.content,
        })

    return render_template('chat.html', messages=user.messages)


@app.route('/perfil', methods=['GET', 'POST'])
@login_required
def perfil():
    user = db.session.query(User).get(current_user.id)

    if request.method == 'POST':
        form = ProfileForm()
        if form.validate_on_submit():
            user.favorite_genre = form.favorite_genre.data
            user.disliked_genre = form.disliked_genre.data
            db.session.commit()
    else:
        form = ProfileForm(obj=user)

    return render_template('perfil.html', form=form)


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = User(email=email, password_hash=bcrypt.generate_password_hash(password).decode('utf-8'))
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('chat'))
    return render_template('sign-up.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = db.session.query(User).filter_by(email=email).first()
            if user and bcrypt.check_password_hash(user.password_hash, password):
                login_user(user)
                return redirect('chat')

            flash("El correo o la contraseña es incorrecta.", "error")

    return render_template('log-in.html', form=form)


@app.get('/logout')
def logout():
    logout_user()
    return redirect('/')
