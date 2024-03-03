# -*- coding: utf-8 -*-


import os
from datetime import datetime
from flask import current_app

from farm.models import Pictures
from farm import db

class PicturesService():
    """ Сервис для работы с изображениями """

    @staticmethod
    def generate_unique_picture_name() -> str:
        """
        Генерация случайных имен состоящих из даты
        """

        return str(datetime.now().timestamp())

    @staticmethod
    def save_picture(picture_name: str, picture_data: bytes) -> int:
        """
        Функция сохранения картинки в БД и в папку uploads

        :param picture_name: Имя картинки
        :param picture_data: Бинарная картинка

        :return: ID картинки
        """

        # Создаем папку uploads, если её еще нет
        uploads_folder = os.path.join(current_app.root_path, 'uploads')
        os.makedirs(uploads_folder, exist_ok=True)

        # Сохраняем картинку в базу данных и в папку uploads
        picture_path = os.path.join(uploads_folder, f'{picture_name}')
        with open(picture_path, 'wb') as picture_file:
            picture_file.write(picture_data)

        new_picture = Pictures(
            name=picture_name,
            image_data=picture_data,
            image_oid=b'',
            url=f'/uploads/pictures/{picture_name}'
        )

        db.session.add(new_picture)
        db.session.commit()

        return new_picture.id
