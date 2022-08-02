# FaceAttendanceSystem
This mini project is build for marking attendance using face data.
The face is detected using haar cascade classifier
When the face is registered it creates 128 measurement of each face image 
During attendance 128 measurement of the faces detected by camera is compared with known 128 measurement of faces which has been taken during registration 
if the measurement is similar the attendance marked.
The detection and recognization of face is done with the help of openCV library.
The database is created using mySQL.
The gui is made using pyQT5
