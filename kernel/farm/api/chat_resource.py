# -*- coding: utf-8 -*-



from flask import Blueprint, request, jsonify
from flask_restful import Api
from flask_socketio import emit
from farm.models import Chat, Message
from farm.services import ChatServices
from datetime import datetime

from farm import socketio, db

chat_api = Blueprint("chat_api", __name__)
chat_services = ChatServices(socketio)


# Сокеты
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('send_message')
def handle_send_message(data):
    chat_id = data['chat_id']
    message_owner = data['message_owner']
    text = data['text']

    chat_services = ChatServices(socketio)
    message_id = chat_services.send_message(chat_id, message_owner, text)

    if message_id:
        emit('message_sent', {'message_id': message_id}, room=chat_id)

# Роутеры
@chat_api.route('/chat', methods=['POST'])
def create_chat():
    data = request.get_json()
    user_1 = data.get('user_1')
    user_2 = data.get('user_2')

    chat_id = chat_services.create_chat(user_1, user_2)

    return {'chat_id': chat_id}, 201

@chat_api.route('/message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()

        chat_id = data.get('chat_id')
        message_owner = data.get('message_owner')
        text = data.get('text')

        message_id = chat_services.send_message(chat_id, message_owner, text)

        print(f"Received message: chat_id={chat_id}, message_owner={message_owner}, text={text}")
        print(f"Message saved with id: {message_id}")

        if message_id is not None:
            emit('message_sent', {'message_id': message_id}, room=str(chat_id))  # Use str() to convert chat_id to a string

        return {'message_id': message_id}, 201
    except Exception as e:
        print(f"Error: {e}")
        raise


@chat_api.route('/get_history/<int:chat_id>', methods=['GET'])
def get_history(chat_id):
    chat = Chat.query.get(chat_id)

    if not chat:
        return jsonify({"error": "Chat not found"}), 404

    # Extract messages from the chat
    messages = [{"id": message.id, "owner": message.message_owner, "text": message.text, "sendtime": str(message.sendtime)} for message in chat.messages]

    return jsonify({"chat_id": chat.id, "messages": messages})

@chat_api.route('/mark_as_read', methods=['POST'])
def mark_as_read():
    data = request.get_json()
    chat_id = data.get('chat_id')
    message_id = data.get('message_id')

    if chat_services.mark_message_as_read(chat_id, message_id):
        emit('marked_as_read', {'message_id': message_id}, room=chat_id)
        return {'status': 'success'}, 200

    return {'status': 'error'}, 404
