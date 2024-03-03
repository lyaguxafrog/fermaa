# -*- coding: utf-8 -*-

from email.policy import default
from flask_admin.contrib.sqla import ModelView
from sqlalchemy import PickleType
from sqlalchemy.orm import relationship

from farm import db


class Posts(db.Model):
    """ Модель постов """

    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)

    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = relationship('UsersModel', backref='post_user', overlaps="post_user")

    timestamp = db.Column(db.Date)

    post_text = db.Column(db.Text)
    picture = db.Column(db.Integer)

    views = db.Column(db.Integer, default=0)
    likes = db.Column(db.Integer, default=0)
    comments = db.Column(PickleType)




class PostComment(db.Model):
    """ Модель комментариев """


    __tablename__ = 'post_comments'

    id = db.Column(db.Integer, primary_key=True)

    comment_owner = db.Column(db.Integer)
    post = db.Column(db.Integer)
    text = db.Column(db.Text, nullable=False)
