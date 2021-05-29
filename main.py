from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, emit, join_room

import cv2
import base64
import io
from PIL import Image
import numpy as np
import uuid

from canvas import canvas
from utils import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

@app.route("/", methods = ['POST', 'GET'])
def home():
    if request.method == 'GET':
        return render_template("home.html")
    else:
        name = request.form['name']
        room = request.form['room']
        roomId = request.form['roomId']
        if room == "new":
            return render_template("host.html", name=name, roomId=str(uuid.uuid4()))
        else:
            return render_template("viewer.html", name=name, roomId=roomId)

@app.route("/room")
def host():
    return render_template("host.html")

socketio = SocketIO(app)

@socketio.on('join-room')
def joinroom(data):
    name = data["name"]
    roomId = data["roomId"]
    join_room(roomId)
    emit('joined', name, room=roomId)

@socketio.on('message')
def message(data):
    name = data["name"]
    roomId = data["roomId"]
    msg = data["msg"]
    emit('msg', {"name": name, "msg": msg}, room=roomId)
    

@socketio.on('capture')
def handleCapture(data):
    img = data["data_uri"]
    roomId = data["roomId"]
    cv_image = buf_to_img(img)
    canvas.processCapture(cv_image)
    paintWindow = canvas.get_paintWindow()
    frame = canvas.get_frame()
    frame_string = img_to_buff(frame)
    canvas_string = img_to_buff(paintWindow)
    emit('new-canvas', canvas_string, room=roomId)
    emit('new-frame', frame_string)


if __name__ == '__main__':
    socketio.run(app)