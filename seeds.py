from db import db
from app import app
from models import User, Message

with app.app_context():
    db.create_all()
