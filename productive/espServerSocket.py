#!/usr/bin/python3
import socket
import threading
import re
import psycopg2

def dht11sensor(temp, hum, room):
     connection = psycopg2.connect(user="sensors",
                                  password="sensors",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="sensors")
     cursor = connection.cursor()
     cursor.execute("SELECT t.room, t.current_temp, h.current_hum FROM room_tempts AS t JOIN room_hums AS h ON t.room = h.room WHERE t.room = %s;", (room,))
     lastData = cursor.fetchall()
     for lastDate in lastData:
         if temp != lastDate[1]:
             cursor.execute("UPDATE room_tempts SET current_temp = %s WHERE room = %s", (temp, room))
             cursor.execute("NOTIFY UPDATE_TEMP, %s", (room,))
         if hum != lastDate[2]:
             cursor.execute("UPDATE room_hums SET current_hum = %s WHERE room = %s", (hum, room))
             cursor.execute("NOTIFY UPDATE_HUM, %s", (room,))
     connection.commit()
     connection.close()



def addDatabaseData(data):
    hum = ""
    temp = ""
    room = ""
    sensorType = ""
    values = re.findall("\w+\s\w+\.?\w+", data)
    for value in values:
        if "room" in value.split(" ")[0]:
            room = value.split(" ")[1]
        elif "temp" in value.split(" ")[0]:
            temp = value.split(" ")[1]
        elif "hum" in value.split(" ")[0]:
            hum = value.split(" ")[1]
        elif "type" in value.split(" ")[0]:
            sensorType = value.split(" ")[1]
    if sensorType == "DHT11":
        dht11sensor(temp, hum, room)

def dataHandler(client):
    while True:
        content = client.recv(1024)
        addDatabaseData(str(content))


s = socket.socket()
s.bind(('0.0.0.0', 8090))
s.listen()
string = ""
while True:
    count = 0
    client, addr = s.accept()
    recvHandler = threading.Thread(target=dataHandler, args=(client,))
    recvHandler.start()
