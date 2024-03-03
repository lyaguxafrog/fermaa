# -*- coding: utf-8 -*-


from farm import db
from farm.models import Message, Chat

from datetime import datetime

class ChatServices:
    """
    Сервисы для отправки/получения сообщений
    """

    def __init__(self, socketio):
        self.socketio = socketio

    @staticmethod
    def create_chat(user_1, user_2):
        try:
            chat = Chat(user_1=user_1, user_2=user_2, messages=[])  # Use fixed values
            db.session.add(chat)
            db.session.commit()
            return chat.id
        except Exception as e:
            # Log the exception
            print(f"Error creating chat: {e}")
            db.session.rollback()  # Rollback changes in case of an error
            return None

    @staticmethod
    def send_message(chat_id, message_owner, text):
        try:
            sendtime = datetime.now().date()  # Provide a valid date
            message = Message(message_owner=message_owner, sendtime=sendtime, text=text)
            chat = Chat.query.get(chat_id)

            if chat:
                chat.messages.append(message)
                db.session.commit()
                return message.id
            else:
                print(f"Chat with ID {chat_id} not found.")
                return None

        except Exception as e:
            print(f"Error in send_message: {e}")
            return None

    @staticmethod
    def mark_message_as_read(self, chat_id, message_id):
        chat = Chat.query.get(chat_id)
        if chat:
            for message in chat.messages:
                if message.id == message_id:
                    message.is_read = True
                    db.session.commit()
                    return True
        return False

    @staticmethod
    def handle_connect(self):
        print('Client connected')

    @staticmethod
    def handle_send_message(self, data):
        chat_id = data['chat_id']
        message_owner = data['message_owner']
        text = data['text']

        message_id = self.send_message(chat_id, message_owner, text)

        if message_id:
            self.socketio.emit('message_sent', {'message_id': message_id},
                               room=chat_id)

    @staticmethod
    def handle_mark_as_read(self, data):
        chat_id = data['chat_id']
        message_id = data['message_id']

        if self.mark_message_as_read(chat_id, message_id):
            self.socketio.emit('marked_as_read', {'message_id': message_id},
                               room=chat_id)
