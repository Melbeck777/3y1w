import sqlite3

dbname = '3y1w'
conn = sqlite3.connect(dbname)
cur = conn.cursor()

cur.execute('create table USER(\
            USER_ID integer auto_increment not null primary key,\
            USER_NAME varchar(64),\
            PASSWORD varchar(128) not null,\
            EMAIL varchar(128));')

cur.execute('create table GROUP(\
            GROUP_ID integer auto_increment not null primary key,\
            GROUP_NAME varchar(64) not null);')

cur.execute('create table CATEGORY(\
            CATEGORY_ID integer auto_increment not null primary key,\
            CATEGORY varchar(64) not null,\
            GROUP_ID integer not null,\
            foreign key (GROUP_ID) references GROUP(GROUP_ID));')

cur.execute('create table EVENT(\
            EVENT_ID integer auto_increment not null primary key,\
            EVENT_NAME varchar(64) not null);')

cur.execute('create table DURING(\
            DURING_ID integer auto_increment not null primary key,\
            EVENT_ID integer not null,\
            DATE datetime not null,\
            foreign key (EVENT_ID) references EVENT(EVENT_ID));')

cur.execute('create table EVENT_CATEGORY(\
            EVENT_CATEGORY_ID integer auto_increment not null primary key,\
            EVENT_ID integer not null,\
            GROUP_ID integer not null,\
            foreign key (EVENT_ID) references EVENT(EVENT_ID),\
            foreign key (GROUP_ID) references GROUP(GROUP_ID));')

cur.execute('create table USER_CATEGORY(\
            USER_CATEGORY_ID integer auto_increment not null primary key,\
            USER_ID integer not null,\
            EVENT_ID integer not null,\
            CATEGORY_ID integer not null,\
            foreign key (USER_ID) references USER(USER_ID),\
            foreign key (EVENT_ID) references EVENT(EVENT_ID),\
            foreign key (CATEGORY_ID) references CATEGORY(CATEGORY_ID));')

# SCHEDULEは2進数の文字列で表現する（例: '0011101111'）
# 頭から順番にコマを割り当てる　（例: 1コマ: 0, 2コマ: 0, 3コマ: 1, ...）
cur.execute('create table USER_SCHEDULE(\
            USER_SCHEDULE_ID integer auto_increment not null,\
            EVENT_ID integer not null,\
            USER_ID integer not null,\
            SCHEDULE varchar(10) not null,\
            foreign key (USER_ID) references USER(USER_ID),\
            foreign key (EVENT_ID) references EVENT(EVENT_ID),\
            primary key (USER_SCHEDULE_ID, EVENT_ID));')

conn.commit()

cur.close()
conn.close()