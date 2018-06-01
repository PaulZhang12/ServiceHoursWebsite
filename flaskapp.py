from flask import Flask
from flask import render_template
import csv
import sqlite3
from flask import request, g

app = Flask(__name__)
DATABASE = '/var/www/html/flaskapp/database.db'

app.config.from_object(__name__)
def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])

def insertUser(firstname, lastname, idd, email, stuOrg, classs, orgName, hours, desc, numStudents, comment):
    con = connect_to_database()
    cur = con.cursor()
    cur.execute("SELECT id from person;")
    ids = cur.fetchall()
    if idd not in ids:
        cur.execute("INSERT INTO person VALUES (?, ?, ?, ?, ?, ?)", (idd, firstname, lastname, email, classs, stuOrg))
    cur.execute("INSERT INTO service VALUES (?, ?, ?, ?, ?, ?)",  (orgName, hours, desc, numStudents, comment, idd))
    con.commit()
    con.close()

def retrieve():
    con = connect_to_database()
    cur = con.cursor()
    cur.execute("SELECT * FROM person, service WHERE person.id = service.id")
    users = cur.fetchall()
    con.close()
    return users


@app.route('/view', methods=['GET'])
def get():
    data = retrieve()
    return render_template("retrieve.html", data=data)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        idd = request.form['id']
        email = request.form['email']
        stuOrg = request.form['stuOrg']
        classs = request.form['class']
        orgName = request.form['orgName']
        hours = request.form['hours']
        desc = request.form['desc']
        numStudents = request.form['numStudents']
        comment = request.form['comment']
        insertUser(firstname, lastname, int(idd), email, stuOrg, classs, orgName, float(hours), desc, int(numStudents), comment)        
        return render_template('layout.html')
    else:
        return render_template('layout.html')

if __name__ == '__main__':
    app.run()
