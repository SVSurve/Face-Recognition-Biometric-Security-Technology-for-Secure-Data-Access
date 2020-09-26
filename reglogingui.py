from tkinter import *
import os
import cv2
import numpy as np;
import xlwrite,firebase.firebase_ini as fire;
import time
import sys
import webbrowser
import subprocess
from playsound import playsound
from datetime import datetime;
 
def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("300x250") 
    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()
 
    Label(register_screen, text="Please enter details below").pack()
    Label(register_screen, text="").pack()
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Register", width=10, height=1, command = register_user).pack()
  
def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()
 
    global username_verify
    global password_verify
 
    username_verify = StringVar()
    password_verify = StringVar()
 
    global username_login_entry
    global password_login_entry
 
    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command = login_verify).pack()
 
def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
        
def register_user():
 
    username_info = username.get()
    password_info = password.get()
 
    file = open(username_info, "w")
    file.write(username_info + "\n")
    file.write(password_info)
    file.close()
 
    username_entry.delete(0, END)
    password_entry.delete(0, END)
 
    Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()
    face_id=(username_info)
    vid_cam = cv2.VideoCapture(0)
    face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    count = 0
    assure_path_exists("dataset/")
    while(True):
        _, image_frame = vid_cam.read()
        gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(image_frame, (x,y), (x+w,y+h), (255,0,0), 2)
            count += 1
            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
            cv2.imshow('frame', image_frame)
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        elif count>=30:
            print("Successfully Captured")
            break
    vid_cam.release()
    os.system("py training_dataset.py")

def recognizer1():
    start=time.time()
    period=8
    face_cas = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0);
    recognizer = cv2.face.LBPHFaceRecognizer_create();
    recognizer.read('trainer/trainer.yml');
    flag = 0;
    id=username1;
    filename='filename';
    dict = {
                'item1': 1
    }
    #font = cv2.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 5, 1, 0, 1, 1)
    font = cv2.FONT_HERSHEY_SIMPLEX
    while True:
        ret, img = cap.read();
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
        faces = face_cas.detectMultiScale(gray, 1.3, 7);
        for (x,y,w,h) in faces:
            roi_gray = gray[y:y + h, x:x + w]
            cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0),2);
            id,conf=recognizer.predict(roi_gray)
            if(conf < 50):
                if(id==1):
                    subprocess.call(["sqlite_web.py","chinook.db"],shell=True)
                
                elif(id==2):
                    open("AI-18.pdf")

                elif(id==3):
                    open("AI-18.pdf")

                elif(id==4):
                    open("AI-18.pdf")

                elif(id==5):
                    open("AI-18.pdf")
                    

            else:
                id = 'Unknown, can not recognize'
                print("Unknown")
                flag=flag+1
                unknown_face()
                break
            
            cv2.putText(img,str(id)+" "+str(conf),(x,y-10),font,0.55,(120,255,120),1)
            
        cv2.imshow('frame',img);
        
        if flag == 10:
            playsound('transactionSound.mp3')
            print("Transaction Blocked")
            break;
        if time.time()>start+period:
            break;
        if cv2.waitKey(100) & 0xFF == ord('q'):
            break;

    cap.release();
    cv2.destroyAllWindows();

    
def login_verify():
    global username1
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)
    list_of_files = os.listdir()
    if username1 in list_of_files:
        file1 = open(username1, "r")
        verify = file1.read().splitlines()
        if password1 in verify:
            recognizer1()
        else:
            password_not_recognised()
    else:
        user_not_found()
 
def  login_success():
    global login_success_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title("Success")
    login_success_screen.geometry("150x100")
    Label(login_success_screen, text="Login Success").pack()
    Button(login_success_screen, text="OK", command=delete_login_success).pack()

def unknown_face():
    global face_not_recognized
    face_not_recognized=Toplevel(login_screen)
    face_not_recognized.title("Success")
    face_not_recognized.geometry("150x100")
    Label(face_not_recognized, text="Face not recognized").pack()
    Button(face_not_recognized, text="EXIT",command=close_all).pack()

def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Success")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_password_not_recognised).pack()
 
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="User Not Found").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()
 
def delete_login_success():
    login_success_screen.destroy()
    
def  close_all():
    face_not_recognized.destroy()
 
def delete_password_not_recognised():
    password_not_recog_screen.destroy()
 
 
def delete_user_not_found_screen():
    user_not_found_screen.destroy()
 
 

 
def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x250")
    main_screen.title("Account Login")
    Label(text="Select Your Choice", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="").pack()
    Button(text="Login", height="2", width="30", command = login).pack()
    Label(text="").pack()
    Button(text="Register", height="2", width="30", command=register).pack()
 
    main_screen.mainloop()
 
 
main_account_screen()
