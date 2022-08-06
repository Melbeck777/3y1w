import sqlite3

dbname = '3y1w'
conn = sqlite3.connect(dbname)

cur = conn.cursor()

cur.execute('create table USER(USER_ID integer auto_increment not null primary key, USER_NAME varchar(64), PASSWORD varchar(128) not null, EMAIL varchar(128));')
cur.execute('create table CATEGORY(CATEGORY_ID integer auto_increment not null primary key, CATEGORY varchar(64) not null);')
cur.execute('create table EVENT(EVENT_ID integer auto_increment not null primary key, EVENT_NAME varchar(64) not null);')
cur.execute('create table DURING(DURING_ID integer auto_increment not null, EVENT_ID integer not null, START_DATE datetime not null, END_DATE datetime not null, foreign key (EVENT_ID) references EVENT(EVENT_ID), primary key (DURING_ID, EVENT_ID));')
cur.execute('create table EVENT_CATEGORY(EVENT_CATEGORY_ID integer auto_increment not null, EVENT_ID integer not null, CATEGORY_ID integer not null, foreign key (EVENT_ID) references EVENT(EVENT_ID), foreign key (CATEGORY_ID) references CATEGORY(CATEGORY_ID), primary key (EVENT_CATEGORY_ID, EVENT_ID));')
cur.execute('create table USER_CATEGORY(USER_CATEGORY_ID integer auto_increment not null, USER_ID integer not null, EVENT_ID integer not null, CATEGORY_ID integer not null, foreign key (USER_ID) references USER(USER_ID), foreign key (EVENT_ID) references EVENT(EVENT_ID), foreign key (CATEGORY_ID) references CATEGORY(CATEGORY_ID), primary key (USER_CATEGORY_ID, USER_ID, EVENT_ID));')

conn.commit()

cur.close()
conn.close()