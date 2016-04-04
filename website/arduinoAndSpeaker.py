#!/usr/bin/env python
from flask import Flask, render_template, Response
import serial
import time
import threading
import pyttsx

ser = serial.Serial('/dev/ttyACM0', 9600)

app = Flask(__name__)

auto = True
def manualMode():
    global auto
    auto = False
    time.sleep(30)
    auto = True

def speaker(msg):
    engine = pyttsx.init()
    engine.say(msg)
    engine.startLoop()
    engine.endLoop()


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

@app.route('/automove/<direction>')
def move(direction):
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

@app.route('/speakeralert/<msg>')
def speakeralert(msg):
    thread = threading.Thread(target=speaker, args=([msg]))
    thread.start()
    return msg

if __name__ == '__main__':
    app.debug = True
    #app.run()
    app.run(host='0.0.0.0',port=5001, debug=True)
