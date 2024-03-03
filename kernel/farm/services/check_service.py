# -*- coding: utf-8 -*-

from farm.models import UsersModel

from typing import Optional

class CheckService():
    """
    Сервисы для проверки пользователей
    """

    @staticmethod
    def user_exists(user_id):
        # Реализация проверки существования пользователя
        # Возвращайте True, если пользователь существует, и False в противном случае
        # Например:
        return UsersModel.query.filter_by(id=user_id).first() is not None

    @staticmethod
    def check_ban(user_id: int) -> bool:
        """
        Функция проверки пользователя на бан

        :param user_id: ID пользователя

        :return: False пользователь не забанен, True пользователь в бане или
        не существует
        """

        user = UsersModel.query.get(user_id)

        if not user:
            return True

        return user.is_banned



    @staticmethod
    def get_phone_by_user_id(user_id: int) -> str:
        """
        Функция получения телефона по user_ID

        :param user_id: ID пользователя

        :return: Номер телефона
        """
        user = UsersModel.query.get(user_id)

        if user:
            return user.phone
        else:
            return ""
