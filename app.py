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
from setup import db
import subprocess
input_date_time_template = "%Y-%m-%d"


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///3y1w.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.urandom(24)

# db = SQLAlchemy(app)

# subprocess.run("py ./setup.py")

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return USER.query.get(int(user_id))

# Verify user
@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        # username = request.form.get('UserName')
        password = request.form.get('Password')
        email    = request.form.get('Email')
        print("{}, {}".format(email,password))
        user     = USER(EMAIL=email, PASSWORD=password)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    else:
        return render_template('signup.html')


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # username = request.form.get('UserName')
        email    = request.form.get('Email')
        password = request.form.get('Password')
        user     = USER.query.filter_by(EMAIL=email).first()
        if check_password_hash(user.PASSWORD,password):
            login_user(user)
            return redirect('/event')
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')
##########################################

# Create Event
@app.route('/event',methods=['GET','POST'])
def event():
    if request.method == 'POST':
        event_name       = request.form.get('event_name')
        # category_num     = request.form.get('category_num') # 入力するカテゴリーの数
        category_num     = 2
        event            = EVENT(EVENT_NAME=event_name)
        
        db.session.add(event)
        db.session.commit()
        # db.flush()
        event_id = event.EVENT_ID
        print("event_name = {}\nevent_id {}".format(event_name, event.EVENT_ID))

        # 開始
        # start.DURING_ID = 0
        start_date      = datetime.datetime.strptime(request.form.get('date'),input_date_time_template)
        # start.DATE      = datetime.datetime.strptime(request.form.get('start_date'),input_date_time_template)
        start = DURING(EVENT_ID=event_id, DATE=start_date)
        
        # print("{}, {}".format(start.DURING_ID, start.DATE))

        db.session.add(start)
        db.session.commit()
        # 終了
        # end = DURING()
        # # end.DURING_ID = 1
        # # end.EVENT_ID  = event_id
        # end.DATE      = datetime.datetime.strptime(request.form.get('end_date'),input_date_time_template)
        # db.session.add(end)
        # db.session.commit()
        category_title = ["学年","班"]

        # カテゴリーのタイトルと中身を記録する
        # [カテゴリーのタイトル, [カテゴリー1,カテゴリー2,....]]
        categories = []
        for i in range(category_num):
            now_num        = request.form.get('now_num')
            # ここは格納するべきなのか？
            category_group = CATEGORY_GROUP()
            category_group.GROUP_NAME = category_title[i]
            db.session.add(category_group)
            db.session.commit()
            category_names = request.form.get('category{}'.format(i+1)).split(',')
            print("category_names = {}".format(category_names))
            category_group_id = category_group.CATEGORY_GROUP_ID
            for category_name in category_names:
                category               = CATEGORY()
                category.CATEGORY_NAME = category_name
                category.CATEGORY_GROUP_ID = category_group_id
                db.session.add(event)
                db.session.commit()
                db.session.add(category)
                db.session.commit()
        return render_template('completion.html',event_id=event_id)
    else:
        return render_template('event.html')

@app.route('/completion')
def completion(event_id):
    return render_template('completion.html',event_id=event_id)

# ユーザがデータを入力するときの関数
@app.route('/<event_id>/schedule',methods=['GET','POST'])
def input_date(event_id):
    if request.method == 'POST':
        # user_id = request.form.get('user_id')
        # event_id = request.form.get('event_id')
        category_num = request.form.get('category_num')
        categories   = []
        for i in range(category_num):
            categories.append(request.form.get('category_title'))
        column_num = 10
        row_num    = request.form.get('row_num')
        for i in range(row_num):
            now_date = datetime.strptime(request.form.get('date'),input_date_time_template)          
            user_schedule                  = USER_SCHEDULE()
            user_schedule.USER_SCHEDULE_ID = now_date.weekday()
            # user_schedule.EVENT_ID         = event_id
            # user_schedule.USER_ID          = user_id
            schedule_txt = ""
            for j in range(column_num):
                schedule_txt += request.form.get("input")
            user_schedule.SCHEDULE = schedule_txt
            db.add(user_schedule)
            db.commit()
        return redirect('/')


# htmlに対応する箇所(ファイル名，内部変数名)
# 予定の自動入力関数
@app.route('/<user_id>/<event_id>',methods=['GET','POST'])
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

# @app.route('/<event_id>/result')
# def result(event_id):
    


db.init_app(app)
if __name__ == "__main__":
    app.run(debug=True)