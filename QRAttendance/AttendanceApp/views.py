from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
import os
from django.core.files.storage import FileSystemStorage
import pymysql
import datetime
import pyqrcode
import png
from pyqrcode import QRCode

global username

def test(request):
    if request.method == 'GET':
       return render(request, 'test.html', {})

def AdminLoginAction(request):
    global username
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        if username == 'admin' and password == 'admin':
            context= {'data':'welcome '+username}
            return render(request, 'AdminScreen.html', context)
        else:
            context= {'data':'login failed. Please retry'}
            return render(request, 'AdminLogin.html', context)  

def AdminLogin(request):
    if request.method == 'GET':
       return render(request, 'AdminLogin.html', {})

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})  

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def AddEmp(request):
    if request.method == 'GET':
       return render(request, 'AddEmp.html', {})

def ViewEmpAttendanceAction(request):
    if request.method == 'POST':
        empid = request.POST.get('t1', False)
        from_date = request.POST.get('t2', False)
        to_date = request.POST.get('t3', False)
        from_dd = str(datetime.datetime.strptime(from_date, "%d-%b-%Y").strftime("'%Y-%m-%d'"))
        to_dd = str(datetime.datetime.strptime(to_date, "%d-%b-%Y").strftime("'%Y-%m-%d'"))
        presence_days = 0
        salary = 0
        columns = ['Employee ID', 'Presence Date']
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        output += "<tr>"
        for i in range(len(columns)):
            output += "<th>"+font+columns[i]+"</th>"            
        output += "</tr>"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'qrattendance',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select salary FROM addemp where emp_id='"+empid+"'")
            rows = cur.fetchall()
            for row in rows:
                salary = row[0]
                break
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'qrattendance',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * from attendance where emp_id='"+empid+"' and presence_days between "+from_dd+" and "+to_dd)
            rows = cur.fetchall()
            for row in rows:
                presence_days = presence_days + 1
                output += "<tr>"
                output += "<td>"+font+str(row[0])+"</td>"
                output += "<td>"+font+str(row[1])+"</td></tr>"
        output += "<tr><td>"+font+"Number of Presence Days : "+str(presence_days)+"</font><td>"+font+"Total Salary = "+str(((salary/30) * presence_days))+"</td></tr>"        
        context= {'data': output}
        return render(request, 'AdminScreen.html', context)

def ViewEmpAttendance(request):
    if request.method == 'GET':
        font = '<font size="" color="black">'
        output = '<tr><td>'+font+'Choose&nbsp;Employee&nbsp;ID</td><td><select name="t1">'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'qrattendance',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select emp_id FROM addemp")
            rows = cur.fetchall()
            for row in rows:
                output += '<option value="'+row[0]+'">'+row[0]+'</option>'
        output += "</select></td></tr>"
        context= {'data1': output}
        return render(request, 'ViewEmpAttendance.html', context)

def ViewAttendance(request):
    if request.method == 'GET':
        return render(request, 'ViewAttendance.html', {})

def ViewAttendanceAction(request):
    if request.method == 'POST':
        global username
        empid = username
        from_date = request.POST.get('t1', False)
        to_date = request.POST.get('t2', False)
        from_dd = str(datetime.datetime.strptime(from_date, "%d-%b-%Y").strftime("'%Y-%m-%d'"))
        to_dd = str(datetime.datetime.strptime(to_date, "%d-%b-%Y").strftime("'%Y-%m-%d'"))
        presence_days = 0
        salary = 0
        columns = ['Employee ID', 'Presence Date']
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        output += "<tr>"
        for i in range(len(columns)):
            output += "<th>"+font+columns[i]+"</th>"            
        output += "</tr>"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'qrattendance',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select salary FROM addemp where emp_id='"+empid+"'")
            rows = cur.fetchall()
            for row in rows:
                salary = row[0]
                break
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'qrattendance',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * from attendance where emp_id='"+empid+"' and presence_days between "+from_dd+" and "+to_dd)
            rows = cur.fetchall()
            for row in rows:
                presence_days = presence_days + 1
                output += "<tr>"
                output += "<td>"+font+str(row[0])+"</td>"
                output += "<td>"+font+str(row[1])+"</td></tr>"
        output += "<tr><td>"+font+"Number of Presence Days : "+str(presence_days)+"</font><td>"+font+"Total Salary = "+str(((salary/30) * presence_days))+"</td></tr>"        
        context= {'data': output}
        return render(request, 'UserScreen.html', context)    

def ViewEmp(request):
    if request.method == 'GET':
        columns = ['Employee ID', 'Employee Name', 'Contact No', 'Email ID', 'Gender', 'Address', 'Designation', 'Salary']
        output = '<table border=1 align=center width=100%>'
        font = '<font size="" color="black">'
        output += "<tr>"
        for i in range(len(columns)):
            output += "<th>"+font+columns[i]+"</th>"            
        output += "</tr>"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'qrattendance',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM addemp")
            rows = cur.fetchall()
            for row in rows:
                output += "<tr>"
                output += "<td>"+font+str(row[0])+"</td>"
                output += "<td>"+font+str(row[1])+"</td>"
                output += "<td>"+font+str(row[2])+"</td>"
                output += "<td>"+font+str(row[3])+"</td>"
                output += "<td>"+font+str(row[4])+"</td>"
                output += "<td>"+font+str(row[5])+"</td>"
                output += "<td>"+font+str(row[6])+"</td>"
                output += "<td>"+font+str(row[7])+"</td></tr>"
        context= {'data': output}
        return render(request, 'AdminScreen.html', context)

def UserLoginAction(request):
    global username
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        index = 0
        emp_name = None
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'qrattendance',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select emp_id, emp_name FROM addemp")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username:
                    emp_name = row[1]
                    index = 1
                    break		
        if index == 1:
            context= {'data':'welcome '+emp_name}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'login failed. Please retry'}
            return render(request, 'UserLogin.html', context)        

def DownloadAction(request):
    if request.method == 'POST':
        global username
        print("===="+username)
        infile = open("AttendanceApp/static/qrcodes/"+username+".png", 'rb')
        data = infile.read()
        infile.close()       

        response = HttpResponse(data, content_type='image/png')
        response['Content-Disposition'] = 'attachment; filename=%s' % username+".png"
        return response

def AddEmpAction(request):
    if request.method == 'POST':
        global username
        empid = request.POST.get('t1', False)
        empname = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        gender = request.POST.get('t4', False)
        email = request.POST.get('t5', False)
        address = request.POST.get('t6', False)
        designation = request.POST.get('t7', False)
        salary = request.POST.get('t8', False)
        output = "none"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'qrattendance',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select emp_id FROM addemp")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == empid:
                    output = empid+" employee already exists"
                    break
        if output == 'none':
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'qrattendance',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO addemp(emp_id,emp_name,contact_no,gender,email,address,designation,salary) VALUES('"+empid+"','"+empname+"','"+contact+"','"+gender+"','"+email+"','"+address+"','"+designation+"','"+salary+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            url = pyqrcode.create(empid)
            url.png('AttendanceApp/static/qrcodes/'+empid+'.png', scale = 6)
            username = empid
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                output = 'New Employee Details added with Employee ID : '+empid
        context= {'data':output}
        return render(request, 'Download.html', context)
      


