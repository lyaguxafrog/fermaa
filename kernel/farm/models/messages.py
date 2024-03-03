# -*- coding: utf-8 -*-

from farm import db
from sqlalchemy import PickleType



class Chat(db.Model):
    __tablename__ = 'chat'

    id = db.Column(db.Integer, primary_key=True)

    user_1 = db.Column(db.Integer, nullable=False)
    user_2 = db.Column(db.Integer, nullable=False)

    messages = db.relationship('Message', backref='chat', lazy=True, cascade='all, delete-orphan')

class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)

    message_owner = db.Column(db.Integer)
    sendtime = db.Column(db.Date, nullable=False)
    text = db.Column(db.Text, nullable=False)

    is_read = db.Column(db.Boolean)

    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
