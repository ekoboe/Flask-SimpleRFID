from flask import Flask, request, flash, session, url_for, redirect, render_template
import time
import time
import board
import adafruit_dht

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(19, GPIO.OUT)

led1Sts = GPIO.input(17)
led2Sts = GPIO.input(18)
led3Sts = GPIO.input(19)
    
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rfid.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class users(db.Model):
    text = db.Column(db.String)
    id = db.Column(db.Integer, primary_key=True)
    
db.create_all()

@app.route("/")
def login():
    return render_template('login.html')

@app.route("/baca")
def baca():
    global users
    id, text = reader.read()
    users = users.query.filter_by(id=id).first()
    if not users:
        flash('Please check your login details and try again.')
        return render_template('login.html')
    else:
        session['username'] = users.text
        return redirect(url_for('index'))

@app.route("/register")
def register():
    return render_template('register.html')

@app.route('/daftar', methods=['POST'])
def daftar():
    global users
    text = request.form.get('text')
    reader.write(text)
    id, nm = reader.read()
    
    user = users.query.filter_by(id=id).first()
    
    if user:
        flash("Kartu telah terdaftar")
        return redirect(url_for('login'))
        
    try:
        new_user = users(text=text, id=id)
        db.session.add(new_user)
        db.session.commit()
        flash("Success")
    except:
        flash("Gagal Registrasi")
    
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route("/index")
def index():
    dhtDevice = adafruit_dht.DHT22(board.D21, use_pulseio=False)
    
    while True:
        try:
            temp_c = dhtDevice.temperature
            print(temp_c)
            humi = dhtDevice.humidity
        
        except RuntimeError as error:
            print(error.args[0])
            time.sleep(2)
            continue
        
        led1Sts = GPIO.input(17)
        led2Sts = GPIO.input(18)
        led3Sts = GPIO.input(19)
            
        return render_template('sensor2.html',temp=23,temp_c=temp_c,humi=humi, nutrisi=367, led1=led1Sts, led2=led2Sts, led3=led3Sts) #status=GPIO.input(26))
    
@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    
    if deviceName == "led1":
        actuator = 17
    if deviceName == "led2":
        actuator = 18
    if deviceName == "led3":
        actuator = 19
    
    if action == "on":
        GPIO.output(actuator, GPIO.HIGH)
    if action == "off":
        GPIO.output(actuator, GPIO.LOW)
    
    led1Sts = GPIO.input(17)
    led2Sts = GPIO.input(18)
    led3Sts = GPIO.input(19)
    
    templateData = {
        'led1' : led1Sts, 
        'led2' : led2Sts,
        'led3' : led3Sts,
        }
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0")