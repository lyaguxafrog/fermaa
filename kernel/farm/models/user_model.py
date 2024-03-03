# -*- coding: utf-8 -*-

from flask_login import UserMixin
from sqlalchemy import PickleType
from werkzeug.security import check_password_hash


from farm import db


class UsersModel(UserMixin, db.Model):
    """ Модель пользователя """

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    email = db.Column(db.String, nullable=False, unique=True)
    phone = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    role = db.Column(db.String, nullable=False)

    sub_level = db.Column(db.String, default="light")
    achievements = db.Column(PickleType, info={'note': 'Список достижений'})

    icoins = db.Column(db.Integer)
    plastic_bottles = db.Column(db.Integer,
                                info={'note': 'Кол-во пластиковых бутылок'})
    alum_bottles = db.Column(db.Integer,
                             info={'note': 'Кол-во алюминиевых бутылок'})

    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    username = db.Column(db.String, unique=True)
    gender = db.Column(db.String)
    bday = db.Column(db.Date)

    friends = db.Column(PickleType, info={'note': 'Взаимоподписки'})
    followers = db.Column(PickleType)
    following = db.Column(PickleType)

    user_posts = db.relationship('Posts', backref='post_user',
                                 lazy=True, overlaps="post_user")
    chats = db.Column(PickleType)

    farms = db.Column(PickleType)
    _3d_models = db.Column(PickleType)
    gifts_3d = db.Column(PickleType)
    seeds = db.Column(PickleType)
    farm_gifts = db.Column(PickleType)
    reviews = db.Column(PickleType)

    is_banned = db.Column(db.Boolean, default=False)

    def get_id(self):
        return str(self.id)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Gift(db.Model):
    """ Модель подарков """


    __tablename__ = 'gift'

    id = db.Column(db.Integer, primary_key=True)

    from_user = db.Column(db.Integer, nullable=False)
    to_user = db.Column(db.Integer, nullable=False)
    count = db.Column(PickleType, nullable=False)
    comment = db.Column(db.String, nullable=False)
