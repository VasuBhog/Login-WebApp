from flask import Flask, flash, redirect, render_template, request, Response, session, abort
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, user_loaded_from_header
import mysql.connector 
from mysql.connector import errorcode
import os

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(12)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:cookie123@localhost/users'
# db = SQLAlchemy(app)

# class User(db.Model):
#     username = db.Column(db.String, primary_key=True)
#     password = db.Column(db.String, unique=True, nullable=False)
#     firstname = db.Column(db.String, unique=True, nullable=False)
#     lastname = db.Column(db.String, unique=True, nullable=False)
#     email = db.Column(db.String, unique=True, nullable=False)
#     authenticated = db.Column(db.Boolean, default=False)

#     def __init__(self, username, password):
#         self.username = username
#         self.password = password

#     def __repr__(self):
#         return '<User %r>' % self.username



#Connect to mysql
mydb = mysql.connector.connect(host='localhost', user='root',password='cookie123', database='users')
mycursor = mydb.cursor()

def insert_user(username, password, firstname,lastname,email):
    
    query = "INSERT INTO user(username,password,firstname,lastname,email) " \
            "VALUES(%s,%s,%s,%s,%s)"
    args = (username, password, firstname,lastname,email)
    mycursor.execute(query,args)
    mydb.commit()
    # mycursor.close()

#Reroutes to home authentication
@app.route("/")
def index():
    return home()

#HomePage
#Starts here with checking if user logs in
@app.route("/home",methods=['GET','POST'])
def home():
    print(session.get('logged_in'))
    #Checks Logged in session
    if not session.get('logged_in'):
        return render_template('login.html')
    #logged in or registered
    else:
        if request.method == 'POST' and 'username' in session:
            print("WHHUYYYY")
            username = session['username']
            password = session['password']
            mycursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password))
            account = mycursor.fetchone()
            print(account)
            if account:
                username = account[0]
                password = account[1]
                firstname = account[2]
                lastname = account[3]
                email = account[4]
                return render_template("home.html",firstname=firstname,lastname=lastname,email=email)
            
        elif request.method == 'POST' and request.form['action'] == 'Logout':
            session['logged_in'] = False
            session.pop('logged_in',None)
            session.pop('username',None)
            session.pop('password',None)
            return home()
        return render_template("home.html", firstname = session['firstname'], lastname = session['lastname'], email = session['email'])


#Login Page
#Checks to see which button the user presses
@app.route("/login", methods=['GET','POST'])
def login():
    msg = ''
    """ GET - display
        POST - login """
    if request.method == 'POST' and request.form['action'] == 'Login' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        session['username'] = username
        session['password'] = password
        mycursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password))
        account = mycursor.fetchone()
        if account:
            session['logged_in'] = True
            return home()
        else:
            msg = 'Incorrect Username/Password'
            render_template('login.html',msg=msg)
    if request.method == 'POST' and request.form['action'] == 'Register':
        return register()

#Registration Form
@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == 'POST':
        if request.form['action'] == 'Submit':
            username = request.form['username']
            password = request.form['password']
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            email = request.form['email']
            mycursor.execute('SELECT * FROM user WHERE username = %s AND password = %s', (username, password))
            account = mycursor.fetchone()
            if account[0] == username:
                return "Username already used"
            else:
                insert_user(username, password, firstname,lastname,email)
                session['username'] = username
                session['password'] = password
                session['firstname'] = firstname
                session['lastname'] = lastname
                session['email'] = email
                session['logged_in'] = True
                return home()
    return render_template("register.html")
    
if __name__ == "__main__":
    app.run()

    # db = SQLAlchemy()

# class User(db.Model):
#     __tablename__ = 'user'
#     username = db.Column(db.String, primary_key=True)
#     password = db.Column(db.String, unique=True, nullable=False)
#     firstname = db.Column(db.String, unique=True, nullable=False)
#     lastname = db.Column(db.String, unique=True, nullable=False)
#     email = db.Column(db.String, unique=True, nullable=False)
#     authenticated = db.Column(db.Boolean, default=False)

#     def is_active(self):
#         return True
#     def get_id(self):
#         return self.username
#     def is_authenticated(self):
#         return self.authenticated
#     def is_anonymous(self):
#         return False