from flask import Flask, render_template
from flask_cors import CORS
import cv2
import numpy as np
import face_recognition
import os
import datetime
import mysql.connector
import glob

application = Flask(__name__)
CORS(application)
cors = CORS(application, resources={r"/*": {"origins": "*"}})

img_path='imageAttendance' #folder where all the images of registered students are saved
image=[]
classnames=[]
classUniqueId=[]  #List that stores Unique Id of student
classname_list=[] #List that stores Names of Student
my_List= os.listdir(img_path)

for x in my_List:
    curImg=cv2.imread(f'{img_path}/{x}')
    image.append(curImg)
    classnames.append(os.path.splitext(x)[0])

for y in classnames:
    data= y.split(" ",1)
    classUniqueId.append(data[0])  #separating id and name from photo name
    classname_list.append(data[1])


def markAttendances(name): #Function to mark attendance in database
            con=mysql.connector.connect(host="localhost" , user='root' , database="studentdb") #connecting to MySql
            cursor=con.cursor()
            dt_now=datetime.datetime.now()  #recording the current time
            dt_StringY=dt_now.strftime("%D %H:%M:%S")
            dt_String = dt_StringY.split(" ") #spliting the string
            sql=("INSERT INTO attendance (Name, Date, Time) " #Inserting date time and name in sql database
            "VALUES (%s,%s,%s)")
            com=(name,dt_String[0],dt_String[1])
            cursor.execute(sql,com)
            con.commit()


def get_Details(name): #Function to fetch the details from database
    my_db = mysql.connector.connect(host="localhost", user="root", database="studentdb") #connecting to database
    my_cursor = my_db.cursor()
    my_cursor.execute("Select * from studentdetails")
    my_result = my_cursor.fetchall() #fetching all rows of the table
    for r in my_result:
        if name in r[1]: #if name is in row then return that row
            return(r)



encode_List_Known=[] #List of List to store the encoding values
with open("encoding.txt", "r") as f: #Reading the encoding text file
     while True:
      lines = f.readline()
      if(lines==''):
         break
      encodes=[]
      encodes.append(float(lines))
      for i in range(127):
         lines = f.readline()
         encodes.append(float(lines))
      encode_List_Known.append(encodes)


@application.route("/")
def helloworld():
    while True:
        row=0
        image_dir = 'uploads' #Floder where the Live Scanned Picture will get uploaded
        data_path = os.path.join(image_dir, '*g')
        files = glob.glob(data_path)
        for k in files:
            img = cv2.imread(k) #reading the image
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        face_Curr = face_recognition.face_locations(img)
        encode_Curr = face_recognition.face_encodings(img, face_Curr)

        for enf, floc in zip(encode_Curr, face_Curr):
            matches = face_recognition.compare_faces(encode_List_Known, enf)
            faceDis = face_recognition.face_distance(encode_List_Known, enf)

            matchIndex = np.argmin(faceDis)
            min = np.amin(faceDis)

            if matches[matchIndex]:
                #print(min)

                name = classname_list[matchIndex].upper()

                if (min < 0.5100000000000000):  # Threshold value

                    row = get_Details(name) #calling the getDetails and markAttendance functions
                    markAttendances(name)
                   # print(row)
                    #print(name)

        if(row):
            return render_template("MainPage.html", data=row)  #if person is registered then displaying the main page
        else:
            return render_template("NoRecord.html")  #else asking the admin to get the student registered


application.run("localhost", port=5000, debug=True)