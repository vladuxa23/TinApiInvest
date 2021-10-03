from flask import Flask
from flask_sqlalchemy import SQLAlchemy


flask_app = Flask(__name__)
flask_app.config.from_object('app.configuration.Config')
db = SQLAlchemy(flask_app)  # flask-sqlalchemy

from app import views, models
