import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import time
import json
import requests
import socket

# socket init
host = '192.168.1.3'
port = 9800
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
s.bind((host,port))
s.listen()
conn, addr = s.accept()

# firebase init
cred = credentials.Certificate('xavier-557c6-firebase-adminsdk-lst73-6995cf776e.json')
firebase_admin.initialize_app(cred,{
    'databaseURL' : 'https://xavier-557c6-default-rtdb.firebaseio.com/'
})

# get name
data = db.reference().get()
name = next(iter(data.keys()))

meal_cnt = 0
medicine_cnt = 0

while True:
    # get time to alarm
    medicine_alarm = int(db.reference(str(name) + '/medicine').get())
    medicine_alarm = str(medicine_alarm)
    meal_alarm = int(db.reference(str(name) + '/meal').get())
    meal_alarm = str(meal_alarm)

    
    mdc_hour = medicine_alarm[:-2]
    mdc_min = medicine_alarm[-2:]
    meal_hour = meal_alarm[:-2]
    meal_min = meal_alarm[-2:]


    now = time.localtime()
    hour = now.tm_hour
    minute = now.tm_min

    
    if hour == int(mdc_hour) and minute == int(mdc_min):
        if medicine_cnt == 0:
            conn.send("1".encode())
            medicine_cnt = 1
            while True:
                if conn.recv(1024): break
        else :
            conn.send("0".encode())
            while True:
                if conn.recv(1024): break
    else:
        
        medicine_cnt = 0
        conn.send("0".encode())
        while True:
            if conn.recv(1024): break

    if hour == int(meal_hour) and minute == int(meal_min):
        if meal_cnt == 0:
            conn.send("2".encode())
            meal_cnt = 1
            while True:
                if conn.recv(1024): break
        else :
            conn.send("0".encode())
            while True:
                if conn.recv(1024): break
    else:
        
        meal_cnt = 0
        conn.send("0".encode())
        while True:
            if conn.recv(1024): break

