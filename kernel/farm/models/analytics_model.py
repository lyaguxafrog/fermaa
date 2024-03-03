# -*- coding: utf-8 -*-

from farm import db


class FarmAnalytic(db.Model):
    __tablename__ = 'farm_analytic'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Date)
    co2 = db.Column(db.Integer)
    air_temperature = db.Column(db.Integer)
    air_humidity = db.Column(db.Integer)
    UV_index = db.Column(db.Integer)
    soil_humidity_1_centimeter = db.Column(db.Integer)
    soil_humidity_1_5_centimeter = db.Column(db.Integer)


class PrintedAnalytic(db.Model):
    __tablename__ = 'printed_analytic'

    id = db.Column(db.Integer, primary_key=True)

    total_printers = db.Column(db.Integer)
    free_printers = db.Column(db.Integer)
    printers_info = db.Column(db.JSON)
    update_time = db.Column(db.Date)
