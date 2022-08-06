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
from setup import USER, CATEGORY, EVENT,  EVENT, DURING, EVENT_CATEGORY, USER_CATEGORY, USER_SCHEDULE, CATEGORY_GROUP

input_date_time_template = "%Y-%m-%d"


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://3y1w.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.urandom(24)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


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
    if request.method == "POST":
        event            = EVENT()
        event_name       = request.form.get('event_name')
        category_num     = request.form.get('category_num') # 入力するカテゴリーの数
        event.EVENT_NAME = event_name
        event_id         = event.EVENT_ID
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
            group = CATEGORY_GROUP()
            group.GROUP_NAME = category_title
            db.session(group)
            db.session.commit()
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
        user_id = request.form.get('user_id')
        event_id = request.form.get('event_id')
        category_num = request.form.get('category_num')
        categories   = []
        for i in range(category_num):
            categories.append(request.form.get('now_category'))
        column_num = 10
        row_num    = request.form.get('row_num')
        for i in range(row_num):
            now_date = datetime.strptime(request.form.get('date'),input_date_time_template)          
            for j in range(column_num):
                user_schedule = USER_SCHEDULE()
                user_schedule.USER_SCHEDULE_ID = now_date.weekday()
                user_schedule.EVENT_ID         = event_id
                user_schedule.USER_ID          = user_id
                user_schedule.SCHEDULE         = request.form.get("schedule")
                db.add(user_schedule)
                db.commit()
        return redirect('/')               

@app.route('/',methods=['GET','POST'])
def check_date(event_id,user_id):
    durations = db.query(DURING).filter(DURING.EVENT_ID == event_id).all()
    now = durations[0]
    date_range = [[now,now.weekday()]]
    auto_data = [user_id,event_id]
    while now != durations[1]:
        now += datetime.timedelta(days=1)
        date_range.append([now,now.weekday()])
    for it in date_range:
        # 曜日 = SCHEDULE_ID
        now_ans = db.query(USER_SCHEDULE).filter(USER_SCHEDULE.START_DATE >= it[0],
                            USER_SCHEDULE.END_DATE <= it[0],
                            USER_SCHEDULE.USER_SCHEDULE_ID == it[1]).all()
        if(now_ans == None):
            continue