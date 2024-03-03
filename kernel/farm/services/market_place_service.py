# -*- coding: utf-8 -*-


from datetime import datetime
from typing import Optional, List

from farm import db
from farm.models import (Lot, LotDescription, Category, DislikesToReview,
                         LikesToReview, Review, Gift)
from farm.services import PicturesService

class MarketPlaceService():


    @staticmethod
    def create_category(cat: str) -> Category:
        """
        Функция создания категории

        :param cat: Название категории

        :return: Созданная категория
        """
        category = Category(cat=cat) # type: ignore

        try:
            db.session.add(category)
            db.session.commit()
            return category
        except Exception as e:
            db.session.rollback()
            raise e


    @staticmethod
    def create_lot(name: str, picture_id: int, category_id: int,
                        summ: int, review: Optional[float] = None,
                        reviews_list: Optional[List[str]] = None) -> Lot:
        """
        Функция создания лота

        :param name: Название лота
        :param picture_id: ID изображения лота
        :param category_id: ID категории лота
        :param summ: Сумма лота
        :param review: Оценка лота (может быть None)
        :param reviews_list: Список отзывов (может быть None)

        :return: Созданный лот
        """


        lot = Lot(name=name, picture_id=picture_id,
                  category_id=category_id, summ=summ,
                  review=review, reviews_list=reviews_list) # type: ignore

        try:
            db.session.add(lot)
            db.session.commit()
            return lot
        except Exception as e:
            db.session.rollback()
            raise e

    @staticmethod
    def create_lot_description(lot_id: int,
                               text_1: str, text_2: str) -> LotDescription:
        """
        Функция создания описания лота

        :param lot_id: ID лота
        :param text_1: Текст первой части описания
        :param text_2: Текст второй части описания

        :return: Созданное описание лота
        """

        lot_description = LotDescription(
            lot_id=lot_id,
            text_1=text_1,
            text_2=text_2) # type: ignore

        try:
            db.session.add(lot_description)
            db.session.commit()
            return lot_description
        except Exception as e:
            db.session.rollback()
            raise e
