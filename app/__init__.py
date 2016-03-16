from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import config


app = Flask(__name__)
app.config.from_object(config.ProductionConfig)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
from app import rest, views
