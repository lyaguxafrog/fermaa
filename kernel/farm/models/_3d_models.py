# -*- coding: utf-8 -*-

from sqlalchemy import PickleType
from farm import db


class Printer(db.Model):
    """ Модель принтеров """


    __tablename__ = 'printer'

    id = db.Column(db.Integer, primary_key=True)

    status = db.Column(db.Boolean, nullable=False)
    size = db.Column(db.String, nullable=False)
    used = db.Column(db.Integer)

    model_id = db.Column(db.Integer)


class _3DModel(db.Model):
    """ Модель 3Д модели """

    __tablename__ = 'model'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.Date, nullable=False)
    pictures = db.Column(db.Integer, nullable=False)
    file_size = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    levels = db.Column(PickleType, nullable=False)

    user_id = db.Column(db.Integer)
    current_level = db.Column(db.String)
    time_start = db.Column(db.Date)
    models = db.Column(PickleType)
    model_size = db.Column(db.String)
    model_height = db.Column(db.String, info={'note': 'высота'})


class Levels3D(db.Model):
    """ Модель уровней для 3D моделей """

    __tablename__ = 'levels_3d'

    id = db.Column(db.Integer, primary_key=True)

    pictures = db.Column(db.Integer, nullable=False)
    text = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    end_time = db.Column(db.Date)
