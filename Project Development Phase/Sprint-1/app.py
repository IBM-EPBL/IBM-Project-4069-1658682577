
import re

import ibm_db
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key='a';  


conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=2d46b6b4-cbf6-40eb-bbce-6251e6ba0300.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32328;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=yhz29794;PWD=9CZ26CLv18tpSPkT",'','')

@app.route('/login',methods=['GET','POST'])   
def login():  
    global userid
    msg=''

    if request.method == 'POST':
        username=request.form['email']
        password=request.form['password']
        sql="SELECT * FROM user WHERE usernam=? AND password=?"
        stmt=ibm_db.prepar(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['loggedin']=True
            session['email']=account['email']
            userid=account['email']
            session['username']=account['email']
            return render_template('dashbord.html')
        else:
            msg='incorrect id/password'
    return render_template('login.html',msg=msg)    

    
#######################################################

@app.route('/register',methods=['GET','POST'])
def register():
    msg = ''
    if request.method == 'POST' :
        fitstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        sql = "SELECT * FROM user WHERE email =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', password):
            msg = 'passwrod must contain characters and numbers !'
        else:
            insert_sql = "INSERT INTO  user VALUES (?, ?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, fitstname)
            ibm_db.bind_param(prep_stmt, 2, lastname)
            ibm_db.bind_param(prep_stmt, 3, email)
            ibm_db.bind_param(prep_stmt, 4, password)
            ibm_db.execute(prep_stmt)
            return render_template('set profile.html',)
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)

#########################################
@app.route('/setprofile',methods=['GET','POST'])
def setprofile():
    msg = ''
    if request.method == 'POST' :
        fitstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        college = request.form['college']
        qulification = request.form['qulification']
        decription = request.form['decription']
        skills= request.form['skills']
        interest= request.form['interest']
        sql = "SELECT * FROM profile WHERE email =?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
       
        else:
            insert_sql = "INSERT INTO  profile VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, fitstname)
            ibm_db.bind_param(prep_stmt, 2, lastname)
            ibm_db.bind_param(prep_stmt, 3, email)
            ibm_db.bind_param(prep_stmt, 4, college)
            ibm_db.bind_param(prep_stmt, 5, qulification)
            ibm_db.bind_param(prep_stmt, 6, decription)
            ibm_db.bind_param(prep_stmt, 7, skills)
            ibm_db.bind_param(prep_stmt, 8, interest)
            ibm_db.execute(prep_stmt)
            return render_template('dashbord.html')
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('set profile.html', msg = msg)

##################################
@app.route('/display')
def display():
    print(session["username"],session['id'])
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM profile WHERE userid = % s', (session['id'],))
    account = cursor.fetchone()
    print("accountdislay",account)

    
    return render_template('display.html',account = account)

#######################################

@app.route('/logout')

def logout():
   session.pop('loggedin', None)
   session.pop('email', None)
   
   return render_template('login.html')
   ############################

@app.route('/dashbord')
def dash():
    
    return render_template('dashbord.html')

###################

if __name__ =='__main__':  
    app.run(debug = True)  


