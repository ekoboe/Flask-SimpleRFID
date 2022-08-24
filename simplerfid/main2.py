from flask import Flask, request, flash, session, url_for, redirect, render_template
import time
#from w1thermsensor import W1ThermSensor
import time
#import board
#import adafruit_dht

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#import RPi.GPIO as GPIO
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(26, GPIO.OUT)
#GPIO.output(26, True)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rfid.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class user(db.Model):
    text = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True)
    
    
db.create_all()

@app.route("/")
def login():
    return render_template('login.html')

@app.route("/register")
def register():
    return render_template('register.html')

@app.route("/index")
def index():
    #sensor = W1ThermSensor()
    #dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)
    
    #while True:
        #try:
            #temp = sensor.get_temperature()
            #temp_c = dhtDevice.temperature
            #print(temp_c)
            #temp_f = temp_c * (9 / 5) + 32
            #humi = dhtDevice.humidity
        
        #except RuntimeError as error:
            #print(error.args[0])
            #time.sleep(5)
            #continue
        
        cahaya = 0
            
        return render_template('sensor2.html',temp=23,temp_c=30,humi=45, nutrisi=367, cahaya=cahaya) #status=GPIO.input(26))
    



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")