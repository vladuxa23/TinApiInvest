from flask import Flask
from flask_sqlalchemy import SQLAlchemy


flask_app = Flask(__name__)
flask_app.config.from_object('CapitalApp.configuration.Config')
db = SQLAlchemy(flask_app)  # flask-sqlalchemy


from CapitalApp import views, models
