from cv2 import exp
import numpy as np
import cv2
import face_recognition
import mysql.connector
from datetime import datetime
import smtplib
from datetime import datetime
import os
# Mark Attendance In CSV File
def markAttendance(studId):
    mydb = mysql.connector.connect(
    host="localhost", user="root", passwd="*******", database="faceattend"
    )
    cursor = mydb.cursor()
    query = f"select student_id, department, year, division, roll_no, fname, lname, emial_id from student where student_id = '{studId}'"
    cursor.execute(query)
    data = cursor.fetchall()
    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login("*****@gmail.com", "*******")
    except Exception as e:
        print(e)
    date = datetime.now()
    dt = date.strftime("%d_%m_%Y")
    fileName = f"Attendance_{dt}.csv"
    fileList = os.listdir()
    flag = False
    for file in fileList:
        if(file==fileName):
            flag = True
    if flag==True:
        with open(fileName,"r+") as f:
            attendData = f.readlines()
            studIdList = []
            for line in attendData:
                entry = line.split(",")
                studIdList.append(entry[0])
            if studId not in studIdList:
                mydb = mysql.connector.connect(
                host="localhost", user="root", passwd="*******", database="faceattend"
                )
                cursor = mydb.cursor()
                query = f"select student_id, department, year, division, roll_no, fname, lname, emial_id from student where student_id = '{studId}'"
                cursor.execute(query)
                data = cursor.fetchall()[0]
                now = datetime.now()
                dt = now.strftime("%H:%M:%S")
                f.writelines(f'\n{data[0]},{data[1]},{data[2]},{data[3]},{data[4]},{data[5]},{data[6]},{dt}')
                try:
                    server.sendmail("******@gmail.com", f"{data[7]}", "Your Attendance is marked")
                except Exception as e:
                    print(e)
        f.close()
        try:
            server.quit()
        except Exception as e:
            print(e)
    else:
        f = open(fileName,'w')
        f.writelines(f"Student Id, Department, Year, Division, Roll NO, First Name, Last Name, Time")
        f.close()

def findEncoding(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        except Exception as e:
            print(e)
    return encodeList

def preProcessing(img,encodeListKnown,studName):
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    facesCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS,facesCurFrame) 

    for encodeFace, faceLoc in zip(encodeCurFrame,facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
        matchIndex = np.argmin(faceDis)     
        if matches[matchIndex]:
            name = studName[matchIndex].upper()
            print(name)
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markAttendance(name)
            
