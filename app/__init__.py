from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import config


app = Flask(__name__)
api = Api(app)
app.config.from_object(config.DevelopmentConfig)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
from app import rest, views