# -*- coding: utf-8 -*-

from sqlalchemy import PickleType
from farm import db


class Pictures(db.Model):
    __tablename__ = 'pictures'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, info={'note': 'Можно рандомную генерацию'})
    image_oid = db.Column(db.LargeBinary, nullable=False)
    image_data = db.Column(db.LargeBinary, nullable=False)

    url = db.Column(db.String)

    __table_args__ = (
        db.UniqueConstraint('name', 'url', name='_name_url_uc'),
    )


class LikesToPosts(db.Model):
    __tablename__ = 'likes_to_posts'

    id = db.Column(db.Integer, primary_key=True)

    like_owner = db.Column(db.Integer)
    post_id = db.Column(db.Integer)
    timestamp = db.Column(db.Date)


class LikesToReview(db.Model):
    __tablename__ = 'likes_to_review'

    id = db.Column(db.Integer, primary_key=True)

    review_id = db.Column(db.Integer)
    owner_id = db.Column(db.Integer)
    date = db.Column(db.Date)


class DislikesToReview(db.Model):
    __tablename__ = 'dislikes_to_review'

    id = db.Column(db.Integer, primary_key=True)

    review_id = db.Column(db.Integer)
    owner_id = db.Column(db.Integer)
    date = db.Column(db.Date)
