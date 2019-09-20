from flask import Flask, flash, redirect, render_template, request, Response, session, abort
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, user_loaded_from_header
import mysql.connector 
from mysql.connector import errorcode
import os

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(12)

#Connect to mysql
mydb = mysql.connector.connect(host='localhost', user='root',password='cookie123', database='users')
mydb.autocommit = True
cursor = mydb.cursor(buffered=True)

#Queries
user_query = ('SELECT * FROM user WHERE username = %s AND password = %s')

#Reroutes to home authentication
@app.route("/")
def index():
    return home()

#HomePage
#Starts here with checking if user logs in
@app.route("/home",methods=['GET','POST'])
def home():
    msg =''
    print("User logged in:")
    print(session.get('logged_in'))
    #Checks Logged in session
    if not session.get('logged_in'):
        return render_template('login.html')
    #logged in or registered
    else:
        print("Logged In")
        username = session['username']
        password = session['password']
        print(username)
        if 'logged_in' == True:
            ("Start")
            cursor.execute(user_query, (username, password))
            account = cursor.fetchone()
            if account:
                username = account[0]
                password = account[1]
                firstname = account[2]
                lastname = account[3]
                email = account[4]
                print(username,password,firstname,lastname,email)
                return render_template("home.html",firstname=firstname,lastname=lastname,email=email)
        elif request.method == 'POST' and request.form['action'] == 'Logout':
            print("User Logout")
            close_session()
            session['logged_in'] = False
            session.pop('logged_in',None)
            session.pop('username',None)
            session.pop('password',None)
            msg="You have been logged out"
            return render_template("login.html",msg=msg)
        return render_template("home.html", firstname = session['firstname'], lastname = session['lastname'], email = session['email'])
    return home()

# @app.route("/logout",methods=["GET"])
# @login_required
# def logout():
#     user = current_user
#     user.authe
def close_session():
    [session.pop(key) for key in list(session.keys())]

#Login Page
#Checks to see which button the user presses
@app.route("/login", methods=['GET','POST'])
def login():
    msg = ''
    """ GET - display
        POST - login """
    if request.method == 'POST' and request.form['action'] == 'Login' and 'username' in request.form and 'password' in request.form:
        userdetails = request.form
        username = userdetails['username']
        password = userdetails['password']
        args = (username,password)
        
        cursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', args)
        account = cursor.fetchone()
        if account:
            session['username'] = username
            session['password'] = password
            session['logged_in'] = True
            return home()
        else:
            print("TESTSETSETSTTSETESTSE")
            msg = 'Incorrect Username/Password'
            session['logged_in'] = True
            render_template('login.html',msg=msg)
    if request.method == 'POST' and request.form['action'] == 'Register':
        return render_template("register.html")

#Registration Form
@app.route("/register",methods=['GET','POST'])
def register():
        if request.method == 'POST' and request.form['action'] == 'Submit':
            msg = ''
            userdetails = request.form
            username = userdetails['username']
            password = userdetails['password']
            args = (username,password)
            cursor.execute(user_query,args)
            result = cursor.fetchone()
            if result:
                msg = "Username already exists"
                return render_template('register.html',msg=msg)
            else: 
                firstname = userdetails['firstname']
                lastname = userdetails['lastname']
                email = userdetails['email']
                session['username'] = username
                session['password'] = password
                session['firstname'] = firstname
                session['lastname'] = lastname
                session['email'] = email
                session['logged_in'] = True
                insert_user(username, password, firstname,lastname,email)
                return render_template("home.html", firstname = session['firstname'], lastname = session['lastname'], email = session['email'])
            return home()

#insert users to table
def insert_user(username, password, firstname,lastname,email):
    query = "INSERT INTO user(username,password,firstname,lastname,email) " \
            "VALUES(%s,%s,%s,%s,%s)"
    args = (username, password, firstname,lastname,email)
    cursor.execute(query,args)
    mydb.commit()
    # cursor.close()

if __name__ == "__main__":
    app.run()

