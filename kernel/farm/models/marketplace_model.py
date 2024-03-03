# -*- coding: utf-8 -*-

from sqlalchemy import PickleType
from sqlalchemy.orm import relationship
from datetime import datetime

from farm import db


class Lot(db.Model):
    __tablename__ = 'lots'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    picture_id = db.Column(db.Integer, db.ForeignKey('pictures.id', ondelete='CASCADE'), unique=True)
    picture = relationship('Pictures', backref='lot', uselist=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    summ = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Float, nullable=True)
    reviews_list = db.Column(PickleType, nullable=True)
    reviews = relationship('Review', backref='lot', lazy=True)


class Category(db.Model):
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    cat = db.Column(db.String, nullable=False)


class Review(db.Model):
    """ Модель оценки/отзыва """


    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)

    owner_id = db.Column(db.Integer, nullable=False)
    lot_id = db.Column(db.Integer, db.ForeignKey('lots.id'))

    timestamp = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    text = db.Column(db.Text, nullable=False)
    rate = db.Column(db.Float, nullable=False)

    magazine_answer = db.Column(db.Text)

    pictures = db.Column(PickleType, info={'note': 'ID картинок'})

    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)


class LotDescription(db.Model):
    """ Модель описания лота """


    __tablename__ = 'lot_description'

    id = db.Column(db.Integer, primary_key=True)

    lot_id = db.Column(db.Integer)
    text_1 = db.Column(db.String)
    text_2 = db.Column(db.String)
