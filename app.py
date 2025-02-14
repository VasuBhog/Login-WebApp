from flask import Flask, flash, redirect, render_template, request, Response, session, url_for, send_file
import mysql.connector 
from mysql.connector import errorcode
from werkzeug.utils import secure_filename
import os

#Upload file
UPLOAD_FOLDER = '/Users/vasubhog/Login-WebApp/uploads'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.debug = True
app.secret_key = os.urandom(12)
app.config['UPLOAD FOLDER'] = UPLOAD_FOLDER

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

    #Download
    if request.method == 'POST' and request.form['action'] == 'Download':
        username = session['username']
        password = session['password']
        cursor.execute(user_query, (username, password))
        print("Downloading file")
        # query = "SELECT file FROM user WHERE username = '%s'"
        # cursor.execute(query,(username))
        # print("sql run")
        result = cursor.fetchone()
        if result:
            filename = result[5]
            filecontent = result[6]
            print("Filename: " + filename)
            print("Filecontent: " + filecontent)
            #Create new file
            newfile = open(filename,'w') 
            newfile.write(filecontent)
            newfile.close()
            newfile = open(filename,'r')
            print("IN FILE")
            
            return Response(
                    newfile,
                    mimetype="text/csv",
                    headers={"Content-disposition":
                    'attachment; filename=test.txt'})
        else:
            print("NOT DOWNLOADING")
            pass

    #USER LOGSOUT
    if request.method == 'POST' and request.form['action'] == 'Logout':
        print("User Logout")
        close_session()
        session['logged_in'] = False
        msg="You have been logged out"
        return render_template("login.html",msg=msg)

    #UPLOAD FILE button pressed
    if request.method == 'POST' and request.form['action'] == 'Upload':
        username = session['username']
        password = session['password']
        print("USER UPLOAD")
        
        file = request.files.get('file')
        content = file.read()
        filecontent = content.decode("utf-8")
        #Calculate num words
        num = filecontent.split()
        wordcount = len(num)
        filename = secure_filename(file.filename)

        #insert filename query
        update_filename(username,filename)

        #insert file query
        update_file(username,filecontent)
        
        #insert wordcount query
        update_wordcount(username,wordcount)

        session['filename'] = filename
        session['filecontent'] = filecontent
        session['wordcount'] = wordcount
        
        #FILE EXISTS then output session upload to homepage
        if file:
            cursor.execute(user_query, (username, password))
            account = cursor.fetchone()
            print(account)
            if account:
                username = account[0]
                password = account[1]
                firstname = account[2]
                lastname = account[3]
                email = account[4]
                filecontent = session['filecontent']
                wordcount = session['wordcount']
                filename = session['filename']
                print(file)
                print(wordcount)
                #create download link
                newfile = open(filename,'w+')
                returnfile = newfile.write(filecontent)
                session['returnfile'] = returnfile
                
                #inserts word count to database
                return render_template("home.html",firstname=firstname,lastname=lastname,email=email,filename=filename,wordcount=wordcount)
    
    #Checks Logged in session
    if not session.get('logged_in'):
        return render_template('login.html')
    #When user logs in
    else:
        #WHEN USER LOGS BACK IN FRESH SESSION
        print("Logged In")
        username = session['username']
        password = session['password']
        cursor.execute(user_query, (username, password))
        account = cursor.fetchone()
        if account:
            username = account[0]
            password = account[1]
            firstname = account[2]
            lastname = account[3]
            email = account[4]
            filename = account[5]
            filecontent = account[6]
            wordcount = account[7]
            print("ACCOUNT:")
            print(username,password,firstname,lastname,email)
            return render_template("home.html",firstname=firstname,lastname=lastname,email=email,filename=filename,wordcount=wordcount)
    return home()
        

def close_session():
    [session.pop(key) for key in list(session.keys())]

#Login Page
#Checks to see which button the user presses
@app.route("/login", methods=['GET','POST'])
def login():
    msg = ''
    """ GET - display
        POST - login """
    if request.method == 'POST' and request.form['action'] == 'Register':
        return render_template("register.html")

    if request.form["username"] == '' or request.form['password'] == '' and request.form['action'] == 'Login':
        msg = "Please enter Username and Password"
        return render_template('login.html',msg=msg)
    
    

    if request.method == 'POST' and request.form['action'] == 'Login' and 'username' in request.form and 'password' in request.form:
        userdetails = request.form
        username = userdetails['username']
        password = userdetails['password']
        args = (username, password)
        
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
            session['logged_in'] = False
            return render_template('login.html',msg=msg)
    

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

def update_filename(username, filename):
    query = "UPDATE user SET filename = %s WHERE username = %s"
    args = (filename, username)
    cursor.execute(query,args)
    mydb.commit()

def update_wordcount(username, wordcount):
    query = "UPDATE user SET wordcount = %s WHERE username = %s"
    args = (wordcount, username)
    cursor.execute(query,args)
    mydb.commit()

def update_file(username, content):
    query = "UPDATE user SET file = %s WHERE username = %s"
    args = (content, username)
    cursor.execute(query,args)
    mydb.commit()

# def get_download(username):
    
    


if __name__ == "__main__":
    app.run()

