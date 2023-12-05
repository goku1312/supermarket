import pymysql

dbc=pymysql.connect(user="root",host="localhost",password="",database="data")
def selectone(qry):
    cur=dbc.cursor()
    cur.execute(qry)
    data=cur.fetchone()
    return data
def insert(qry):
    cur=dbc.cursor()
    cur.execute(qry)
    dbc.commit()
def update(qry):
    cur=dbc.cursor()
    cur.execute(qry)
    dbc.commit()
def selectall(qry):
    cur=dbc.cursor()
    cur.execute(qry)
    data=cur.fetchall()
    return data
def delete(qry):
    cur=dbc.cursor()
    cur.execute(qry)
    dbc.commit()