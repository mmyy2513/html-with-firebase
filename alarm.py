import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

import time
import json
import requests
import socket

# socket init
host = '192.168.1.3'
port = 9999
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

# get time to alarm
alarm = int(db.reference(str(name) + '/medicine').get())
print(alarm)


while True:
    now = time.localtime()
    hour = now.tm_hour
    minute = now.tm_min

    print(hour, type(hour))
    print(minute, type(minute))

    if hour == alarm and minute == 0:
        print("its time")
        # socket 1 send
    else:
        print("not yet")
        # socket 0 send

