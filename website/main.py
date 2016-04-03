#!/usr/bin/env python
from flask import Flask, render_template, Response
from camera import VideoCamera
import requests
import json
import os.path

app = Flask(__name__)

if not os.path.isfile('info.json'):
    print "Please give information. This will be saved in info.json and used for future requests"
    username = raw_input("Enter your username: ")
    password = raw_input("Enter your passowrd: ")
    did = raw_input("Enter your did number: ")
    dst = raw_input("Enter your destination number: ")
    message = raw_input("Enter your message: ")
    infoIn = {"api_username": username, "api_password": password, "did": did, "dst": dst, "message": message,
            'method' : 'sendSMS'}
    with open('info.json', 'w') as outfile:
        json.dump(infoIn, outfile)

with open('info.json', 'r') as infile:
    global info
    info = json.load(infile)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/alert/<msg>')
def alert(msg):
    info['message'] = msg
    print requests.get('https://voip.ms/api/v1/rest.php', params=info).text

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
