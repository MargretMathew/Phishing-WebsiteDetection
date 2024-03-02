import os
import phishing_detection
from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask import jsonify
from werkzeug.utils import secure_filename
import sqlite3 as sql


app = Flask(__name__)

app.secret_key="myapp"
#code for connection
#conn = sql.connect('phishing_url.db')

#index Page
@app.route('/')
def index():
    return render_template('index.html')

#admin Login Page
@app.route('/admin_login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        return redirect(url_for('index'))
    return render_template('admin_login.html')

#user Login Page
@app.route('/user_login', methods=['GET','POST'])
def user_login():
    if request.method == 'POST':
        return redirect(url_for('index'))

    return render_template('user_login.html')

#user Registration
@app.route('/user_reg', methods=['GET','POST'])
def user_reg():
    if request.method == 'POST':
        return redirect(url_for('index'))

    return render_template('user_reg.html')

#user Registration Action
@app.route('/user_reg_db', methods=['GET','POST'])
def user_reg_db():
    msg=''
    if request.method=='POST':
        try:
            #passing HTML form data into python variable
            fname = request.form['fName']
            sname = request.form['sName']
            contact = request.form['PhoneNumber']
            email = request.form['Email']
            address=request.form['Address']
            uname=request.form['uName']
            password=request.form['password']
            #creating variable for connection
            with sql.connect("phishing_url.db") as con:
                print ("Opened database successfully")
                cur = con.cursor()
                print ("Opened database successfully")
                cur.execute("INSERT INTO users (f_name,s_name,contact,email,username,password,usr_type,address)VALUES (?,?,?,?,?,?,?,?)",(fname,sname,contact,email,uname,password,'User',address))
                print ("Opened database successfully")
                con.commit()
                msg = "Data Entered Sucessfully "
        except:
            con.rollback()
            msg = "error in insert operation"
    
        finally:
            return redirect(url_for('user_reg', msg=msg))
            con.close()

#Login Action
@app.route('/user_login_db', methods=['GET','POST'])
def user_login_db():
    msg=''
   
    #passing HTML form data into python variable
    uname=request.form['username']
    password=request.form['password']
    #creating variable for connection
    with sql.connect("phishing_url.db") as con:
        print ("Opened database successfully")
        cur = con.cursor()
        print ("Opened database successfully")
        cur.execute("SELECT * FROM users WHERE username=? AND password=?",(uname,password))
        print ("Opened database successfully")
        rows=cur.fetchone()
        if rows:
            if rows[7]=='User':
                session['loggedin']=True
                session['id']=rows[0]
                session['username']=rows[5]
                session['user_type']=rows[7]
                return render_template('user_index.html')
            if rows[7]=='Admin':
                session['loggedin']=True
                session['id']=rows[0]
                session['username']=rows[5]
                session['user_type']=rows[7]
                return render_template('admin_index.html')
    return render_template('index.html')

###################################################
#User Sections
#User Profile
@app.route('/profile', methods=['GET','POST'])
def profile():
    u_id=int(session['id'])
    print(u_id)
    with sql.connect("phishing_url.db") as con:
        #print ("Opened database successfully")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE id='{}'".format(u_id))
        #pened database successfully")
        rows=cur.fetchone()
        if rows:
            return render_template('profile.html',u_id=rows[0],f_name=rows[1],s_name=rows[2],contact=rows[3],email=rows[4],address=rows[8])

#User Url Testing Page
@app.route('/webTest', methods=['GET','POST'])
def webTest():
    return render_template('webTest.html')

#User Phishing Testing
@app.route('/result', methods=['GET','POST'])
def result():
    urlname  = request.form['url_link']
    result,whois_response,rank_checker_response,global_rank,url,domain  = phishing_detection.getResult(urlname)
    print("Result: ", result)
    return render_template('webTest.html',result_set=result,urlname=urlname,whois_response=whois_response,rank_checker_response=rank_checker_response,global_rank=global_rank,url=url,domain=domain)


#User Feedback
@app.route('/feedback', methods=['GET','POST'])
def feedback():
    return render_template('feedback.html')

#User Feedback Action
@app.route('/feedback_db', methods=['GET','POST'])
def feedback_db():
    u_id=int(session['id'])
    feedback=request.form['feedback']
    try:
        with sql.connect("phishing_url.db") as con:
            print ("Opened database successfully")
            print (feedback)
            cur = con.cursor()
            cur.execute("INSERT INTO feedbacks(feedback,u_id) VALUES (?,?)",(feedback,u_id))
            print("pened database successfully")
            con.commit()
    except:
            con.rollback()
            msg = "error in insert operation"
    
    finally:
        return redirect(url_for('feedback'))
        con.close()    

#User Blacklist Request
@app.route('/blacklist_request', methods=['GET','POST'])
def blacklist_request():
    u_id=int(session['id'])
    url_link=request.form['url_link']
    try:
        with sql.connect("phishing_url.db") as con:
            print ("Opened database successfully")
            print (feedback)
            cur = con.cursor()
            cur.execute("INSERT INTO blacklist(blacklist_url,u_id) VALUES (?,?)",(url_link,u_id))
            print("pened database successfully")
            con.commit()
    except:
            con.rollback()
            msg = "error in insert operation"
    
    finally:
        return redirect(url_for('request_blacklist'))
        con.close()  
    return render_template('blacklist_request.html')


#User Blacklist Request
@app.route('/request_blacklist', methods=['GET','POST'])
def request_blacklist():
    return render_template('blacklist_request.html')
#######################################################

#Admin Pages
#Admin View User
@app.route('/view_user', methods=['GET','POST'])
def view_user():
    with sql.connect("phishing_url.db") as con:
        #print ("Opened database successfully")
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE usr_type='User'")
        #pened database successfully")
        rows=cur.fetchall()
        
        if rows:
            return render_template('view_user.html',elements=rows)

#Admin Add Black List
@app.route('/add_blacklist', methods=['GET','POST'])
def add_blacklist():
    return render_template('add_blacklist.html')

#Admin Add Black List Action
@app.route('/add_blacklist_db', methods=['GET','POST'])
def add_blacklist_db():
    u_id=int(session['id'])
    url_link=request.form['url_link']
    try:
        with sql.connect("phishing_url.db") as con:
            print ("Opened database successfully")
            cur = con.cursor()
            print(u_id)
            cur.execute("INSERT INTO blacklist(blacklist_url,u_id) VALUES (?,?)",(url_link,u_id))
            print("pened database successfully")
            con.commit()
    except:
            con.rollback()
            msg = "error in insert operation"
    
    finally:
        return redirect(url_for('add_blacklist'))
        con.close()  

#Admin View Black List
@app.route('/view_blacklist', methods=['GET','POST'])
def view_blacklist():
    with sql.connect("phishing_url.db") as con:
        print ("Opened database successfully")
        cur = con.cursor()
        cur.execute("SELECT * FROM blacklist")
        print("pened database successfully")
        rows=cur.fetchall()
        if rows:
            return render_template('view_blacklist.html',elements=rows)
    
#Admin View Feedback
@app.route('/view_feedbacks', methods=['GET','POST'])
def view_feedbacks():
     with sql.connect("phishing_url.db") as con:
        print ("Opened database successfully")
        cur = con.cursor()
        cur.execute("SELECT * FROM feedbacks")
        print("pened database successfully")
        rows=cur.fetchall()
        if rows:
            return render_template('view_feedbacks.html',elements=rows)

#Logout
@app.route('/logout', methods=['GET','POST'])
def logout():
    if id in session:
        session.pop(id,None)
        return render_template('index.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
