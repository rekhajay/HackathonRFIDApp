#import os
#from flask import Flask
#from flask_sqlalchemy import flask_sqlalchemy
#from flask_migrate import Migrate
from app import login
from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

#This class contains user login info
#this is another change to test
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)



class Swipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    rfid = db.Column(db.Integer)

    def __repr__(self):
        return '<Swipe {}>'.format(self.body)


class Rfid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rftagid = db.Column(db.Integer, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    users = db.relationship('User', backref='rfid')
    def __repr__(self):
        return '<Rfid {}>'.format(self.rfidtag)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
