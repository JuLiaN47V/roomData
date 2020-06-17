# data
Project to get current temperatur/humidity and past five hours inside a postgresDB and a flaskApplication which is connected to a `frontendSocket` to display the current dataset for each room live.
  
## espServerSocket ##
socket server to get data from ESP8266's and writes them into database  
  
## interval-Temperatur/Humidity ##
writes every hour the current temperatur into database to get the temperatur of the last 5 hours.  
Each needs a crontab  
  
## webDisplay ##
Flask application to display current temperatur and humidity for each room with sensor live.
  
## frontendServerSocket ##
socket server to handle update events on database where clients(Flask, Android App) can connect to.  
Only sends data if something has changed inside the database.
  
## Get Started ##
First you need a postgresDB, with a user called `sensors` with all privileges, a database called `sensors` and these tables with columns:  
> room_tempts: id(SERIAL PRIMARYKEY), room(varchar), current_temp(varchar), hours_0_temp(varchar), hours_1_temp(varchar), hours_2_temp(varchar), hours_3_temp(varchar), hours_4_temp(varchar), hours_number(varchar)  
  
> room_hums: id(SERIAL PRIMARYKEY), room(varchar), current_hum(varchar), hours_0_hum(varchar), hours_1_hum(varchar), hours_2_hum(varchar), hours_3_hum(varchar), hours_4_hum(varchar), hours_number(varchar)  
  
Next clone this repo.  
`git clone https://github.com/JuLiaN47V/roomData`  
Next navigate to 'productive'.  
`cd roomData/productive`  
***Make sure, in each file you have to change the credentials!!!***  
***For each room you first have to create a row in each table with the correct room name!!!***  
put `DHT11.ino` onto your ESP module.  
Next you need to create a symbolic link for each `Interval`-File into a executable path.  
Then create a crontab for each `Interval`-File.  
`0 * * * * temperaturInterval >/dev/null 2>&1`  
Following you have to start both socket server.  
`python3 espServerSocket.py`  
`python3 frontendServerSocket.py`  
Last you have to start the flask app.
`cd flaskClient`
`python3.7 app.py`
