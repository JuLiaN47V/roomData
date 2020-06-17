import pgpubsub
import psycopg2
import socket
from _thread import *
import threading
import json
import time

conn = psycopg2.connect(user='sensors', database='sensors', password='sensors', host='XXXX')
cur = conn.cursor()
pubsub = pgpubsub.connect(user='sensors', database='sensors', password='sensors', host='XXXX')
pubsub.listen('UPDATE_TEMP')
pubsub.listen('UPDATE_HUM')
host = ""
data = {"rowID": "", "room": "", "value": "", "type": ""}
dataJson = ""
port = 12345
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5)
event = threading.Event()
lock = threading.Lock()


def threaded(c):
    while True:
        event.wait()
        try:
            c.send(dataJson)
        except BrokenPipeError:
            lock.release()
            event.clear()
            break
        try:
            lock.release()
        except RuntimeError:
            pass
        event.clear()


def clientAccept():
    while True:
        c, addr = s.accept()
        start_new_thread(threaded, (c,))


clients = threading.Thread(target=clientAccept)
clients.start()

while True:
    for e in pubsub.events():
        if e[1] == "update_temp":
            cur.execute("SELECT id, room, current_temp FROM room_tempts WHERE room = %s", (e.payload,))
            dbOutput = cur.fetchone()
            data["rowID"] = dbOutput[0]
            data["room"] = dbOutput[1]
            data["value"] = dbOutput[2]
            data["type"] = "temp"
            lock.acquire()
            dataJson = json.dumps(data).encode()
            event.set()
        elif e[1] == "update_hum":
            cur.execute("SELECT id, room, current_hum FROM room_hums WHERE room = %s", (e.payload,))
            dbOutput = cur.fetchone()
            data["rowID"] = dbOutput[0]
            data["room"] = dbOutput[1]
            data["value"] = dbOutput[2]
            data["type"] = "hum"
            lock.acquire()
            dataJson = json.dumps(data).encode()
            event.set()
