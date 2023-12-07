# -------------------------------------------
#
# CMPSC 487 W - Project 3
# Zachary Newman
#
# -------------------------------------------


# -=- Import Statements -=-


from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
import os
from werkzeug.utils import secure_filename

# -=- Global Variables and Initialization


app = Flask(__name__) # Flask Initialization

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'ztn5011SQL'
app.config['MYSQL_DB'] = 'maintenanceSystem'
mysql = MySQL(app)
print("Connected to Database\n")

img = os.path.join('static','Image')

app.config['UPLOAD'] = img


# -=- Back-End Functions -=-


def loginValidate(username, password):
    crsr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT password,type FROM users WHERE username = %s"
    sqlInput = (username,)
    crsr.execute(sql,sqlInput)
    output = crsr.fetchone() #Obtain the type of the user. None if they don't exist
    if((output is not None) and (output['password'] != password)):
        output = None
    crsr.close()
    return output
# End of Login Validate


def addRequest(aNum, loc, desc, image):
    crsr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = "INSERT INTO requests (apartment_number, problem_area, description, time_date, photo, status) VALUES (%s,%s,%s,%s,%s,%s)"
    timedate = datetime.now()
    print(timedate)
    sqlInput = (aNum, loc, desc, timedate, image, "Pending")
    crsr.execute(sql,sqlInput)
    mysql.connection.commit()
# End of Add Request


def getTenantInfo(username):
    crsr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT * FROM tenants WHERE username = %s"
    sqlInput = (username,)
    crsr.execute(sql,sqlInput)
    output = crsr.fetchone()
    crsr.close
    return output
# End of Get Tenant Info


def getUserInfo(username):
    crsr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = "SELECT * FROM user WHERE username = %s"
    sqlInput = (username,)
    crsr.execute(sql,sqlInput)
    output = crsr.fetchone()
    crsr.close
    return output
# End of Get User Info


def browseRequests(aNumF, areaF, dateStartF, dateEndF, statusF, default):
    crsr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if(default): # Default Value for testing
        sql = "Select * FROM requests"
        crsr.execute(sql)
        requests = crsr.fetchall()
        crsr.close
        return requests

    aNumF = "%" + aNumF + "%"
    areaF = "%" + areaF + "%"
    statusF = "%" + statusF + "%"
    
    if(dateStartF == "" and dateEndF == ""):
        print(1)
        sql = "Select * FROM requests WHERE apartment_number like %s AND problem_area like %s AND status like %s"
        sqlInput = (aNumF, areaF, statusF)
        crsr.execute(sql,sqlInput)
    elif(dateStartF == ""):
        print(2)
        sql = "Select * FROM requests WHERE apartment_number like %s AND problem_area like %s AND time_date <= %s AND status like %s"
        sqlInput = (aNumF, areaF, dateEndF, statusF)
        crsr.execute(sql,sqlInput)
    elif(dateEndF == ""):
        print(3)
        sql = "Select * FROM requests WHERE apartment_number like %s AND problem_area like %s AND time_date >= %s AND status like %s"
        sqlInput = (aNumF, areaF, dateStartF, statusF)
        crsr.execute(sql,sqlInput)
    else:
        print(4)
        sql = "Select * FROM requests WHERE apartment_number like %s AND problem_area like %s AND time_date >= %s AND time_date <= %s AND status like %s"
        sqlInput = (aNumF, areaF, dateStartF, dateEndF, statusF)
        crsr.execute(sql,sqlInput)
        
    requests = crsr.fetchall()
    print(requests)
    crsr.close
    return requests
# End of Browse Requests


def completeRequest(request_ID):
    crsr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if(request_ID != ""):
        sql = "UPDATE requests SET status = %s WHERE request_ID = %s"
        sqlInput = ("Completed",request_ID)
        crsr.execute(sql,sqlInput)
        mysql.connection.commit()
        crsr.close
        return True
#End of Complete Request


def browseTenants():
    crsr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = "Select * FROM tenants"
    crsr.execute(sql)
    requests = crsr.fetchall()
    crsr.close
    return requests
# End of Browse Tenants


def moveTenant(tenantID,aNum): 
    crsr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if(tenantID != "" and aNum != ""):
        sql = "UPDATE tenants SET apartment_number = %s WHERE tenant_ID = %s"
        sqlInput = (aNum, tenantID)
        crsr.execute(sql,sqlInput)
        mysql.connection.commit()
        crsr.close
        return True
