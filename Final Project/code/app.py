import ibm_boto3
from ibm_botocore.client import ClientError, Config
from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re





# Constants for IBM COS values
COS_ENDPOINT = "https://s3.jp.tok.cloud-object-storage.appdomin.cloud" # Current list avaiable at https://control.cloud-object-storage.cloud.ibm.com/v2/endpoints
COS_API_KEY_ID = "LWGNzbVTji5V5MG0Doq4jy-Lr4CaAntqoeX6Eh9LMf7T" # eg "W00YixxxxxxxxxxMB-odB-2ySfTrFBIQQWanc--P3byk"
COS_INSTANCE_CRN = "crn:v1:bluemix:public:iam-identity::a/c2c7b865995e48f082d98cc5bb07e3e1::serviceid:ServiceId-3921a51c-3155-4709-b889-8b111dfd3532" # eg "crn:v1:bluemix:public:cloud-object-storage:global:a/3bf0d9003xxxxxxxxxx1c3e97696b71c:d6f04d83-6c4f-4a62-a165-696756d63903::"

# Create resource
cos = ibm_boto3.resource("s3",
    ibm_api_key_id=COS_API_KEY_ID,
    ibm_service_instance_id=COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=COS_ENDPOINT
)
###################################################
app = Flask(__name__)
app.secret_key='a';  


conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=2d46b6b4-cbf6-40eb-bbce-6251e6ba0300.bs2io90l08kqb1od8lcg.databases.appdomain.cloud;PORT=32328;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=yhz29794;PWD=9CZ26CLv18tpSPkT",'','')

@app.route('/login',methods=['GET','POST'])   
def login():  
    global userid
    msg=''

    if request.method == 'POST':
        username=request.form['username']
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
            session['id']=account['USERNAME']
            userid=account['USERNAME']
            session['username']=account['USERNAME']
            return render_template('dashboard.html', msg = msg)
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
def multi_part_upload(bucket_name,iteam_name,file_path):
    try:
        part_size=1024  * 1024 *5
        
        file_threshold=1024 * 1024 *15

        transfre_config=ibm_boto3.s3.transfer.TransferConfig(

            multipart_threshold=file_threshold,
            multipart_chunksize=part_size
        )

        with open(file_path,"rb") as file_data:
            cos.Object(bucket_name,iteam_name).upload_fileobj(
                Fileobj=file_data,
                Config=transfre_config

            )

    except ClientError as be:
        print("client error :[0]\n".format(be))
    except Exception as e:
        print("unable to complete upload")



######################################
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

        bucket='resumes-storage'
        file_name=request.form['email']
        file=request.files['resume']
        multi_part_upload(bucket,file_name,file.filename)
       



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
   
    return render_template('display.html')

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


