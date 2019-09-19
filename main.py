from flask import Flask
from flask import Flask, flash, redirect, render_template, request, Response, session, abort
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
cache = Cache(app)
# db = SQLAlchemy(app)

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String, unique=True, nullable=False)
#     email = db.Column(db.String, unique=True, nullable=False)

# db.session.commit()

#Reroutes to home authentication
@app.route("/")
def index():
    return home()

#HomePage
#Starts here with checking if user logs in
@app.route("/home",methods=['POST'])
def home():
    print(session.get('logged_in'))
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if request.method == 'POST':
            if request.form['action'] == 'Logout':
                    session['logged_in'] = False
                    print(session.get('logged_in'))
                    return render_template('login.html')
        return render_template("home.html")


#Login Page
#Checks to see which button the user presses
@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        if request.form['action'] == 'Login':
            if request.form['username'] == 'admin' or request.form['password'] == 'admin':
                session['logged_in'] = True
            else:
                flash("Wrong Username or Password")
            return home()
        if request.form['action'] == 'Register':
            return register()

#Registration Form
@app.route("/register",methods=['POST'])
def register():
    if request.method == 'POST':
        if request.form['action'] == 'Submit':
            session['logged_in'] = True
            return home()
    return render_template("register.html")
    
if __name__ == "__main__":
    cache.clear()
    app.secret_key = os.urandom(12)
    app.run(debug=True)