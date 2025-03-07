from flask import Flask, render_template, request, redirect, url_for
from flask_socketio import SocketIO, send, join_room, leave_room
from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app)

users_online = set()  # Store unique online users

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    username = data['username']
    room = data.get('room', 'general')
    join_room(room)
    users_online.add(username)

    socketio.emit('user_joined', {
        'username': username,
        'timestamp': datetime.now().strftime('%H:%M:%S'),
        'online_users': list(users_online)
    }, room=room)

@socketio.on('message')
def handle_message(msg):
    send(msg, broadcast=True)

@socketio.on('exit')
def handle_exit(data):
    username = data['username']
    users_online.discard(username)
    socketio.emit('user_left', {
        'username': username,
        'online_users': list(users_online)
    })

if __name__ == '__main__':
    socketio.run(app)
