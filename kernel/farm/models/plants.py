# -*- coding: utf-8 -*-

from sqlalchemy import PickleType
from farm import db


class Ferma(db.Model):
    __tablename__ = 'ferma'

    id = db.Column(db.Integer, primary_key=True)

    garden_list = db.Column(PickleType)
    size = db.Column(db.String, nullable=False)


class Garden(db.Model):
    __tablename__ = 'garden'

    id = db.Column(db.Integer, primary_key=True)

    cells_list = db.Column(PickleType)
    name = db.Column(db.String, nullable=False)
    user = db.Column(db.Integer)


class GardenCell(db.Model):
    __tablename__ = 'garden_cell'

    id = db.Column(db.Integer, primary_key=True)

    status = db.Column(db.Boolean)
    seed = db.Column(db.Integer)


class Seeds(db.Model):
    __tablename__ = 'seeds'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    pictures = db.Column(db.Integer, info={'note': 'ID'})

    description = db.Column(db.Text, nullable=False)

    url_pics = db.Column(PickleType, info={'note': 'Список ID'})
    levels = db.Column(PickleType)
    seeds_list = db.Column(PickleType)

    start = db.Column(db.Date)
    information = db.Column(db.Integer)


class SeedInformation(db.Model):
    __tablename__ = 'seed_information'

    id = db.Column(db.Integer, primary_key=True)

    text = db.Column(db.Text, nullable=False)
    data = db.Column(db.Text, nullable=False)


class SeedLevel(db.Model):
    __tablename__ = 'seed_level'

    id = db.Column(db.Integer, primary_key=True)

    picture = db.Column(db.Integer, nullable=False)
    levels = db.Column(PickleType, nullable=False)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
