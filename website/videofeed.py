#!/usr/bin/python
'''
Creates the videofeed that takes frames from the camera
Reference: https://github.com/log0/video_streaming_with_flask_example
'''

from flask import Flask, render_template, Response
from camera import VideoCamera

app = Flask(__name__)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5003')
