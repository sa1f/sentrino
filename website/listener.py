#!/usr/bin/env python
#
# Project: Video Streaming with Flask
# Author: Log0 <im [dot] ckieric [at] gmail [dot] com>
# Date: 2014/12/21
# Website: http://www.chioka.in/
# Description:
# Modified to support streaming out with webcams, and not just raw JPEGs.
# Most of the code credits to Miguel Grinberg, except that I made a small tweak. Thanks!
# Credits: http://blog.miguelgrinberg.com/post/video-streaming-with-flask
#
# Usage:
# 1. Install Python dependencies: cv2, flask. (wish that pip install works like a charm)
# 2. Run "python main.py".
# 3. Navigate the browser to the local webpage.
from flask import Flask, render_template, Response
import serial

ser = serial.Serial('/dev/ttyACM0', 9600)

app = Flask(__name__)


@app.route('/move/<direction>')
def move(direction):
    if direction == 'up':
        ser.write('u')
    elif direction == 'down':
        ser.write('d')
    elif direction == 'right':
        ser.write('r')
    elif direction == 'left':
        ser.write('l')
    return direction


if __name__ == '__main__':
    app.debug = True
    #app.run()
    app.run(host='192.168.43.179',port=5001, debug=True)
