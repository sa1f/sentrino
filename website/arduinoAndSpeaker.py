#!/usr/bin/env python
'''
This file allows the Pi to talk to the Arduino
'''

from flask import Flask, render_template, Response
import serial
import time
import threading
import pyttsx

#The serial connection to the Arduino
ser = serial.Serial('/dev/ttyACM0', 9600)

app = Flask(__name__)

#Manual mode and autonomous mode change
auto = True
def manualMode():
    global auto
    auto = False
    time.sleep(30)
    auto = True

#Default text to speech
def speaker(msg):
    engine = pyttsx.init()
    engine.say(msg)
    engine.startLoop()
    engine.endLoop()

#Text to speech is sent with a set speech rate
def speaking(msg):
    engine = pyttsx.init()
    engine.say(msg)
    engine.setProperty("rate", 30)
    engine.startLoop()
    engine.endLoop()

#Alarm character is sent
def ard():
    ser.write('a')


#Manual Control Mode
@app.route('/move/<direction>')
def move(direction):

    # Non blocking method for switching
    # to manual mode and switching back to auto mode
    # after 30 seconds
    t = threading.Thread(target=manualMode)
    t.start()

    if direction == 'up':
        ser.write('u')
    elif direction == 'down':
        ser.write('d')
    elif direction == 'right':
        ser.write('r')
    elif direction == 'left':
        ser.write('l')
    return direction

#Autonomous Control Mode
@app.route('/automove/<direction>')
def automove(direction):
    if auto:
        if direction == 'up':
            ser.write('u')
        elif direction == 'down':
            ser.write('d')
        elif direction == 'right':
            ser.write('r')
        elif direction == 'left':
            ser.write('l')
        return direction

#Speaker message
@app.route('/speak/<msg>')
def speakthis(msg):
    thread = threading.Thread(target=speaking, args=([msg]))
    thread.start()
    return "hi"

#Alarm initializer
@app.route('/alert/<msg>')
def speakeralert(msg):
    thread = threading.Thread(target=speaker, args=([msg]))
    thread.start()

    ardThread = threading.Thread(target=ard)
    ardThread.start()
    return msg

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5001)
