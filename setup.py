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
    USER_ID   = db.Column(db.Integer, primary_key=True)
    USER_NAME = db.Column(db.VarChar(56),nullable=False)
    PASSWORD  = db.Column(db.VarChar(128))
    EMAIL     = db.Column(db.VarChar(128))

class CATEGORY():
    CATEGORY_ID   = db.Column(db.Integer,    nullable=False, primary_key=True, autoincrement=True)
    CATEGORY_NAME = db.Column(db.VarChar(64),nullable=False)
    
class EVENT(db.Model):
    EVENT_ID   = db.Column(db.Integer,    nullable=False, autoincrement=True)
    EVENT_NAME = db.Column(db.VarChar(64),nullable=False)

class DURING(db.Model):
    DURING_ID = db.Column(db.Integer,  nullable=False)
    EVENT_ID  = db.Column(db.Integer,  nullable=False)
    DATE      = db.Column(db.DateTime, nullable=False)

class EVENT_CATEGORY(db.Model):
    EVENT_CATEGORY_ID = db.Column(db.Integer, nullable=False)
    EVENT_ID          = db.Column(db.Integer, nullable=False, autoincrement=True)
    CATEGORY_ID       = db.Column(db.Integer, nullable=False)
    
class USER_CATEGORY(db.Model):
    USER_CATEGORY_ID = db.Column(db.Integer, nullable=False, autoincrement=True)
    USER_ID          = db.Column(db.Integer, nullable=False)
    EVENT_ID         = db.Column(db.Integer, nullable=False)
    CATEGORY_ID      = db.Column(db.Integer, nullable=False)

class USER_INPUT(db.Model):
    USER_ID       = db.Column(db.Integer,     primary_key=True)
    EVENT_ID      = db.Column(db.Integer,     nullable=False, unique=True)
    CATEGORY_ID   = db.Column(db.Integer,     nullable=False)
    CATEGORY_NAME = db.Column(db.VarChar(64), nullable=False)