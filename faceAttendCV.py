from PyQt5.QtWidgets import QApplication, QLineEdit, QMainWindow, QDateEdit, QPushButton,QWidget,QStackedWidget,QLabel,QComboBox
from PyQt5 import uic,QtCore
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QImage,QPixmap
import sys
import cv2
from cvFunc import findEncoding, preProcessing
import os
import mysql.connector
import base64
from datetime import datetime

class UI_Interface(QMainWindow):
    def __init__(self):
        super(UI_Interface, self).__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.logic = 0
        self.capLogic = 0
        uic.loadUi("final.ui", self)

        #Login Window
        self.logWid = self.findChild(QWidget,"loginWidget")
        self.entUser = self.findChild(QLineEdit,"userNameField")
        self.entPass = self.findChild(QLineEdit,"passwordField")
        self.logButton = self.findChild(QPushButton,"loginButton")

        self.mainWid = self.findChild(QWidget,"mainWidget")
        self.mainWid.hide()

        self.loginAuth = {"admin":"admin25"}

        self.logButton.clicked.connect(self.logIn)

        #Capturing StackWidget
        self.stackView = self.findChild(QStackedWidget, "stackedWidget")

        #Capturing Page Switching Button
        self.regButton = self.findChild(QPushButton, "registrationPButton")
        self.regButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.homeButton = self.findChild(QPushButton,"homeButton")
        self.homeButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.takeAttendButton = self.findChild(QPushButton,"takeAttendButton")
        self.takeAttendButton.setFocusPolicy(QtCore.Qt.NoFocus)

        #Capturing RegisterPage Widget and it's Component
        self.newRegPage = self.findChild(QWidget, "registrationPage")
        self.studId = self.findChild(QLineEdit,"studentIdEnt")
        self.studRollNo = self.findChild(QLineEdit,"rollEnt")
        self.studDiv = self.findChild(QLineEdit,"divEnt")
        self.studFName = self.findChild(QLineEdit,"firstNEnt")
        self.studLName = self.findChild(QLineEdit,"lastNEnt")
        self.studDob = self.findChild(QDateEdit,"dobEnt")
        self.studDob.setCalendarPopup(True)
        self.imgLabel = self.findChild(QLabel,"imgLabel")
        self.genderBox = self.findChild(QComboBox,"genderBox")
        self.deptBox = self.findChild(QComboBox,"departmentBox")
        self.yearBox = self.findChild(QComboBox,"yearBox")
        self.studEmail = self.findChild(QLineEdit,"emailEnt")
        self.register = self.findChild(QPushButton,"registerButton")
        self.startCamButton = self.findChild(QPushButton,"startCamButton")
        self.captureButton = self.findChild(QPushButton,"CaptureButton")
        self.captureButton.setDisabled(True)
        self.register.setDisabled(True)

        #Capturing HomePage Widget and it's Component
        self.homePage = self.findChild(QWidget,"homePage")

        #Capturing TakeAttendancePage Widget and it's Component
        self.takeAttendPage = self.findChild(QWidget,"takeAttendance")
        self.startCapButton = self.findChild(QPushButton,"startCapButton")
        self.stopCapButton = self.findChild(QPushButton,"stopCapButton")
        self.attendCapLabel = self.findChild(QLabel,"attendCapLabel")

        #Connecting Button
        self.homeButton.clicked.connect(self.homeSwitch)
        self.regButton.clicked.connect(self.regSwitch)
        self.takeAttendButton.clicked.connect(self.takeAttendSwitch)
        self.startCapButton.clicked.connect(self.onCap)
        self.stopCapButton.clicked.connect(self.stopCap)
        self.startCamButton.clicked.connect(self.startCam)
        self.captureButton.clicked.connect(self.capImage)
        self.register.clicked.connect(self.registerStudent) 

        #ComboBox Setup
        self.genderBox.addItems(["Male","Female","Other"])
        self.deptBox.addItems(["Computer","IT","Electronic","Civil","Chemical"])
        self.yearBox.addItems(["F.E","S.E","T.E","B.E"])

        # Attendance Setup
        self.path = "Faces"
        self.images = []
        self.studName = []
        self.myList = os.listdir(self.path)
        for student in self.myList:
            currImg = cv2.imread(f"{self.path}/{student}")
            self.images.append(currImg)
            self.studName.append(os.path.splitext(student)[0])
   
        self.encodeListKnown = findEncoding(self.images)
        print("Encoding Completed")

        #Show Page
        self.show()

    # Switch to home page
    def homeSwitch(self):
        print("Home Page")
        self.stackView.setCurrentWidget(self.homePage)

    # Switch to registration page
    def regSwitch(self):
        print("Registration Page")
        self.stackView.setCurrentWidget(self.newRegPage)

    # Switch to take Attendance page
    def takeAttendSwitch(self):
        print("Take Attendance Page")
        self.stackView.setCurrentWidget(self.takeAttendPage)
    
    # Start Camera for Registering Face
    def startCam(self):
        self.captureButton.setDisabled(False)
        cap = cv2.VideoCapture(0)
        while(cap.isOpened()):
            succuss,frame = cap.read()
            if succuss == True:
                self.displayImage(frame,self.imgLabel,1)
                cv2.waitKey()
                if self.capLogic == 1:
                    cv2.imwrite(f'D:\CODEFACERECOG\Faces\{self.studId.text()}.jpg',frame)
                    self.capLogic = 0
                    break
        cap.release()
        cv2.destroyAllWindows()

    def registerStudent(self):
        self.captureButton.setDisabled(True)
        self.register.setDisabled(True)
        mydb = mysql.connector.connect(
        host="localhost", user="root", passwd="*******", database="faceattend"
        )
        try:
            studId = self.studId.text()
            studRollNO = self.studRollNo.text()
            studDiv = self.studDiv.text()
            studFName = self.studFName.text()
            studLName = self.studLName.text()
            studDob = str(self.studDob.date())
            index = studDob.index("(")
            studDob = studDob[index+1:-1].split(", ")
            studDob = datetime(int(studDob[0]),int(studDob[1]),int(studDob[2]))
            studYear = self.yearBox.currentText()
            studGen = self.genderBox.currentText()[0]
            studDept = self.deptBox.currentText()
            studEmail = self.studEmail.text()
            studImage = open(f'D:\CODEFACERECOG\Faces\{studId}.jpg','rb').read()
            studImage = base64.b64decode(studImage)   
        except Exception as e:
            print(e)
        
        mycursor = mydb.cursor()
        sqlForm = "INSERT INTO student(student_id, division, roll_no, fname, lname, dob, gender, department, year, emial_id, pic) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"

        try:
            students = [(studId,studDiv,studRollNO,studFName,studLName,studDob,studGen,studDept,studYear,studEmail,studImage)]
            mycursor.execute(sqlForm, students[0])
            mydb.commit()
        except Exception as e:
            print(e)

    # Capture the Face and Recognize it      
    def onCap(self):
        cap = cv2.VideoCapture(0)
        while(cap.isOpened()):
            success, frame = cap.read()
            if success == True:
                preProcessing(frame,self.encodeListKnown,self.studName)
                self.displayImage(frame,self.attendCapLabel,1)
                cv2.waitKey()
                if self.logic == 1:
                    self.logic = 0
                    break
        cap.release()
        cv2.destroyAllWindows()

    def capImage(self):
        self.register.setDisabled(False)
        self.capLogic = 1

    def stopCap(self):
        self.logic = 1

    # Display Image in Label
    def displayImage(self,img,label,window=0):
        qformat = QImage.Format_Indexed8

        if len(img.shape) == 3:
            if(img.shape[2]) == 4:
                qformat = QImage.Format_RGBA888
            else:
                qformat = QImage.Format_RGB888
        img = QImage(img,img.shape[1],img.shape[0],qformat)
        img = img.rgbSwapped()
        label.setPixmap(QPixmap.fromImage(img))
        label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def logIn(self):
        uname = self.entUser.text()
        if(self.loginAuth.get(uname) == self.entPass.text()):
            print("Successfully Login")
            self.logWid.hide()
            self.mainWid.show()
        else:
            print("Unsuccesfull Login")

    def mousePressEvent(self, event):
        self.oldPosition = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPosition)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPosition = event.globalPos()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    interface = UI_Interface()
    # Run the app
    app.exec_()
