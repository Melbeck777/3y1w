from email.policy import default
import os
from unicodedata import category 
from flask import Flask, render_template
from flask import request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user,logout_user,login_required
from sqlalchemy import column
from sqlalchemy.dialects import postgresql as pg
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://3y1w.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.urandom(24)

db = SQLAlchemy(app)

class USER(UserMixin, db.Model):
    USER_ID   = db.Column(db.Integer,      nullable=False, primary_key=True, autoincrement=True)
    PASSWORD  = db.Column(db.String(128), nullable=False)
    USER_NAME = db.Column(db.String(64))
    EMAIL     = db.Column(db.String(128))

class CATEGORY_GROUP(db.Model):
    CATEGORY_GROUP_ID = db.Column(db.Integer,     nullable=False, primary_key=True, autoincrement=True)
    GROUP_NAME        = db.Column(db.String(64), nullable=False)

class CATEGORY(db.Model):
    CATEGORY_ID       = db.Column(db.Integer,     nullable=False, primary_key=True, autoincrement=True)
    CATEGORY_NAME     = db.Column(db.String(64), nullable=False)
    CATEGORY_GROUP_ID = db.Column(db.Integer,     nullable=False)    # foreign key
    
class EVENT(db.Model):
    EVENT_ID   = db.Column(db.Integer,     nullable=False, primary_key=True, autoincrement=True)
    EVENT_NAME = db.Column(db.String(64), nullable=False)

class DURING(db.Model):
    DURING_ID = db.Column(db.Integer,  nullable=False, primary_key=True, autoincrement=True)
    EVENT_ID  = db.Column(db.Integer,  nullable=False)      # foreign key
    DATE      = db.Column(db.DateTime, nullable=False)

class EVENT_CATEGORY(db.Model):
    EVENT_CATEGORY_ID = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    EVENT_ID          = db.Column(db.Integer, nullable=False)   # foreign key
    CATEGORY_GROUP_ID = db.Column(db.Integer, nullable=False)   # foreign key
    
class USER_CATEGORY(db.Model):
    USER_CATEGORY_ID = db.Column(db.Integer, nullable=False, primary_key=True, autoincrement=True)
    USER_ID          = db.Column(db.Integer, nullable=False)    # foreign key
    EVENT_ID         = db.Column(db.Integer, nullable=False)    # foreign key
    CATEGORY_ID      = db.Column(db.Integer, nullable=False)    # foreign key

class USER_SCHEDULE(db.Model):
    USER_SCHEDULE_ID = db.Column(db.Integer,     nullable=False, primary_key=True, autoincrement=True)
    EVENT_ID         = db.Column(db.Integer,     nullable=False, primary_key=True)    # foreign key
    USER_ID          = db.Column(db.Integer,     nullable=False)    # foreign key
    SCHEDULE         = db.Column(db.String(10), nullable=False)