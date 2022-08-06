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

login_manager = LoginManager()
login_manager.init_app(app)

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

# Verify user
@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == "POST":
        username = request.form.get('UserName')
        password = request.form.get('Password')
        user     = USER(USER_NAME=username, PASSWORD=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('signup.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form.get('UserName')
        password = request.form.get('Password')
        user     = USER.query.filter_by(USER_NAME=username).first()
        if check_password_hash(user.PASSWORD,password):
            login_user(user)
            return redirect('/')
        else:
            return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')
##########################################

# Create Event
@app.route('/<event_name>',methods=['GET','POST'])
def create_event():
    input_date_time_template = "%Y-%m-%d"
    if request.method == "POST":
        event = EVENT()
        event_name   = request.form.get('event_name')
        category_num = request.form.get('category_num') # 入力するカテゴリーの数
        event.EVENT_NAME = event_name
        event_id = event.EVENT_ID
        db.session.add(event)
        db.session.commit()

        # 開始
        start = DURING()
        start.DURING_ID = 0
        start.EVENT_ID  = event_id
        start.DATE      = datetime.datetime.strptime(request.form.get('start_date'),input_date_time_template)
        db.session.add(start)
        db.session.commit()

        # 終了
        end = DURING()
        end.DURING_ID = 1
        end.EVENT_ID  = event_id
        end.DATE      = datetime.datetime.strptime(request.form.get('end_date'),input_date_time_template)
        db.session.add(end)
        db.session.commit()

        # カテゴリーのタイトルと中身を記録する
        # [カテゴリーのタイトル, [カテゴリー1,カテゴリー2,....]]
        categories = []
        for i in range(category_num):
            now_num        = request.form.get('now_num')
            # ここは格納するべきなのか？
            category_title = request.form.get('category_title') 
            for j in range(now_num):
                event                  = EVENT()
                event.EVENT_NAME       = event_name
                event.EVENT_ID         = event_id
                category               = CATEGORY()
                category_name          = request.form.get('category_name')
                category.CATEGORY_NAME = category_name
                db.session(event)
                db.session.commit()
                db.session(category)
                db.session.commit()
        return redirect('/')

@app.route('/input_date',methods=['GET','POST'])
def input_date():
    if request.method == "POST":
        category_num = request.form.get('category_num')
        categories   = []
        for i in range(category_num):
            categories.append(request.form.get('now_category'))
        column_num = request.form.get('column_num')
        row_num    = request.form.get('row_num')
        date_data  = []
        for i in range(row_num):
            now_date = []
            for j in range(column_num):
                now_date.append(request.form.get('your_input'))
            date_data.append(now_date)
        user_input               = USER_INPUT()
        user_input.EVENT_NAME    = request.form.get('event_name')
        user_input.my_categories = categories
        user_input.my_dates      = date_data
        db.session(user_input)
        db.session.commit()
        return redirect('/')

# @app.route('/',methods=['GET','POST'])
# def check_date():
#     if request.method == "POST":
        