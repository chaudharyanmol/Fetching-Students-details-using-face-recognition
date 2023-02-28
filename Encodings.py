#!/usr/bin/env python
import cv2
import face_recognition
import os
import glob
import shutil


source_dir= r'C:\xampp\htdocs\Anmol Project\newImages'
destination_dir= r'C:\xampp\htdocs\Anmol Project\imageAttendance'
for jpgfile in glob.iglob(os.path.join(source_dir,"*.jpg")):
    shutil.copy(jpgfile , destination_dir)                         #copying the image present in newImage folder to imageAttendance folder

image=[]
classnames_List=[]
img_path='newImages'
my_List=os.listdir(img_path)

for x in my_List:
    curImg=cv2.imread(f'{img_path}/{x}')
    image.append(curImg)
    classnames_List.append(os.path.splitext(x)[0])

def findencoding(images):
    encode_List=[]
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encode_List.append(encode)
    return encode_List

encode_List_Known=findencoding(image)   #encodeListKnown is a list of lists

with open("encoding.txt", "a") as f:  #if new student registeres his encoding value will be appended in the encoding text file
    for i in encode_List_Known:
       for k in i:
         f.write(str(k)+"\n")


for file in os.listdir(source_dir):
    file_path=os.path.join(source_dir,file)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)   #deleting the image from newImage folder so that there is no duplicate encoding in the text file when next student is registered
    except Exception as e:
        print("")