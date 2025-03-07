import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app)

# Track online users
online_users = set()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    username = data['username']
    room = data.get('room', 'general')

    join_room(room)
    online_users.add(username)

    # Notify room of new user
    socketio.emit('user_joined', {'username': username, 'online_users': list(online_users)}, room=room)
    socketio.emit('update_user_count', {'count': len(online_users)})

@socketio.on('leave')
def handle_leave(data):
    username = data['username']
    room = data.get('room', 'general')

    leave_room(room)
    if username in online_users:
        online_users.remove(username)

    # Notify room of user leaving
    socketio.emit('user_left', {'username': username, 'online_users': list(online_users)}, room=room)
    socketio.emit('update_user_count', {'count': len(online_users)})

@socketio.on('message')
def handle_message(data):
    room = data.get('room', 'general')
    socketio.emit('message', data, room=room)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
