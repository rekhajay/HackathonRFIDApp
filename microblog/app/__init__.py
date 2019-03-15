from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from flask_bootstrap import Bootstrap


#import RPi.GPIO as GPIO


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

#GPIO.setmode(GPIO.BCM)


login = LoginManager(app)
login.login_view = 'login'


migrate = Migrate(app,db)

from app import routes, models
