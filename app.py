from flask import Flask, render_template, request
from flask_socketio import SocketIO, send, join_room, leave_room

app = Flask(__name__)
socketio = SocketIO(app)

users_online = set()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def handle_join(data):
    username = data['username']
    room = data['room'] if data['room'] else 'general'
    join_room(room)
    users_online.add(username)
    socketio.emit('server_message', {'msg': f'{username} has joined the room.'}, room=room)
    socketio.emit('update_users', {'count': len(users_online), 'users': list(users_online)})

@socketio.on('message')
def handle_message(msg):
    socketio.emit('chat_message', msg, room=msg['room'])

@socketio.on('disconnect')
def handle_disconnect():
    for user in list(users_online):
        users_online.remove(user)
    socketio.emit('update_users', {'count': len(users_online), 'users': list(users_online)})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
