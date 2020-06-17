from flask_socketio import SocketIO
import psycopg2
from flask import Flask, render_template
import threading
import time
import socket
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'XXXX'
socketio = SocketIO(app)


class Database:
    user = "sensors"
    password = "sensors"
    host = "XXXX"
    database = "sensors"
    conn = None
    cursor = None

    def connect(self):
        self.conn = psycopg2.connect("dbname=" + self.database +
                                     " user=" + self.user +
                                     " password=" + self.password +
                                     " host=" + self.host
                                     )
        self.cursor = self.conn.cursor()

    def getRooms(self):
        self.cursor.execute("SELECT t.id, t.room, t.current_temp, h.current_hum FROM room_tempts AS t JOIN room_hums AS h ON t.id = t.id;")
        data = self.cursor.fetchall()
        return data

    def disconnect(self):
        self.conn.close()

def events():
    HOST = 'XXXX'
    PORT = 12345
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((HOST, PORT))
            except ConnectionRefusedError:
                time.sleep(2)
            else:
                while True:
                    try:
                        s.send("check".encode())
                    except ConnectionResetError:
                        break
                    try:
                        data = s.recv(1024)
                    except ConnectionResetError:
                        break
                    if data is None:
                        pass
                    else:
                        socketio.emit("TableUpdate", data.decode())
                        
@app.route('/')
def hello_world():
    db = Database()
    db.connect()
    date = db.getRooms()
    db.disconnect()
    return render_template('data.html', date=date)


if __name__ == '__main__':
    socketThread = threading.Thread(target=events)
    socketThread.start()
    socketio.run(app, host='0.0.0.0')
