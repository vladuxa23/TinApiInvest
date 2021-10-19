from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

flask_app = Flask(__name__)
flask_app.config.from_object('CapitalApp.configuration.Config')
db = SQLAlchemy(flask_app)  # flask-sqlalchemy
migrate = Migrate(flask_app, db)

from CapitalApp import views, models
