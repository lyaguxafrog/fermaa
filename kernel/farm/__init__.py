# -*- coding: utf-8 -*-

from flask import Flask

from flask_bootstrap import Bootstrap
from flask_babel import Babel
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO, emit


import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


app = Flask(__name__, static_url_path='/uploads', static_folder='uploads')
bootstrap = Bootstrap(app)
babel = Babel(app)
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*")


app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = os.getenv("SECRETKEY")
app.config['UPLOAD_FOLDER'] = 'uploads'

login_manager = LoginManager()
login_manager.login_view = "login" # type: ignore
login_manager.init_app(app)

POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")



app.config['SQLALCHEMY_DATABASE_URI'] = (
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

migrate = Migrate(app, db)

from farm import route, admin
