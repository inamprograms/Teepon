# app/app.py
from dotenv import load_dotenv
from flask import Flask

from .routes import users_blueprint
from .extensions import db, migrate
from .config import Config

import os
load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(users_blueprint())

    return app
