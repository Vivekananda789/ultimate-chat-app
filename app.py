import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Track online users and rooms
online_users = {}
rooms = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    username = data['username']
    room = data.get('room', 'general')

    join_room(room)
    if room not in rooms:
        rooms[room] = set()
    rooms[room].add(username)
    online_users[username] = room

    # Broadcast join event
    emit('user_joined', {
        'username': username,
        'room': room,
        'online_users': list(rooms[room])
    }, room=room)

    # Update user count
    emit('update_user_count', {
        'count': len(rooms[room]),
        'online_users': list(rooms[room])
    }, room=room)

@socketio.on('leave')
def handle_leave(data):
    username = data['username']
    room = online_users.get(username)

    if room:
        leave_room(room)
        rooms[room].discard(username)
        online_users.pop(username, None)

        # Broadcast leave event
        emit('user_left', {
            'username': username,
            'room': room,
            'online_users': list(rooms[room])
        }, room=room)

        # Update user count
        emit('update_user_count', {
            'count': len(rooms[room]),
            'online_users': list(rooms[room])
        }, room=room)

@socketio.on('message')
def handle_message(data):
    room = data.get('room', 'general')
    emit('message', data, room=room)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
