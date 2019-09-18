from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_caching import Cache
import os

app = Flask(__name__)
cache = Cache(app)

@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' or request.form['password'] == 'admin':
            session['logged_in'] = False
        else:
            flash("Wrong Username or Password")
    return render_template('home.html')

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/")
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template("home.html")

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template("login.html")

    
if __name__ == "__main__":
    cache.clear()
    app.secret_key = os.urandom(12)
    app.run(debug=True)