# End of Move Tenant


def deleteTenant(tenantID): 
    crsr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if(tenantID != ""):
        sql = "DELETE FROM tenants WHERE tenant_ID = %s"
        sqlInput = (tenantID,)
        crsr.execute(sql,sqlInput)
        mysql.connection.commit()
        crsr.close
        return True
    else:
        return False
# End of Delete Tenant



def addTenant(tenantID, username, password, name, phoneNum, email, inDate, outDate, aNum):
    crsr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # Verify that no other tenant has the same userName or tenantID
    sql = "SELECT * FROM tenants WHERE tenant_ID = %s OR username = %s"
    sqlInput = (tenantID, username)
    crsr.execute(sql,sqlInput)
    output = crsr.fetchall()
    if(output == ()):
        # Username and tenantID are unused
        return True
    else:
        return False
# End of Add Tenant


# -=- FLASK Stuff -=-


@app.route('/', methods =['GET', 'POST'])
def loginpage():
    feedback = ""
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        output = loginValidate(username, password)
        if (output is None):
            feedback = "Incorrect Login Information"
            return render_template('loginpage.html',feedback=feedback)
        else:
            userType = output['type']
            if(userType == "T"):
                # Tenant Page
                return redirect(url_for('tenantpage',username=username))
            elif(userType == "S"):
                # Staff Page
                return redirect(url_for('staffpage'))
            elif(userType == "M"):
                # Manager Page
                return redirect(url_for('managerpage'))
            else:
                feedback = "Incorrect Login Information"
                render_template('loginpage.html',feedback=feedback)
    return render_template('loginpage.html',feedback=feedback)
# End of loginpage


@app.route('/tenant/<username>', methods =['GET', 'POST'])
def tenantpage(username):
    feedback = ""
    output = getTenantInfo(username)
    name = output['name']
    if request.method == 'POST':
        # Attempt to add to add a request
        loc = request.form['loc']
        description = request.form['description']
        imageFile = request.files['imageFile']
        image = secure_filename(imageFile.filename)

        if(loc != "" and description != ""):
            aNum = output['apartment_number']
            addRequest(aNum, loc, description, image)
            if(image != ""):
                imageFile.save(os.path.join(app.config['UPLOAD'], image))
            feedback = "Add Successful"
        else:
            feedback = "Add Unsuccessful"
    return render_template('tenantpage.html',name=name,feedback=feedback)
# End of tenantpage


@app.route('/staff', methods =['GET', 'POST'])
def staffpage():
    if (request.method == 'POST' and 'complete' in request.form):
        # Mark request as Complete
        requestID = request.form['complete']
        completeRequest(requestID)
    elif request.method == 'POST':
        # Filter requests
        aNum = request.form["aNum"]
        area = request.form["area"]
        startDate = request.form["startDate"]
        endDate = request.form["endDate"]
        status = request.form["status"]
        requests = browseRequests(aNum,area,startDate,endDate,status,False)
        return render_template('staffpage.html', requests=requests)
    requests = browseRequests("","","","","",True)
    return render_template('staffpage.html', requests=requests)
# End of staffpage


@app.route('/manager/view', methods =['GET', 'POST'])
def managerpage():
    if(request.method == 'POST' and 'move' in request.form):
        # Move tenant
        tenantID = request.form['move']
        aNum = request.form['moveNum']
        moveTenant(tenantID, aNum)
    elif(request.method == 'POST' and 'delete' in request.form):
        # Delete tenant
        tenantID = request.form['delete']
        deleteTenant(tenantID)
    tenants = browseTenants()
    return render_template('managerpage.html',tenants=tenants)
# End of managerpage


@app.route('/manager/add', methods =['GET', 'POST'])
def addpage():
    feedback = ""
    if(request.method == 'POST'):
        # Attempt to add a Tenant
        tenantID = request.form['tenantID']
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        phoneNum = request.form['phoneNum']
        email = request.form['email']
        inDate = request.form['checkInDate']
        outDate = request.form['checkOutDate']
        aNum = request.form['aNum']
        result = addTenant(tenantID, username, password, name, phoneNum, email, inDate, outDate, aNum)
        if(result):
            feedback = "Tenant Added Successfully"
        else:
            feedback = "Unable to Add Tenant"
    return render_template('addpage.html',feedback=feedback)
# End of addpage

if __name__ == '__main__': # "Main" Method
    app.run()
# End of "Main" method
