from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, send
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send({'msg': f"{username} has joined the room.", 'timestamp': datetime.now().strftime('%H:%M:%S')}, room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send({'msg': f"{username} has left the room.", 'timestamp': datetime.now().strftime('%H:%M:%S')}, room=room)

@socketio.on('message')
def handle_message(data):
    data['timestamp'] = datetime.now().strftime('%H:%M:%S')
    send(data, room=data['room'])

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
