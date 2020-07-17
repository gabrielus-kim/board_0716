from flask import Flask, render_template, request, session
from flask import abort, redirect
import pymysql
from datetime import datetime

app = Flask(__name__, template_folder='template')

db = pymysql.connect(user = 'root',
                    passwd = 'avante',
                    db = 'web',
                    host = 'localhost',
                    charset = 'utf8',
                    cursorclass = pymysql.cursors.DictCursor)

app.config['ENV'] = 'Development'
app.config['DEBUG'] = True
app.secret_key = 'Who are you?'

def who_am_i():
    return session['user']['name'] if 'user' in session else "Hi ! Everybody~~"
 

@app.route('/')
def index():

    return render_template('template.html',
                            owner = who_am_i())

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        cursor = db.cursor()
        cursor.execute(f"""
            select name from author
            where name = '{request.form['id']}'
        """)
        user = cursor.fetchone()
        if user != None:
            cursor = db.cursor()
            cursor.execute(f"""
                select id, name, password from author
                where name = '{request.form['id']}' and
                    password = SHA2('{request.form['pw']}', 256)
            """)
            user = cursor.fetchone()
            if user != None:
                session['user'] = user
                return redirect('/')
            else:
                title = " 입력하신 Password가 잘못되었읍니다. 다시 입력하세요."
        else:
            title = " 입력하신 login ID 는 등록이 안되어 있읍니다."
    else:
        title = " Please, login first"
    return render_template('login.html',
                            owner = who_am_i(),
                            title = title)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

@app.route('/favicon.ico')
def favicon():
    return abort(404)

app.run(port='8000')