
from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter
import numpy as np
from tkinter import simpledialog
from tkinter import filedialog
import os
import cv2
import pymysql
import time

main = tkinter.Tk()
main.title("Webcam application to scan QR Code for Employee Attendance") #designing main screen
main.geometry("1300x1200")

global emp_id, present_date
emp_id = "none"

def addAttendance(eid):
    output = "Error in marking attendance"
    status = 0
    dd = str(time.strftime('%Y-%m-%d'))
    exists = 0
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'qrattendance',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select * FROM addemp where emp_id='"+eid+"'")
        rows = cur.fetchall()
        for row in rows:
            exists = 1
            break
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'qrattendance',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select * FROM attendance where emp_id='"+eid+"' and presence_days='"+dd+"'")
        rows = cur.fetchall()
        for row in rows:
            status = 1
            output = "Attendance already marked for Employee ID : "+eid+" for todays date "+dd
            break
    if status == 0 and exists == 1:
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'qrattendance',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO attendance(emp_id,presence_days) VALUES('"+eid+"','"+dd+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        output = "Attendance saved in database"
    if status == 1:
        output = "Attendance already marked"
    if exists == 0:
        output = "Wrong QR code. Emp does not exists"
    return output

def runWebCam():
    global emp_id, present_date
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    while True:
        _, img = cap.read()
        data, bbox, _ = detector.detectAndDecode(img)
        if bbox is not None:
            for i in range(len(bbox)):
                cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255, 0, 0), thickness=2)
        if data and data != emp_id:
            output = addAttendance(data)
            emp_id = data
            messagebox.showinfo(output, output)
        cv2.imshow("QR Code Scanner", img)
        if cv2.waitKey(1) == ord("q"):
            break    
    cap.release()
    cv2.destroyAllWindows()        
            
def exit():
    main.destroy()

font = ('times', 13, 'bold')
title = Label(main, text='Webcam application to scan QR Code for Employee Attendance')
title.config(bg='LightGoldenrod1', fg='medium orchid')  
title.config(font=font)           
title.config(height=3, width=120)       
title.place(x=0,y=5)

font1 = ('times', 12, 'bold')
text=Text(main,height=20,width=100)
scroll=Scrollbar(text)
text.configure(yscrollcommand=scroll.set)
text.place(x=480,y=100)
text.config(font=font1)


font1 = ('times', 12, 'bold')
uploadButton = Button(main, text="Start Webcam", command=runWebCam)
uploadButton.place(x=50,y=100)
uploadButton.config(font=font1)  

exitButton = Button(main, text="Exit", command=exit)
exitButton.place(x=50,y=150)
exitButton.config(font=font1) 


main.config(bg='OliveDrab2')
main.mainloop()
